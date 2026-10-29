from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout():
    return dbc.Container([
        
        # ==========================================
        # 1. TOP HEADER & NAVIGATION BAR
        # ==========================================
        dbc.Row([
            # App Title
            dbc.Col([
                html.H2("Vision Inspector", className="font-weight-bold text-dark mb-0")
            ], width=12, md=4, className="d-flex align-items-center mb-3 mb-md-0"),
            
            # Navigation Tabs aligned to the right
            dbc.Col([
                dbc.Tabs([
                    dbc.Tab(label="Single Inspection", tab_id="summary-tab"),
                    dbc.Tab(label="Live Line", tab_id="details-tab"),
                    dbc.Tab(label="Audit Logs", tab_id="settings-tab")
                ], id="card-tabs", active_tab="summary-tab", className="nav-pills justify-content-md-end")
            ], width=12, md=8)
        ], className="align-items-center py-3 border-bottom mb-4 bg-white px-3 rounded shadow-sm"),

        # ==========================================
        # 2. DYNAMIC CONTENT CONTAINER (Must be empty initially!)
        # ==========================================
        html.Div(id="tab-content")

    ], fluid=True, className="px-4 py-3 bg-light min-vh-100")