from dash import dcc, html
import dash_bootstrap_components as dbc

def create_kpi_card(title, value, color="primary", icon=None):
    """Creates a premium KPI card component."""
    return html.Div([
        html.H5(title, className="kpi-title"),
        html.H3(value, className="kpi-value"),
    ], className="kpi-card glass-card mb-4 animate-fade-in")

def create_header():
    """Creates the dashboard header."""
    return dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.I(className="bi bi-graph-up-arrow text-primary", style={"fontSize": "2rem"})),
                        dbc.Col(dbc.NavbarBrand("Retail Analytics AI", className="header-title ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Dashboard", href="/", active="exact")),
                        dbc.NavItem(dbc.NavLink("Reports", href="/reports", active="exact")),
                        dbc.NavItem(dbc.NavLink("Settings", href="/settings", active="exact")),
                    ],
                    className="ms-auto",
                    navbar=True,
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ]),
        color="dark",
        dark=True,
        className="dashboard-header",
        sticky="top"
    )

def create_footer():
    """Creates the dashboard footer."""
    return html.Footer(
        dbc.Container(
            html.P([
                "© 2025 Retail Analytics System. ",
                html.Span("Powered by Agentic AI.", className="text-primary")
            ], className="text-center text-muted small"),
            className="py-4"
        ),
        className="mt-5 border-top border-secondary"
    )
