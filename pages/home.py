import dash
from dash import Dash, Input, Output, callback, dash_table, ctx, dcc, State, html, ALL
import pandas as pd
import dash_bootstrap_components as dbc
import sqlite3

from Common import sql_execute, sql_read

dash.register_page(__name__, path='/')

layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dbc.Input(id="input", placeholder="Enter your first name", type="text"),
    html.Div([],id="team_number_div"),
    html.Div([],id="test")
]

# @callback(Output("team_number_div", "children"), [Input("input", "value")])
# def output_text(value):
#     if value != None:
#         # button_group = dbc.ButtonGroup([
#         #     dbc.Button("Left", color="danger",id="team_number_1"),
#         #     dbc.Button("Middle", color="warning",id="team_number_2"),
#         #     dbc.Button("Right", color="success",id="team_number_3"),
#         # ])
#         # return button_group
#         children = []
#         for each in ['a','b','c','d']:
#             button_id = {
#                 "type": "button",
#                 "index": "button-{}".format(each)
#             }
#             children.append(dbc.Button('Button {}'.format(each), id=button_id))
#         return children

# @callback(Output("test", "children"), 
#             Input({"type": "button", "index": ALL}, "n_clicks"),)
# def output_team(value):
#     print(value)
#     #Output("url", "pathname", allow_duplicate=True)
#     return('aaa')

 

@callback(Output("team_number_div", "children"), 
          Input("input", "value"))
def output_text(value):
    if value != None:
        children = [dbc.Button("Judges page", href=f'/judges_v2?name={value}&team=na', color="primary", className="me-1"),
                    dbc.Button("Schedule page", href=f'/print/', color="primary", className="me-1")]

        return dbc.Row(children)
