import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

# Assuming DataProcessor and AnalysisEngine are in src/
from src.data_processor import DataProcessor
from src.analysis_engine import AnalysisEngine

# Define base directory for relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize data processing and analysis engines
processor = DataProcessor(
    raw_data_dir=os.path.join(BASE_DIR, 'data', 'raw'),
    processed_data_dir=os.path.join(BASE_DIR, 'data', 'processed')
)
engine = AnalysisEngine(
    processed_data_dir=os.path.join(BASE_DIR, 'data', 'processed')
)

# ------------------------------
# Load data (ensure these files exist after running data_processor.py and analysis_engine.py)
# ------------------------------
try:
    analysis_df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'processed', 'tech_analysis_final.csv'))
    trends_df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'processed', 'trends_processed.csv'), index_col='date', parse_dates=True)
except FileNotFoundError:
    print("Error: Data files not found. Please run data_processor.py and analysis_engine.py first.")
    # Exit or handle gracefully, e.g., by creating dummy data or running the scripts programmatically
    # For this example, we'll create empty dataframes to prevent app crash
    analysis_df = pd.DataFrame(columns=['technology', 'momentum_score', 'search_growth', 'github_stars', 'tech_status'])
    trends_df = pd.DataFrame()

# ------------------------------
# Dash app
# ------------------------------
app = dash.Dash(__name__)

# Define a dark theme color palette
DARK_BG = "#0e1117"
CARD_BG = "#1e1e2f"
TEXT_LIGHT = "#f0f0f0"
TEXT_MUTED = "#a0a0a0"
ACCENT_BLUE = "#3b82f6"
ACCENT_GREEN = "#10b981"
ACCENT_ORANGE = "#f59e0b"
BORDER_RADIUS = "12px"

# Custom template for Plotly graphs (dark)
plotly_template = dict(
    layout=dict(
        paper_bgcolor=DARK_BG,
        plot_bgcolor=DARK_BG,
        font=dict(color=TEXT_LIGHT),
        title=dict(font=dict(color=TEXT_LIGHT)),
        xaxis=dict(gridcolor="#2d2d3a", linecolor="#2d2d3a", tickfont=dict(color=TEXT_MUTED)),
        yaxis=dict(gridcolor="#2d2d3a", linecolor="#2d2d3a", tickfont=dict(color=TEXT_MUTED)),
        legend=dict(font=dict(color=TEXT_LIGHT))
    )
)

# ------------------------------
# App layout
# ------------------------------
app.layout = html.Div(
    style={
        "backgroundColor": DARK_BG,
        "fontFamily": "'Inter', 'Segoe UI', Arial, sans-serif",
        "padding": "20px",
        "minHeight": "100vh",
        "color": TEXT_LIGHT
    },
    children=[
        # Header
        html.Div(
            style={
                "backgroundColor": CARD_BG,
                "padding": "30px",
                "borderRadius": BORDER_RADIUS,
                "marginBottom": "30px",
                "textAlign": "center",
                "boxShadow": "0 8px 20px rgba(0,0,0,0.3)"
            },
            children=[
                html.H1(
                    "🚀 Emerging Tech Momentum Radar",
                    style={"margin": "0", "fontWeight": "600", "letterSpacing": "-0.5px"}
                ),
                html.P(
                    "Track emerging technology trends and compare search interest with open-source activity",
                    style={"marginTop": "10px", "color": TEXT_MUTED, "fontSize": "16px"}
                )
            ]
        ),
        
        # Metrics row
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "gap": "20px",
                "marginBottom": "30px",
                "flexWrap": "wrap"
            },
            children=[
                # Top Technology
                html.Div(
                    style={
                        "flex": "1",
                        "backgroundColor": CARD_BG,
                        "padding": "20px",
                        "borderRadius": BORDER_RADIUS,
                        "textAlign": "center",
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.2)"
                    },
                    children=[
                        html.H3("🏆 Top Technology", style={"margin": "0", "color": TEXT_MUTED, "fontSize": "18px"}),
                        html.H2(
                            analysis_df.loc[analysis_df['momentum_score'].idxmax(), 'technology'] if not analysis_df.empty else 'N/A',
                            style={"margin": "10px 0 0", "color": ACCENT_BLUE, "fontWeight": "700"}
                        )
                    ]
                ),
                # Avg Momentum Score
                html.Div(
                    style={
                        "flex": "1",
                        "backgroundColor": CARD_BG,
                        "padding": "20px",
                        "borderRadius": BORDER_RADIUS,
                        "textAlign": "center",
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.2)"
                    },
                    children=[
                        html.H3("📊 Avg Momentum Score", style={"margin": "0", "color": TEXT_MUTED, "fontSize": "18px"}),
                        html.H2(
                            f"{analysis_df['momentum_score'].mean():.1f}" if not analysis_df.empty else 'N/A',
                            style={"margin": "10px 0 0", "color": ACCENT_GREEN, "fontWeight": "700"}
                        )
                    ]
                ),
                # Tech Count
                html.Div(
                    style={
                        "flex": "1",
                        "backgroundColor": CARD_BG,
                        "padding": "20px",
                        "borderRadius": BORDER_RADIUS,
                        "textAlign": "center",
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.2)"
                    },
                    children=[
                        html.H3("🔢 Tech Count", style={"margin": "0", "color": TEXT_MUTED, "fontSize": "18px"}),
                        html.H2(
                            len(analysis_df) if not analysis_df.empty else 0,
                            style={"margin": "10px 0 0", "color": ACCENT_ORANGE, "fontWeight": "700"}
                        )
                    ]
                )
            ]
        ),
        
        # Charts row
        html.Div(
            style={"display": "flex", "gap": "20px", "marginBottom": "30px", "flexWrap": "wrap"},
            children=[
                html.Div(
                    style={"flex": "1", "backgroundColor": CARD_BG, "borderRadius": BORDER_RADIUS, "padding": "15px"},
                    children=[dcc.Graph(id="momentum-bubble", config={"displayModeBar": False})]
                ),
                html.Div(
                    style={"flex": "1", "backgroundColor": CARD_BG, "borderRadius": BORDER_RADIUS, "padding": "15px"},
                    children=[dcc.Graph(id="status-distribution", config={"displayModeBar": False})]
                )
            ]
        ),
        
        # Table
        html.Div(
            style={
                "backgroundColor": CARD_BG,
                "borderRadius": BORDER_RADIUS,
                "padding": "20px",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.2)"
            },
            children=[
                html.H3("📈 Technology Rankings", style={"margin": "0 0 20px 0", "fontWeight": "600"}),
                html.Table(
                    style={"width": "100%", "borderCollapse": "collapse"},
                    children=[
                        html.Thead(
                            html.Tr(
                                [
                                    html.Th("Technology", style={"padding": "12px", "backgroundColor": "#2d2d3a", "color": TEXT_LIGHT}),
                                    html.Th("Momentum Score", style={"padding": "12px", "backgroundColor": "#2d2d3a", "color": TEXT_LIGHT}),
                                    html.Th("Search Growth", style={"padding": "12px", "backgroundColor": "#2d2d3a", "color": TEXT_LIGHT}),
                                    html.Th("GitHub Stars", style={"padding": "12px", "backgroundColor": "#2d2d3a", "color": TEXT_LIGHT}),
                                    html.Th("Status", style={"padding": "12px", "backgroundColor": "#2d2d3a", "color": TEXT_LIGHT})
                                ]
                            )
                        ),
                        html.Tbody(
                            [
                                html.Tr(
                                    [
                                        html.Td(row["technology"], style={"padding": "10px", "borderBottom": "1px solid #2d2d3a"}),
                                        html.Td(f"{row['momentum_score']:.1f}", style={"padding": "10px", "borderBottom": "1px solid #2d2d3a"}),
                                        html.Td(f"{row['search_growth']:.2f}", style={"padding": "10px", "borderBottom": "1px solid #2d2d3a"}),
                                        html.Td(f"{row['github_stars']:,}", style={"padding": "10px", "borderBottom": "1px solid #2d2d3a"}),
                                        html.Td(row["tech_status"], style={"padding": "10px", "borderBottom": "1px solid #2d2d3a"})
                                    ]
                                )
                                for _, row in analysis_df.nlargest(5, "momentum_score").iterrows()
                            ] if not analysis_df.empty else []
                        )
                    ]
                )
            ]
        )
    ]
)

# ------------------------------
# Callbacks
# ------------------------------
@app.callback(
    Output("momentum-bubble", "figure"),
    Input("momentum-bubble", "id")
)
def update_bubble(_):
    if analysis_df.empty:
        return go.Figure()

    fig = px.scatter(
        analysis_df,
        x="search_growth",
        y="momentum_score",
        size="github_stars",
        color="tech_status",
        hover_name="technology",
        title="Tech Momentum Radar: Search Growth vs Momentum Score",
        labels={
            "search_growth": "Search Interest Growth (YoY)",
            "momentum_score": "Momentum Score (0-100)",
            "github_stars": "GitHub Stars"
        },
        template="plotly_dark",
        color_discrete_map={
            "Stable/Mature": ACCENT_BLUE,
            "Rising Star": ACCENT_GREEN,
            "Speculative/Hype": ACCENT_ORANGE
        }
    )
    fig.update_layout(
        title_font_size=18,
        title_x=0.5,
        plot_bgcolor=CARD_BG,
        paper_bgcolor=CARD_BG,
        font=dict(color=TEXT_LIGHT),
        legend=dict(bgcolor=CARD_BG)
    )
    return fig

@app.callback(
    Output("status-distribution", "figure"),
    Input("status-distribution", "id")
)
def update_distribution(_):
    if analysis_df.empty:
        return go.Figure()

    status_counts = analysis_df["tech_status"].value_counts()
    fig = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Technology Status Distribution",
        template="plotly_dark",
        color_discrete_sequence=[ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE]
    )
    fig.update_layout(
        title_font_size=18,
        title_x=0.5,
        plot_bgcolor=CARD_BG,
        paper_bgcolor=CARD_BG,
        font=dict(color=TEXT_LIGHT),
        legend=dict(bgcolor=CARD_BG)
    )
    return fig

# ------------------------------
# Run server
# ------------------------------
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
