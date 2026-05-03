import os
from pathlib import Path
from sqlalchemy import create_engine, text
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db.sqlite3"

def get_engine():
    return create_engine(f"sqlite:///{DB_PATH}")

def get_revenue_over_time() -> pd.DataFrame:
    query = text("""
        SELECT
            DATE(created_at) as date,
            SUM(oi.price * oi.quantity) as revenue
        FROM orders_order o
        JOIN orders_orderitem oi ON oi.order_id = o.id
        WHERE o.status != 'cancelled'
        GROUP BY DATE(created_at)
        ORDER BY date ASC
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn)

def get_sales_by_category() -> pd.DataFrame:
    query = text("""
        SELECT
            pc.name as category,
            SUM(oi.quantity) as units_sold,
            SUM(oi.price * oi.quantity) as revenue
        FROM orders_orderitem oi
        JOIN orders_order o ON o.id = oi.order_id
        JOIN products_product pp ON pp.id = oi.product_id
        JOIN products_category pc ON pc.id = pp.category_id
        WHERE o.status != 'cancelled'
        GROUP BY pc.name
        ORDER BY revenue DESC
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn)

def get_order_status_breakdown() -> pd.DataFrame:
    query = text("""
        SELECT status, COUNT(*) as count
        FROM orders_order
        GROUP BY status
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn)

def get_top_products(limit: int = 5) -> pd.DataFrame:
    query = text(f"""
        SELECT
            pp.name as product,
            pc.name as category,
            SUM(oi.quantity) as units_sold,
            SUM(oi.price * oi.quantity) as revenue
        FROM orders_orderitem oi
        JOIN orders_order o ON o.id = oi.order_id
        JOIN products_product pp ON pp.id = oi.product_id
        JOIN products_category pc ON pc.id = pp.category_id
        WHERE o.status != 'cancelled'
        GROUP BY pp.name, pc.name
        ORDER BY revenue DESC
        LIMIT {limit}
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn)

def get_low_stock_products(threshold: int = 10) -> pd.DataFrame:
    query = text(f"""
        SELECT
            pp.name as product,
            pc.name as category,
            pp.stock,
            CASE
                WHEN pp.stock <= 3 THEN 'Critical'
                WHEN pp.stock <= 10 THEN 'Low'
                ELSE 'OK'
            END as status
        FROM products_product pp
        JOIN products_category pc ON pc.id = pp.category_id
        WHERE pp.stock <= {threshold} AND pp.available = 1
        ORDER BY pp.stock ASC
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn)

def get_kpis() -> dict:
    query = text("""
        SELECT
            ROUND(SUM(oi.price * oi.quantity), 2) as total_revenue,
            COUNT(DISTINCT o.id) as total_orders,
            ROUND(SUM(oi.price * oi.quantity) / COUNT(DISTINCT o.id), 2) as avg_order_value
        FROM orders_order o
        JOIN orders_orderitem oi ON oi.order_id = o.id
        WHERE o.status != 'cancelled'
    """)
    low_stock_query = text("""
        SELECT COUNT(*) as low_stock_count
        FROM products_product
        WHERE stock <= 10 AND available = 1
    """)
    with get_engine().connect() as conn:
        kpi_row = pd.read_sql(query, conn).iloc[0]
        low_stock_row = pd.read_sql(low_stock_query, conn).iloc[0]
    return {
        "total_revenue": kpi_row["total_revenue"] or 0,
        "total_orders": int(kpi_row["total_orders"] or 0),
        "avg_order_value": kpi_row["avg_order_value"] or 0,
        "low_stock_count": int(low_stock_row["low_stock_count"] or 0),
    }

def get_forecast_data(days_ahead: int = 30) -> dict:
    import sys
    sys.path.insert(0, str(BASE_DIR))
    from forecasting.engine import forecast_revenue, forecast_product_demand
    return {
        "revenue": forecast_revenue(days_ahead),
        "products": forecast_product_demand(days_ahead),
    }