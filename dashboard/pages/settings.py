from dash import dcc, html
import dash_bootstrap_components as dbc

def get_settings_layout():
    return dbc.Container([
        html.H2("System Settings", className="text-white mb-4"),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H4("Model Configuration", className="text-white mb-3"),
                    
                    html.Label("Forecast Horizon (Days)", className="text-muted"),
                    dcc.Slider(min=30, max=365, step=30, value=90, 
                               marks={30: '30', 90: '90', 180: '180', 365: '365'},
                               className="mb-4"),
                               
                    html.Label("Confidence Interval", className="text-muted"),
                    dcc.Dropdown(
                        options=[
                            {'label': '80%', 'value': 0.8},
                            {'label': '90%', 'value': 0.9},
                            {'label': '95%', 'value': 0.95}
                        ],
                        value=0.95,
                        className="mb-4 text-dark"
                    ),
                    
                    html.Label("Seasonality Mode", className="text-muted"),
                    dbc.RadioItems(
                        options=[
                            {"label": "Additive", "value": "additive"},
                            {"label": "Multiplicative", "value": "multiplicative"},
                        ],
                        value="additive",
                        className="text-white mb-4"
                    ),
                    
                    dbc.Button("Save Configuration", color="primary", className="w-100")
                    
                ], className="glass-card p-4 h-100")
            ], width=12, md=6),
            
            dbc.Col([
                html.Div([
                    html.H4("System Preferences", className="text-white mb-3"),
                    
                    dbc.Switch(label="Dark Mode (Enabled)", value=True, className="text-white mb-3", disabled=True),
                    dbc.Switch(label="Enable Notifications", value=False, className="text-white mb-3"),
                    dbc.Switch(label="Auto-refresh Data", value=True, className="text-white mb-3"),
                    
                    html.Hr(className="border-secondary"),
                    
                    html.H5("Data Management", className="text-white mb-3"),
                    dbc.Button([html.I(className="bi bi-arrow-clockwise me-2"), "Re-run Data Pipeline"], 
                               color="warning", outline=True, className="w-100 mb-2"),
                    dbc.Button([html.I(className="bi bi-trash me-2"), "Clear Cache"], 
                               color="danger", outline=True, className="w-100")
                    
                ], className="glass-card p-4 h-100")
            ], width=12, md=6),
        ]),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H4("Custom Dataset Integration", className="text-white mb-3"),
                    html.P("Analyze your own retail data by providing a direct CSV URL.", className="text-muted"),
                    
                    dbc.InputGroup([
                        dbc.InputGroupText(html.I(className="bi bi-link-45deg")),
                        dbc.Input(id="dataset-url-input", placeholder="https://example.com/my-retail-data.csv", type="url"),
                    ], className="mb-3"),
                    
                    dbc.Button([html.I(className="bi bi-cloud-download me-2"), "Load & Analyze Dataset"], 
                               id="load-dataset-btn", color="success", className="w-100"),
                    
                    html.Div(id="dataset-loading-output", className="mt-3")
                    
                ], className="glass-card p-4 mt-4")
            ], width=12)
        ])
    ], fluid=True, className="animate-fade-in")
