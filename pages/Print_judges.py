import dash
from dash import Dash, Input, Output, callback, dash_table, ctx, dcc, State, html, clientside_callback, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import sqlite3

from Common import sql_execute, sql_read

dash.register_page(__name__, path='/Print_judges')


def gen_table_s():
        df = sql_read('select * from Schedule')
        if len(df) == 0:
            return False, False
        else:
            df['Teams'] = df['judging_team'] + ' - '+df['Team']

            df_ms = pd.pivot_table(df[df['Division']=='Middle school'], values=['Teams'], index=['Match number','Time','time_p'],columns='Room',aggfunc='sum').reset_index()
            df_ms.columns= ['Match number','Time','time_p','room 1','room 2']
            df_ms = df_ms.sort_values(by=['Time'],ascending=True)

            df_ls = pd.pivot_table(df[df['Division']!='Middle school'], values=['Teams'], index=['Match number','Time','time_p'],columns='Room',aggfunc='sum').reset_index()
            df_ls.columns= ['Match number','Time','time_p','room 3','room 4']
            df_ls = df_ls.sort_values(by=['Time'],ascending=True)
            return df_ms, df_ls


color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="switch_Print_judges"),
        dbc.Switch( id="switch_Print_judges", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="switch_Print_judges"),
    ]
)

clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute("data-bs-theme", switchOn ? "light" : "dark");
       return window.dash_clientside.no_update
    }
    """,
    Output("switch_Print_judges", "id"),
    Input("switch_Print_judges", "value"),
)

df_ms,df_ls = gen_table_s()
if not isinstance(df_ms, pd.DataFrame):
     layout =dbc.Container([html.Div(children="schedule has not been generated")])
else:

    layout = dbc.Container([color_mode_switch,dbc.Row([
            dbc.Col([
                html.Div(children="Middle School"),
                html.Div(children="day 1 - Morning"),
                dbc.Table.from_dataframe(df_ms[df_ms['time_p']==1].drop(columns=['time_p']), striped=True, bordered=True, hover=True),
                html.Div(children="day 1 - Afternoon"),
                dbc.Table.from_dataframe(df_ms[df_ms['time_p']==2].drop(columns=['time_p']), striped=True, bordered=True, hover=True),
                html.Div(children="day 2 - Morning"),
                dbc.Table.from_dataframe(df_ms[df_ms['time_p']==3].drop(columns=['time_p']), striped=True, bordered=True, hover=True),
            ]),dbc.Col([
                html.Div(children="Elementary School"),
                html.Div(children="day 1 - Morning"),
                dbc.Table.from_dataframe(df_ls[df_ls['time_p']==1].drop(columns=['time_p']), striped=True, bordered=True, hover=True),
                html.Div(children="day 1 - Afternoon"),
                dbc.Table.from_dataframe(df_ls[df_ls['time_p']==2].drop(columns=['time_p']), striped=True, bordered=True, hover=True),
                html.Div(children="day 2 - Morning"),
                dbc.Table.from_dataframe(df_ls[df_ls['time_p']==3].drop(columns=['time_p']), striped=True, bordered=True, hover=True),
            ])])
    ],fluid=True)


