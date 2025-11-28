from dash import dcc, html
import dash_bootstrap_components as dbc
import os

def get_reports_layout():
    # Read the business insights report content
    report_path = os.path.join(os.path.dirname(__file__), '..', 'reports', 'business_insights_report.md')
    try:
        with open(report_path, 'r') as f:
            report_content = f.read()
    except:
        report_content = "Report not found. Please run the analysis pipeline first."

    return dbc.Container([
        html.H2("Business Intelligence Reports", className="text-white mb-4"),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H4("Executive Insights", className="text-white mb-3"),
                    html.Div([
                        dcc.Markdown(report_content, className="text-muted")
                    ], style={"maxHeight": "600px", "overflowY": "scroll", "paddingRight": "10px"})
                ], className="glass-card p-4 h-100")
            ], width=12, lg=8),
            
            dbc.Col([
                html.Div([
                    html.H4("Downloadable Assets", className="text-white mb-3"),
                    html.P("Access raw data and detailed analysis files.", className="text-muted mb-4"),
                    
                    dbc.ListGroup([
                        dbc.ListGroupItem([
                            html.I(className="bi bi-file-earmark-spreadsheet me-2 text-success"),
                            "Cleaned Dataset (CSV)",
                            html.Button("Download", className="btn btn-sm btn-outline-success float-end disabled")
                        ], className="bg-transparent text-white border-secondary d-flex justify-content-between align-items-center"),
                        
                        dbc.ListGroupItem([
                            html.I(className="bi bi-exclamation-triangle me-2 text-warning"),
                            "Anomalies Report (CSV)",
                            html.Button("Download", className="btn btn-sm btn-outline-warning float-end disabled")
                        ], className="bg-transparent text-white border-secondary d-flex justify-content-between align-items-center"),
                        
                        dbc.ListGroupItem([
                            html.I(className="bi bi-people me-2 text-info"),
                            "Customer Segments (CSV)",
                            html.Button("Download", className="btn btn-sm btn-outline-info float-end disabled")
                        ], className="bg-transparent text-white border-secondary d-flex justify-content-between align-items-center"),
                        
                        dbc.ListGroupItem([
                            html.I(className="bi bi-file-text me-2 text-primary"),
                            "Full PDF Report",
                            html.Button("Download", className="btn btn-sm btn-outline-primary float-end disabled")
                        ], className="bg-transparent text-white border-secondary d-flex justify-content-between align-items-center"),
                    ], flush=True),
                    
                    html.Div([
                        html.Small("* Downloads are disabled in this demo version.", className="text-muted fst-italic")
                    ], className="mt-3")
                    
                ], className="glass-card p-4")
            ], width=12, lg=4)
        ])
    ], fluid=True, className="animate-fade-in")
