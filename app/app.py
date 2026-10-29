# Imported Libraries dash, html for plotly
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from layout import create_layout

# Initializing the Dash App
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY],suppress_callback_exceptions=True)

# App Layout/ Tree Components
app.layout = create_layout()

# Setting Callbacks for Interactivity
import callbacks

# Running the App
if __name__ == "__main__":
    app.run(debug=True)