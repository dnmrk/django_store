import numpy as np
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db.sqlite3"


def get_engine():
    return create_engine(f"sqlite:///{DB_PATH}")


def get_daily_revenue() -> pd.DataFrame:
    query = text("""
        SELECT
            DATE(o.created_at) as date,
            SUM(oi.price * oi.quantity) as revenue
        FROM orders_order o
        JOIN orders_orderitem oi ON oi.order_id = o.id
        WHERE o.status != 'cancelled'
        GROUP BY DATE(o.created_at)
        ORDER BY date ASC
    """)
    with get_engine().connect() as conn:
        df = pd.read_sql(query, conn)
    df["date"] = pd.to_datetime(df["date"])
    return df


def get_product_daily_sales() -> pd.DataFrame:
    query = text("""
        SELECT
            DATE(o.created_at) as date,
            pp.id as product_id,
            pp.name as product_name,
            pp.stock as current_stock,
            SUM(oi.quantity) as units_sold
        FROM orders_orderitem oi
        JOIN orders_order o ON o.id = oi.order_id
        JOIN products_product pp ON pp.id = oi.product_id
        WHERE o.status != 'cancelled'
        GROUP BY DATE(o.created_at), pp.id
        ORDER BY date ASC
    """)
    with get_engine().connect() as conn:
        df = pd.read_sql(query, conn)
    df["date"] = pd.to_datetime(df["date"])
    return df


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["day_index"] = (df["date"] - df["date"].min()).dt.days
    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
    return df


def forecast_revenue(days_ahead: int = 30) -> dict:
    df = get_daily_revenue()

    if len(df) < 7:
        return {
            "error": "Not enough data to forecast. Need at least 7 days of orders.",
            "historical": [],
            "forecast": [],
        }

    # Fill missing dates with 0 revenue
    full_range = pd.date_range(df["date"].min(), df["date"].max())
    df = df.set_index("date").reindex(full_range, fill_value=0).reset_index()
    df.columns = ["date", "revenue"]

    df = build_features(df)

    # Train model on historical data
    feature_cols = ["day_index", "day_of_week", "month", "is_weekend"]
    X = df[feature_cols]
    y = df["revenue"]

    model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
    model.fit(X, y)

    # Build future dates
    last_date = df["date"].max()
    future_dates = [last_date + timedelta(days=i) for i in range(1, days_ahead + 1)]
    future_df = pd.DataFrame({"date": future_dates})
    future_df = build_features(future_df)

    # Predict
    future_predictions = model.predict(future_df[feature_cols])
    future_predictions = np.clip(future_predictions, 0, None)  # no negative revenue

    # Format results
    historical = [
        {"date": row["date"].strftime("%Y-%m-%d"), "revenue": round(float(row["revenue"]), 2)}
        for _, row in df.tail(60).iterrows()
    ]

    forecast = [
        {"date": d.strftime("%Y-%m-%d"), "revenue": round(float(p), 2)}
        for d, p in zip(future_dates, future_predictions)
    ]

    total_forecast = round(float(sum(future_predictions)), 2)
    avg_daily = round(float(np.mean(future_predictions)), 2)

    return {
        "historical": historical,
        "forecast": forecast,
        "summary": {
            "days_ahead": days_ahead,
            "total_forecast_revenue": total_forecast,
            "avg_daily_revenue": avg_daily,
            "forecast_start": future_dates[0].strftime("%Y-%m-%d"),
            "forecast_end": future_dates[-1].strftime("%Y-%m-%d"),
        }
    }


def forecast_product_demand(days_ahead: int = 30) -> list:
    df = get_product_daily_sales()

    if df.empty:
        return []

    results = []

    for product_id, group in df.groupby("product_id"):
        product_name = group["product_name"].iloc[0]
        current_stock = group["current_stock"].iloc[0]

        # Fill missing dates
        full_range = pd.date_range(group["date"].min(), group["date"].max())
        g = group.set_index("date")["units_sold"].reindex(full_range, fill_value=0).reset_index()
        g.columns = ["date", "units_sold"]

        if len(g) < 5:
            continue

        g = build_features(g)

        feature_cols = ["day_index", "day_of_week", "month", "is_weekend"]
        X = g[feature_cols]
        y = g["units_sold"]

        model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
        model.fit(X, y)

        last_date = g["date"].max()
        future_dates = [last_date + timedelta(days=i) for i in range(1, days_ahead + 1)]
        future_df = pd.DataFrame({"date": future_dates})
        future_df = build_features(future_df)

        predictions = model.predict(future_df[feature_cols])
        predictions = np.clip(predictions, 0, None)
        total_predicted = round(float(sum(predictions)), 1)
        daily_avg = round(float(np.mean(predictions)), 1)

        # Restock alert: will stock run out before the forecast period ends?
        days_until_stockout = None
        if daily_avg > 0:
            days_until_stockout = round(current_stock / daily_avg)

        results.append({
            "product_id": product_id,
            "product_name": product_name,
            "current_stock": int(current_stock),
            "predicted_units": total_predicted,
            "avg_daily_demand": daily_avg,
            "days_until_stockout": days_until_stockout,
            "needs_restock": days_until_stockout is not None and days_until_stockout < days_ahead,
        })

    # Sort by most urgent restock first
    results.sort(key=lambda x: (not x["needs_restock"], x.get("days_until_stockout") or 9999))
    return results