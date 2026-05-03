from shiny import App, ui, render, reactive
import pandas as pd
import plotly.graph_objects as go
from db import (
    get_kpis,
    get_revenue_over_time,
    get_sales_by_category,
    get_order_status_breakdown,
    get_top_products,
    get_low_stock_products,
    get_forecast_data
)
from charts import revenue_chart, category_chart, status_chart

# ─── UI ───────────────────────────────────────────────────────────────────────

app_ui = ui.page_fluid(

    ui.head_content(
        ui.tags.script(src="https://cdn.plot.ly/plotly-2.32.0.min.js"),
        ui.tags.style("""
            body { background: #f8f9fa; font-family: sans-serif; }
            .topbar { background: #1a1a2e; color: white; padding: 14px 24px;
                      display: flex; justify-content: space-between; align-items: center; }
            .topbar h4 { margin: 0; font-size: 18px; }
            .topbar small { color: #aaa; font-size: 12px; }
            .badge-shiny { background: #4ECDC4; color: #04342C; padding: 3px 10px;
                           border-radius: 99px; font-size: 12px; font-weight: 600; }
            .kpi-card { background: white; border-radius: 10px; padding: 16px 20px;
                        border: 1px solid #eee; margin-bottom: 4px; }
            .kpi-label { font-size: 13px; color: #888; margin-bottom: 4px; }
            .kpi-value { font-size: 26px; font-weight: 600; color: #1a1a2e; }
            .kpi-sub { font-size: 12px; margin-top: 4px; }
            .up { color: #1D9E75; } .down { color: #E24B4A; }
            .chart-card { background: white; border-radius: 10px; padding: 16px;
                          border: 1px solid #eee; margin-bottom: 16px; }
            .chart-card h6 { font-size: 14px; font-weight: 600;
                             color: #1a1a2e; margin-bottom: 12px; }
            .section-label { font-size: 13px; font-weight: 600; color: #555;
                             text-transform: uppercase; letter-spacing: 0.5px;
                             margin: 16px 0 8px; }
            .filter-row { background: white; padding: 10px 24px;
                          border-bottom: 1px solid #eee; display: flex;
                          align-items: center; gap: 12px; }
            table { width: 100%; border-collapse: collapse; font-size: 13px; }
            th { color: #888; font-weight: 500; text-align: left;
                 padding: 6px 0; border-bottom: 1px solid #eee; }
            td { padding: 7px 0; border-bottom: 1px solid #f5f5f5; color: #333; }
            .badge-critical { background: #FCEBEB; color: #A32D2D; padding: 2px 8px;
                              border-radius: 99px; font-size: 11px; }
            .badge-low { background: #FAEEDA; color: #854F0B; padding: 2px 8px;
                         border-radius: 99px; font-size: 11px; }
        """)
    ),

    ui.div({"class": "section-label"}, "Forecasting"),
    ui.layout_columns(
        ui.div(
            {"class": "chart-card"},
            ui.h6("Revenue forecast"),
            ui.input_select(
                "forecast_days",
                label=None,
                choices={"7": "7 days", "30": "30 days", "60": "60 days", "90": "90 days"},
                selected="30",
                width="140px",
            ),
            ui.output_ui("plot_forecast"),
        ),
        ui.div(
            {"class": "chart-card"},
            ui.h6("Restock alerts"),
            ui.output_ui("table_restock"),
        ),
        col_widths=[7, 5],
    ),

    ui.div(
        {"class": "topbar"},
        ui.div(
            ui.h4("Store Analytics Dashboard"),
            ui.tags.small("Live data from Django Store"),
        ),
        ui.span({"class": "badge-shiny"}, "shiny"),
    ),

    ui.div(
        {"class": "filter-row"},
        ui.tags.label("Date range:", style="font-size:13px;color:#555;font-weight:500;"),
        ui.input_select(
            "date_range",
            label=None,
            choices={
                "7": "Last 7 days",
                "30": "Last 30 days",
                "90": "Last 90 days",
                "365": "This year",
                "0": "All time",
            },
            selected="30",
            width="180px",
        ),
        ui.input_select(
            "stock_threshold",
            label=None,
            choices={"5": "Stock ≤ 5", "10": "Stock ≤ 10", "20": "Stock ≤ 20"},
            selected="10",
            width="160px",
        ),
        ui.input_action_button("refresh", "Refresh", class_="btn btn-sm btn-outline-secondary"),
    ),

    ui.div(
        {"style": "padding: 20px 24px;"},

        # ── KPI Cards ──────────────────────────────────────────────────────────
        ui.div({"class": "section-label"}, "Key Metrics"),
        ui.layout_columns(
            ui.div(
                {"class": "kpi-card"},
                ui.div({"class": "kpi-label"}, "Total Revenue"),
                ui.output_text("kpi_revenue"),
            ),
            ui.div(
                {"class": "kpi-card"},
                ui.div({"class": "kpi-label"}, "Orders Placed"),
                ui.output_text("kpi_orders"),
            ),
            ui.div(
                {"class": "kpi-card"},
                ui.div({"class": "kpi-label"}, "Avg. Order Value"),
                ui.output_text("kpi_avg"),
            ),
            ui.div(
                {"class": "kpi-card"},
                ui.div({"class": "kpi-label"}, "Low Stock Items"),
                ui.output_text("kpi_stock"),
            ),
            col_widths=[3, 3, 3, 3],
        ),

        # ── Charts Row 1 ───────────────────────────────────────────────────────
        ui.div({"class": "section-label"}, "Revenue & Sales"),
        ui.layout_columns(
            ui.div(
                {"class": "chart-card"},
                ui.h6("Revenue over time"),
                ui.output_ui("plot_revenue"),
            ),
            ui.div(
                {"class": "chart-card"},
                ui.h6("Sales by category"),
                ui.output_ui("plot_category"),
            ),
            col_widths=[7, 5],
        ),

        # ── Charts Row 2 ───────────────────────────────────────────────────────
        ui.div({"class": "section-label"}, "Orders & Products"),
        ui.layout_columns(
            ui.div(
                {"class": "chart-card"},
                ui.h6("Order status breakdown"),
                ui.output_ui("plot_status"),
            ),
            ui.div(
                {"class": "chart-card"},
                ui.h6("Top products"),
                ui.output_table("table_top_products"),
            ),
            col_widths=[4, 8],
        ),

        # ── Low Stock Table ────────────────────────────────────────────────────
        ui.div({"class": "section-label"}, "Inventory Alerts"),
        ui.div(
            {"class": "chart-card"},
            ui.h6("Low stock products"),
            ui.output_ui("table_low_stock"),
        ),
    ),
)

# ─── Server ───────────────────────────────────────────────────────────────────

def server(input, output, session):

    @reactive.calc
    def kpis():
        input.refresh()
        return get_kpis()

    @reactive.calc
    def revenue_data():
        input.refresh()
        days = int(input.date_range())
        df = get_revenue_over_time()
        if days > 0 and not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            cutoff = pd.Timestamp.now() - pd.Timedelta(days=days)
            df = df[df["date"] >= cutoff]
        return df

    @reactive.calc
    def low_stock_data():
        input.refresh()
        threshold = int(input.stock_threshold())
        return get_low_stock_products(threshold)

    @render.text
    def kpi_revenue():
        val = kpis()["total_revenue"]
        return f"₱{val:,.2f}"

    @render.text
    def kpi_orders():
        return str(kpis()["total_orders"])

    @render.text
    def kpi_avg():
        val = kpis()["avg_order_value"]
        return f"₱{val:,.2f}"

    @render.text
    def kpi_stock():
        return str(kpis()["low_stock_count"])

    @render.ui
    def plot_revenue():
        df = revenue_data()
        fig = revenue_chart(df)
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False))

    @render.ui
    def plot_category():
        input.refresh()
        df = get_sales_by_category()
        fig = category_chart(df)
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False))

    @render.ui
    def plot_status():
        input.refresh()
        df = get_order_status_breakdown()
        fig = status_chart(df)
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False))

    @render.table
    def table_top_products():
        input.refresh()
        df = get_top_products(5)
        if df.empty:
            return pd.DataFrame({"Message": ["No orders yet"]})
        df["revenue"] = df["revenue"].apply(lambda x: f"₱{x:,.2f}")
        df.columns = ["Product", "Category", "Units Sold", "Revenue"]
        return df

    @render.ui
    def table_low_stock():
        df = low_stock_data()
        if df.empty:
            return ui.p("No low stock items.", style="color:#888;font-size:13px;")

        rows = []
        for _, row in df.iterrows():
            badge_class = "badge-critical" if row["status"] == "Critical" else "badge-low"
            rows.append(ui.tags.tr(
                ui.tags.td(row["product"]),
                ui.tags.td(row["category"]),
                ui.tags.td(str(row["stock"])),
                ui.tags.td(ui.span({"class": badge_class}, row["status"])),
            ))

        return ui.tags.table(
            ui.tags.thead(ui.tags.tr(
                ui.tags.th("Product"),
                ui.tags.th("Category"),
                ui.tags.th("Stock"),
                ui.tags.th("Status"),
            )),
            ui.tags.tbody(*rows),
        )
    
    @reactive.calc
    def forecast_data():
        input.refresh()
        days = int(input.forecast_days())
        return get_forecast_data(days)

    @render.ui
    def plot_forecast():
        data = forecast_data()
        revenue = data["revenue"]

        if "error" in revenue:
            fig = go.Figure()
            fig.add_annotation(text=revenue["error"], showarrow=False)
            return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False))

        historical_dates = [p["date"] for p in revenue["historical"]]
        historical_vals = [p["revenue"] for p in revenue["historical"]]
        forecast_dates = [p["date"] for p in revenue["forecast"]]
        forecast_vals = [p["revenue"] for p in revenue["forecast"]]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=historical_dates, y=historical_vals,
            mode="lines", name="Historical",
            line=dict(color="#1D9E75", width=2),
            fill="tozeroy", fillcolor="rgba(29,158,117,0.08)"
        ))
        fig.add_trace(go.Scatter(
            x=forecast_dates, y=forecast_vals,
            mode="lines", name="Forecast",
            line=dict(color="#7F77DD", width=2, dash="dash"),
            fill="tozeroy", fillcolor="rgba(127,119,221,0.08)"
        ))
        fig.update_layout(
            margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", y=-0.2),
            hovermode="x unified",
        )
        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs=False))

    @render.ui
    def table_restock():
        data = forecast_data()
        products = data["products"]
        urgent = [p for p in products if p["needs_restock"]]

        if not urgent:
            return ui.p("No restock alerts.", style="color:#888;font-size:13px;")

        rows = []
        for p in urgent[:8]:
            days_left = p["days_until_stockout"]
            badge_class = "badge-critical" if days_left and days_left < 7 else "badge-low"
            rows.append(ui.tags.tr(
                ui.tags.td(p["product_name"]),
                ui.tags.td(str(p["current_stock"])),
                ui.tags.td(str(p["avg_daily_demand"])),
                ui.tags.td(ui.span({"class": badge_class},
                    f"{days_left}d" if days_left else "—")),
            ))

        return ui.tags.table(
            ui.tags.thead(ui.tags.tr(
                ui.tags.th("Product"),
                ui.tags.th("Stock"),
                ui.tags.th("Avg/day"),
                ui.tags.th("Runs out"),
            )),
            ui.tags.tbody(*rows),
        )

app = App(app_ui, server)