# Input component → callback function → Output component

from dash import Output, Input, State, html, dcc
import dash_bootstrap_components as dbc
import os
import requests
from app import app

# localhost be placed in .env file for production deployment
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8001/predict")

@app.callback(
    [Output("output-image-upload", "children"),
     Output("telemetry-output", "children")],
    [Input("upload-image", "contents")],
    [State("upload-image", "filename")]
)
def fetch_edge_inpection(contents, filename):
    if contents is None:
        return (
            [html.Span("Awaiting Image Feed...", className="text-muted font-italic")],
            [html.Small("System Status: Standby | Latency: -- ms", className="text-secondary")]
        )
    
    try:
        # Send base64 image data via HTTP POST to FastAPI microservice
        response = requests.post(FASTAPI_URL, json={"image_base64": contents}, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            is_pass = result["is_pass"]
            score = result["anomaly_score"]
            latency = result["latency_ms"]
            hardware = result["hardware"]
            runtime = result["runtime"]
        else:
            raise Exception("Model server returned an error.")
            
    except requests.exceptions.ConnectionError:
        # Fallback if FastAPI server isn't running yet
        is_pass, score, latency, hardware, runtime = False, 0.0, "--", "Offline", "N/A"

    # Render UI feedback elements
    if is_pass:
        status_banner = dbc.Alert("✅ STATUS: PASS (OK)", color="success", className="mb-2 font-weight-bold py-1 w-100 text-center")
    else:
        status_banner = dbc.Alert("❌ STATUS: REJECT (NG)", color="danger", className="mb-2 font-weight-bold py-1 w-100 text-center")

    img_display = html.Img(src=contents, style={"maxHeight": "180px", "maxWidth": "100%", "borderRadius": "5px"})

    viewport_content = [status_banner, img_display]

    telemetry_content = html.Div([
        html.Div([
            html.Span(f"File: {filename} ", className="font-weight-bold text-dark"),
            html.Span(f"| Anomaly Score: {score}", className="text-muted")
        ], className="mb-1"),
        html.Small(f"Hardware: {hardware} | Runtime: {runtime} | Latency: {latency} ms", className="text-secondary")
    ])

    return viewport_content, telemetry_content



@app.callback(
    Output("tab-content", "children"),
    Input("card-tabs", "active_tab")
)
def render_tab_content(active_tab):
    # ==========================================
    # TAB 1: SINGLE INSPECTION (Default View)
    # ==========================================
    if active_tab == "summary-tab":
        return dbc.Row([
            # Left Column: Conveyor Simulation / Upload Box
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Conveyor Simulation", className="card-title text-dark mb-2"),
                        html.P("Upload part image to query FastAPI model service.", className="text-muted small mb-4"),
                        
                        dcc.Upload(
                            id="upload-image",
                            children=html.Div([
                                html.I(className="bi bi-cloud-arrow-up display-4 text-primary mb-2"),
                                html.Br(),
                                "Drag and Drop or ",
                                html.A("Select an Image", className="text-primary font-weight-bold")
                            ]),
                            style={
                                "width": "100%", "height": "220px", "lineHeight": "60px",
                                "borderWidth": "2px", "borderStyle": "dashed", "borderColor": "#cbd5e1",
                                "borderRadius": "10px", "textAlign": "center", "backgroundColor": "#f8fafc",
                                "cursor": "pointer", "display": "flex", "alignItems": "center", "justifyContent": "center",
                                "flexDirection": "column"
                            },
                            multiple=False
                        )
                    ])
                ], className="shadow-sm border-0 h-100")
            ], width=12, lg=5, className="mb-4 mb-lg-0"),

            # Right Column: Inspection Viewport & Telemetry
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Inspection Viewport", className="card-title text-dark mb-3"),
                        
                        html.Div(
                            id="output-image-upload",
                            className="border rounded p-3 text-center bg-light d-flex align-items-center justify-content-center flex-column",
                            style={"minHeight": "180px", "backgroundColor": "#f8fafc !important"},
                            children=[html.Span("Awaiting Image Feed...", className="text-muted font-italic")]
                        ),
                        
                        html.Div(
                            id="telemetry-output", 
                            className="mt-3 p-3 bg-white rounded border",
                            children=[html.Small("System Status: Standby | Latency: -- ms", className="text-secondary")]
                        )
                    ])
                ], className="shadow-sm border-0 h-100")
            ], width=12, lg=7)
        ], className="g-4")

    # ==========================================
    # TAB 2: LIVE LINE INSPECTION
    # ==========================================
    elif active_tab == "details-tab":
        return html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Live Factory Conveyor Stream", className="card-title text-dark mb-2"),
                    html.P("Real-time telemetry and automated frame grabs from plant floor cameras.", className="text-muted mb-4"),
                    dbc.Alert("Live camera feed streaming service is currently offline.", color="warning", className="mb-0")
                ])
            ], className="shadow-sm border-0")
        ], className="mt-2")

    # ==========================================
    # TAB 3: AUDIT LOGS / MANUAL CHECK
    # ==========================================
    elif active_tab == "settings-tab":
        return html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Manual Operator Quality Audit Logs", className="card-title text-dark mb-2"),
                    html.P("Review historical anomaly logs, manual overrides, and inspection records.", className="text-muted mb-4"),
                    dbc.Button("Export Inspection Log (CSV)", color="secondary", size="sm")
                ])
            ], className="shadow-sm border-0")
        ], className="mt-2")
    
    return html.P("Select a valid tab.")