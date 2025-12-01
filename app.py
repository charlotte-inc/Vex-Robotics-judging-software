import dash
from dash import Dash,html, Input, Output, callback, dash_table, ctx, dcc, State
import pandas as pd
import dash_bootstrap_components as dbc
import sqlite3
#import dash_auth

#app = Dash(__name__, use_pages=True)
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.FONT_AWESOME, dbc_css], use_pages=True,suppress_callback_exceptions=True)

# VALID_USERNAME_PASSWORD_PAIRS = {
#     'judge': 'a'
# }

# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )

app.layout = dash.page_container

if __name__ == '__main__':
    app.run(debug=True)
    #app.run()