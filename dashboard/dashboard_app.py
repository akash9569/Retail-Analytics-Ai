import sys
import os
import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import json
import requests
import io

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dashboard.dashboard_components import create_kpi_card, create_header, create_footer
from dashboard.pages.reports import get_reports_layout
from dashboard.pages.settings import get_settings_layout

# Import pipeline scripts
from scripts.run_pipeline import run_cleaning_pipeline
from scripts.run_features import run_feature_engineering
from scripts.run_forecasting import run_forecasting
from scripts.run_advanced import run_advanced_analytics

# Load Data
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
REPORTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'reports')

def load_global_data():
    try:
        df = pd.read_csv(os.path.join(DATA_DIR, 'retail_sales_cleaned.csv'))
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        
        # Load forecast metrics if available
        metrics_path = os.path.join(REPORTS_DIR, 'model_metrics.json')
        if os.path.exists(metrics_path):
            with open(metrics_path, 'r') as f:
                metrics = json.load(f)
        else:
            metrics = {}
            
        # Load advanced insights if available
        insights_path = os.path.join(REPORTS_DIR, 'advanced_insights.json')
        if os.path.exists(insights_path):
            with open(insights_path, 'r') as f:
                insights = json.load(f)
        else:
            insights = {}
            
        return df, metrics, insights
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame(), {}, {}

# Initial Load
df, metrics, insights = load_global_data()

# Initialize App with Dark Theme
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.SLATE, "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css"],
                suppress_callback_exceptions=True)
app.title = "Retail Analytics AI"

# Helper to style figures
def style_figure(fig):
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified"
    )
    return fig

# Dashboard Layout (The original layout)
def get_dashboard_layout():
    # Reload data to ensure fresh view
    global df, metrics, insights
    df, metrics, insights = load_global_data()
    
    if df.empty:
        return dbc.Container([
            html.H3("No Data Available", className="text-white text-center mt-5"),
            html.P("Please load a dataset via Settings or run the pipeline.", className="text-muted text-center")
        ])

    return dbc.Container([
        dcc.Tabs(className="custom-tabs mb-4", children=[
            # Tab 1: Executive Summary
            dcc.Tab(label='Executive Summary', className="custom-tab", selected_className="custom-tab--selected", children=[
                html.Br(),
                dbc.Row([
                    dbc.Col(create_kpi_card("Total Sales", f"${df['Total Sales'].sum():,.0f}", "success"), width=12, md=6, lg=3),
                    dbc.Col(create_kpi_card("Total Profit", f"${df['Profit'].sum():,.0f}", "info"), width=12, md=6, lg=3),
                    dbc.Col(create_kpi_card("Total Orders", f"{len(df):,}", "primary"), width=12, md=6, lg=3),
                    dbc.Col(create_kpi_card("Profit Margin", f"{(df['Profit'].sum()/df['Total Sales'].sum()*100):.1f}%", "warning"), width=12, md=6, lg=3),
                ], className="g-4 mb-4"),
                
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H4("Sales Trend", className="text-white mb-3"),
                            dcc.Graph(
                                figure=style_figure(px.line(
                                    df.groupby(pd.Grouper(key='Order Date', freq='ME'))['Total Sales'].sum().reset_index(), 
                                    x='Order Date', y='Total Sales', 
                                    color_discrete_sequence=['#3b82f6']
                                )).update_layout(height=350),
                                config={'responsive': True, 'displayModeBar': False},
                                style={'height': '350px'}
                            )
                        ], className="glass-card p-4")
                    ], width=12, lg=8),
                    dbc.Col([
                        html.Div([
                            html.H4("Category Distribution", className="text-white mb-3"),
                            dcc.Graph(
                                figure=style_figure(px.pie(
                                    df, values='Total Sales', names='Category', 
                                    color_discrete_sequence=px.colors.qualitative.Pastel
                                ).update_traces(textposition='inside', textinfo='percent+label')).update_layout(height=350),
                                config={'responsive': True, 'displayModeBar': False},
                                style={'height': '350px'}
                            )
                        ], className="glass-card p-4")
                    ], width=12, lg=4),
                ], className="g-4 mb-4")
            ]),
            
            # Tab 2: Regional Performance
            dcc.Tab(label='Regional Performance', className="custom-tab", selected_className="custom-tab--selected", children=[
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H4("Sales by Region", className="text-white mb-3"),
                            dcc.Graph(
                                figure=style_figure(px.bar(
                                    df.groupby('Region')['Total Sales'].sum().reset_index(),
                                    x='Region', y='Total Sales', color='Region',
                                    color_discrete_sequence=px.colors.qualitative.Bold
                                ))
                            )
                        ], className="glass-card p-4 mb-4")
                    ], width=6),
                    dbc.Col([
                        html.Div([
                            html.H4("Profit by Region", className="text-white mb-3"),
                            dcc.Graph(
                                figure=style_figure(px.bar(
                                    df.groupby('Region')['Profit'].sum().reset_index(),
                                    x='Region', y='Profit', color='Region',
                                    color_discrete_sequence=px.colors.qualitative.Bold
                                ))
                            )
                        ], className="glass-card p-4 mb-4")
                    ], width=6),
                ]),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H4("Geographic Sales Map", className="text-white mb-3"),
                            dcc.Graph(
                                figure=style_figure(px.choropleth(
                                    df.groupby('State')['Total Sales'].sum().reset_index(),
                                    locations='State', locationmode="USA-states",
                                    color='Total Sales', scope="usa", 
                                    color_continuous_scale="Viridis"
                                ))
                            )
                        ], className="glass-card p-4")
                    ], width=12)
                ])
            ]),
            
            # Tab 3: Product Insights
            dcc.Tab(label='Product Insights', className="custom-tab", selected_className="custom-tab--selected", children=[
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H4("Top 10 Products by Sales", className="text-white mb-3"),
                            dcc.Graph(
                                figure=style_figure(px.bar(
                                    df.groupby('Product Name')['Total Sales'].sum().sort_values(ascending=False).head(10).reset_index(),
                                    y='Product Name', x='Total Sales', orientation='h',
                                    color='Total Sales', color_continuous_scale='Bluyl'
                                ))
                            )
                        ], className="glass-card p-4 mb-4")
                    ], width=6),
                    dbc.Col([
                        html.Div([
                            html.H4("Profit vs Discount", className="text-white mb-3"),
                            dcc.Graph(
                                figure=style_figure(px.scatter(
                                    df, x='Discount', y='Profit', color='Category',
                                    size='Quantity', hover_data=['Product Name'],
                                    color_discrete_sequence=px.colors.qualitative.Vivid
                                ))
                            )
                        ], className="glass-card p-4 mb-4")
                    ], width=6),
                ])
            ]),
            
            # Tab 4: Forecasting & Advanced Analytics
            dcc.Tab(label='Forecasting & Analytics', className="custom-tab", selected_className="custom-tab--selected", children=[
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H4("Model Performance", className="text-white mb-3"),
                            dbc.Table([
                                html.Thead(html.Tr([html.Th("Model"), html.Th("RMSE"), html.Th("MAPE")])),
                                html.Tbody([
                                    html.Tr([html.Td("SARIMA"), html.Td(f"{metrics.get('SARIMA', {}).get('RMSE', 0):.2f}"), html.Td(f"{metrics.get('SARIMA', {}).get('MAPE', 0):.2%}")]),
                                    html.Tr([html.Td("Prophet"), html.Td(f"{metrics.get('Prophet', {}).get('RMSE', 0):.2f}"), html.Td(f"{metrics.get('Prophet', {}).get('MAPE', 0):.2%}")]),
                                ])
                            ], className="table table-dark table-hover table-borderless mb-0")
                        ], className="glass-card p-4 mb-4")
                    ], width=12)
                ]),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H4("Anomaly Detection", className="text-white mb-3"),
                            html.P(f"Detected {insights.get('anomalies_detected', 0)} anomalies in the dataset.", className="lead text-warning"),
                            html.P("These anomalies represent unusual sales spikes or deep discount transactions that deviate significantly from normal patterns.", className="text-muted")
                        ], className="glass-card p-4")
                    ], width=12)
                ])
            ])
        ])
    ], fluid=True)

# Main Layout with Routing
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    create_header(),
    html.Div(id='page-content'),
    create_footer()
])

# Routing Callback
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/reports':
        return get_reports_layout()
    elif pathname == '/settings':
        return get_settings_layout()
    else:
        return get_dashboard_layout()

# Dataset Loading Callback
@app.callback(
    Output("dataset-loading-output", "children"),
    Input("load-dataset-btn", "n_clicks"),
    State("dataset-url-input", "value"),
    prevent_initial_call=True
)
def load_custom_dataset(n_clicks, url):
    if not url:
        return dbc.Alert("Please enter a valid URL.", color="warning")
    
    try:
        # 1. Download Dataset
        response = requests.get(url)
        response.raise_for_status()
        
        # 2. Validate CSV
        content = response.content.decode('utf-8')
        df_new = pd.read_csv(io.StringIO(content))
        
        required_cols = ['Order Date', 'Total Sales', 'Profit', 'Category', 'Region', 'State', 'Product Name']
        missing_cols = [col for col in required_cols if col not in df_new.columns]
        
        if missing_cols:
            return dbc.Alert(f"Missing required columns: {', '.join(missing_cols)}", color="danger")
            
        # 3. Save to Raw Data
        raw_path = os.path.join(RAW_DATA_DIR, 'retail_sales_dataset.csv')
        df_new.to_csv(raw_path, index=False)
        
        # 4. Run Pipeline
        # We run these sequentially. In a production app, this should be a background task (Celery/Redis)
        run_cleaning_pipeline()
        run_feature_engineering()
        run_forecasting()
        run_advanced_analytics()
        
        # 5. Reload Global Data
        global df, metrics, insights
        df, metrics, insights = load_global_data()
        
        return dbc.Alert("Dataset loaded and analyzed successfully! Go to Dashboard to view results.", color="success")
        
    except Exception as e:
        return dbc.Alert(f"Error processing dataset: {str(e)}", color="danger")

if __name__ == '__main__':
    app.run(debug=True, port=8050)
