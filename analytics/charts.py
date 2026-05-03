import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

STATUS_COLORS = {
    "pending": "#378ADD",
    "processing": "#BA7517",
    "shipped": "#7F77DD",
    "delivered": "#1D9E75",
    "cancelled": "#E24B4A",
}

def revenue_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data yet", showarrow=False)
        return fig

    fig = px.area(
        df,
        x="date",
        y="revenue",
        labels={"date": "Date", "revenue": "Revenue (₱)"},
        color_discrete_sequence=["#1D9E75"],
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#eee"),
        hovermode="x unified",
    )
    fig.update_traces(line_color="#1D9E75", fillcolor="rgba(29,158,117,0.1)")
    return fig

def category_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data yet", showarrow=False)
        return fig

    fig = px.bar(
        df,
        x="revenue",
        y="category",
        orientation="h",
        labels={"revenue": "Revenue (₱)", "category": "Category"},
        color="category",
        color_discrete_sequence=["#378ADD", "#1D9E75", "#BA7517", "#D4537E", "#888780"],
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        yaxis=dict(categoryorder="total ascending"),
    )
    return fig

def status_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data yet", showarrow=False)
        return fig

    colors = [STATUS_COLORS.get(s, "#888780") for s in df["status"]]
    fig = go.Figure(go.Pie(
        labels=df["status"].str.capitalize(),
        values=df["count"],
        hole=0.55,
        marker_colors=colors,
        textinfo="percent",
        hovertemplate="%{label}: %{value} orders<extra></extra>",
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="v", x=1, y=0.5),
        showlegend=True,
    )
    return fig