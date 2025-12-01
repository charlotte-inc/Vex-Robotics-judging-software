import dash
from dash import Dash, Input, Output, callback, dash_table, ctx, dcc, State, html, clientside_callback, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import sqlite3

from Common import sql_execute, sql_read

dash.register_page(__name__, path='/display')

color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="switch_judges_room_2"),
        dbc.Switch( id="switch_judges_room_2", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="switch_judges_room_2"),
    ]
)

clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute("data-bs-theme", switchOn ? "light" : "dark");
       return window.dash_clientside.no_update
    }
    """,
    Output("switch_judges_room_2", "id"),
    Input("switch_judges_room_2", "value"),
)

def gen_table_s():
    df = sql_read('select * from Schedule')
    if len(df) == 0:
        t1 = []
        t2 = []
        t3 = []
        t4 = []
        t5 = []
        t6 = []
        return t1,t2,t3,t4,t5,t6
    else:

        df_m = pd.pivot_table(df[df['Division']=='Middle school'], values=['Team','Status'], index=['Match number','time_p','Time'],columns='Room',aggfunc='sum').reset_index()
        #print(df_m)
        df_m.columns= ['Match number','time_p','Time','s1','s2','t1','t2']
        df_m = df_m.sort_values(by=['Time'],ascending=True)


        df_e = pd.pivot_table(df[df['Division']=='Elementary school'], values=['Team','Status'], index=['Match number','time_p','Time'],columns='Room',aggfunc='sum').reset_index()
        #print(df_e)
        df_e.columns= ['Match number','time_p','Time','s1','s2','t1','t2']
        df_e = df_e.sort_values(by=['Time'],ascending=True)

        t1 = []
        t2 = []
        t3 = []
        t4 = []
        t5 = []
        t6 = []
        for x in range(3):
                x=x+1
                t1.append(df_e[df_e['time_p']==x][['Match number']])
                t2.append(df_e[df_e['time_p']==x][['s1','t1']])
                t3.append(df_e[df_e['time_p']==x][['s2','t2']])

                t4.append(df_m[df_m['time_p']==x][['Match number']])
                t5.append(df_m[df_m['time_p']==x][['s1','t1']])
                t6.append(df_m[df_m['time_p']==x][['s2','t2']])
        return t1,t2,t3,t4,t5,t6


colours = {'Done':{'bg':'#0b9620','text':'white'},
           'progress':{'bg':'#888B95','text':'white'},
           'missed':{'bg':'#ed1555','text':'white'},
           'next':{'bg':'#ffbf0f','text':'white'},
           'else':{'bg':"#2d2d2d",'text':'white'}
           }

t2_style =[
        {'if': {},'backgroundColor': colours['else']['bg'],'color': colours['else']['text']},
        {'if': {'filter_query': '{s1} contains progress','column_id': ['t1','s1']},'backgroundColor': colours['progress']['bg'],'color': colours['progress']['text']},
        {'if': {'filter_query': '{s2} contains progress','column_id': ['t2','s2']},'backgroundColor': colours['progress']['bg'],'color': colours['progress']['text']},

        {'if': {'filter_query': '{s1} contains Done','column_id': ['t1','s1']},'backgroundColor': colours['Done']['bg'],'color': colours['Done']['text']},
        {'if': {'filter_query': '{s2} contains Done','column_id': ['t2','s2']},'backgroundColor': colours['Done']['bg'],'color': colours['Done']['text']},

        {'if': {'filter_query': '{s1} contains missed','column_id': ['t1','s1']},'backgroundColor': colours['missed']['bg'],'color': colours['missed']['text']},
        {'if': {'filter_query': '{s2} contains missed','column_id': ['t2','s2']},'backgroundColor': colours['missed']['bg'],'color': colours['missed']['text']},

        {'if': {'filter_query': '{s1} contains next','column_id': ['t1','s1']},'backgroundColor': colours['next']['bg'],'color': colours['next']['text']},
        {'if': {'filter_query': '{s2} contains next','column_id': ['t2','s2']},'backgroundColor': colours['next']['bg'],'color': colours['next']['text']}]



df_t1,df_t2,df_t3,df_t4,df_t5,df_t6 = gen_table_s()


if not df_t1:
        layout =dbc.Container([html.Div(children="schedule has not been generated")])
else:
        style_cell= style_cell={'textAlign': 'center'}

        table1 = [dash_table.DataTable(df_t1[0].to_dict('records'),[{"name": i, "id": i} for i in df_t1[0].columns], id='table_s1_1',style_as_list_view=True,style_data_conditional=t2_style,style_cell=style_cell,css=[{'selector': 'tr:first-child','rule': 'display: none',},]),
                dash_table.DataTable(df_t1[1].to_dict('records'),[{"name": i, "id": i} for i in df_t1[1].columns], id='table_s1_2',style_as_list_view=True,style_data_conditional=t2_style,style_cell=style_cell,css=[{'selector': 'tr:first-child','rule': 'display: none',},]),
                dash_table.DataTable(df_t1[2].to_dict('records'),[{"name": i, "id": i} for i in df_t1[2].columns], id='table_s1_3',style_as_list_view=True,style_data_conditional=t2_style,style_cell=style_cell,css=[{'selector': 'tr:first-child','rule': 'display: none',},])]

        table2 = [dash_table.DataTable(df_t2[0].to_dict('records'),[{"name": i, "id": i} for i in df_t2[0].columns], id='table_s2_1',style_header = {'display': 'none'},style_as_list_view=True,style_data_conditional=t2_style,style_cell=style_cell,css=[{'selector': 'tr:first-child','rule': 'display: none',},]),
                dash_table.DataTable(df_t2[1].to_dict('records'),[{"name": i, "id": i} for i in df_t2[1].columns], id='table_s2_2',style_header = {'display': 'none'},style_as_list_view=True,style_data_conditional=t2_style,style_cell=style_cell,css=[{'selector': 'tr:first-child','rule': 'display: none',},]),
                dash_table.DataTable(df_t2[2].to_dict('records'),[{"name": i, "id": i} for i in df_t2[2].columns], id='table_s2_3',style_header = {'display': 'none'},style_as_list_view=True,style_data_conditional=t2_style,style_cell=style_cell,css=[{'selector': 'tr:first-child','rule': 'display: none',},])]

        table3 = [dash_table.DataTable(df_t3[0].to_dict('records'),[{"name": i, "id": i} for i in df_t3[0].columns], id='table_s3_1',style_header = {'display': 'none'},style_as_list_view=True,style_data_conditional=t2_style,style_cell=style_cell,css=[{'selector': 'tr:first-child','rule': 'display: none',},]),
                dash_table.DataTable(df_t3[1].to_dict('records'),[{"name": i, "id": i} for i in df_t3[1].columns], id='table_s3_2',style_header = {'display': 'none'},style_as_list_view=True,style_data_conditional=t2_style,style_cell=style_cell,css=[{'selector': 'tr:first-child','rule': 'display: none',},]),
                dash_table.DataTable(df_t3[2].to_dict('records'),[{"name": i, "id": i} for i in df_t3[2].columns], id='table_s3_3',style_header = {'display': 'none'},style_as_list_view=True,style_data_conditional=t2_style,style_cell=style_cell,css=[{'selector': 'tr:first-child','rule': 'display: none',},])]


        table4= [dash_table.DataTable(df_t4[0].to_dict('records'),[{"name": i, "id": i} for i in df_t4[0].columns], id='table_s4_1',style_as_list_view=True,style_data_conditional=t2_style,style_cell=style_cell,css=[{'selector': 'tr:first-child','rule': 'display: none',},]),
                dash_table.DataTable(df_t4[1].to_dict('records'),[{"name": i, "id": i} for i in df_t4[1].columns], id='table_s4_2',style_as_list_view=True,style_data_conditional=t2_style,style_cell=style_cell,css=[{'selector': 'tr:first-child','rule': 'display: none',},]),
                dash_table.DataTable(df_t4[2].to_dict('records'),[{"name": i, "id": i} for i in df_t4[2].columns], id='table_s4_3',style_as_list_view=True,style_data_conditional=t2_style,style_cell=style_cell,css=[{'selector': 'tr:first-child','rule': 'display: none',},])]

        table5 = [dash_table.DataTable(df_t5[0].to_dict('records'),[{"name": i, "id": i} for i in df_t5[0].columns], id='table_s5_1',style_header = {'display': 'none'},style_as_list_view=True,style_data_conditional=t2_style,style_cell=style_cell,css=[{'selector': 'tr:first-child','rule': 'display: none',},]),
                dash_table.DataTable(df_t5[1].to_dict('records'),[{"name": i, "id": i} for i in df_t5[1].columns], id='table_s5_2',style_header = {'display': 'none'},style_as_list_view=True,style_data_conditional=t2_style,style_cell=style_cell,css=[{'selector': 'tr:first-child','rule': 'display: none',},]),
                dash_table.DataTable(df_t5[2].to_dict('records'),[{"name": i, "id": i} for i in df_t5[2].columns], id='table_s5_3',style_header = {'display': 'none'},style_as_list_view=True,style_data_conditional=t2_style,style_cell=style_cell,css=[{'selector': 'tr:first-child','rule': 'display: none',},])]

        table6 = [dash_table.DataTable(df_t6[0].to_dict('records'),[{"name": i, "id": i} for i in df_t6[0].columns], id='table_s6_1',style_header = {'display': 'none'},style_as_list_view=True,style_data_conditional=t2_style,style_cell=style_cell,css=[{'selector': 'tr:first-child','rule': 'display: none',},]),
                dash_table.DataTable(df_t6[1].to_dict('records'),[{"name": i, "id": i} for i in df_t6[1].columns], id='table_s6_2',style_header = {'display': 'none'},style_as_list_view=True,style_data_conditional=t2_style,style_cell=style_cell,css=[{'selector': 'tr:first-child','rule': 'display: none',},]),
                dash_table.DataTable(df_t6[2].to_dict('records'),[{"name": i, "id": i} for i in df_t6[2].columns], id='table_s6_3',style_header = {'display': 'none'},style_as_list_view=True,style_data_conditional=t2_style,style_cell=style_cell,css=[{'selector': 'tr:first-child','rule': 'display: none',},])]


        style_day ={'border-style': 'solid','text-align': 'center','border-radius': '10px','background-color': '#0077C8','font-size': '20px', 'color':'#ffffff','border-color': '#2d2d2d'}
        style_day2 ={'border-style': 'solid','text-align': 'center','border-radius': '10px','background-color': '#7A41A3','font-size': '20px', 'color':'#ffffff','border-color': '#2d2d2d'}

        #7A41A3
        style_room ={'text-align': 'center', 'color':'#ffffff'}
        style_table ={  'border-top-style': 'none', 'border-right-style': 'solid', 'border-bottom-style': 'none', 'border-left-style': 'solid','text-align': 'center'} 
        style_table_1 ={  'border-top-style': 'none', 'border-right-style': 'solid', 'border-bottom-style': 'none', 'border-left-style': 'none','text-align': 'center'} 


        layout = dbc.Container([color_mode_switch,

        dbc.Row([
                dbc.Col([
                        html.Div(style=style_day,children="Elementary"),
                        html.Div(style=style_day,children="day 1 - Morning"),
                        dbc.Row([
                                dbc.Col(children=[table1[0]]),
                                dbc.Col(style=style_table,children=[table2[0]]),
                                dbc.Col(style=style_table_1,children=[table3[0]])]),
                        html.Div(style=style_day,children="day 1 - Afternoon"),
                        dbc.Row([
                                dbc.Col(children=[table1[1]]),
                                dbc.Col(style=style_table,children=[table2[1]]),
                                dbc.Col(style=style_table_1,children=[table3[1]])]),
                        html.Div(style=style_day,children="day 2 - Morning"),
                        dbc.Row([
                                dbc.Col(children=[table1[2]]),
                                dbc.Col(style=style_table,children=[table2[2]]),
                                dbc.Col(style=style_table_1,children=[table3[2]])]),
                ]),dbc.Col([
                        html.Div(style=style_day2,children="Middle school"),
                        html.Div(style=style_day2,children="day 1 - Morning"),
                        dbc.Row([
                                dbc.Col(children=[table4[0]]),
                                dbc.Col(style=style_table,children=[table5[0]]),
                                dbc.Col(style=style_table_1,children=[table6[0]])]),
                        html.Div(style=style_day2,children="day 1 - Afternoon"),
                        dbc.Row([
                                dbc.Col(children=[table4[1]]),
                                dbc.Col(style=style_table,children=[table5[1]]),
                                dbc.Col(style=style_table_1,children=[table6[1]])]),
                        html.Div(style=style_day2,children="day 2 - Morning"),
                        dbc.Row([
                                dbc.Col(children=[table4[2]]),
                                dbc.Col(style=style_table,children=[table5[2]]),
                                dbc.Col(style=style_table_1,children=[table6[2]])]),
                ])]),

        dcc.Interval(id='interval-component',interval=10*1000, n_intervals=0)
        ],fluid=True)


@callback(
    Output('table_s1_1','data'),
    Output('table_s1_2','data'),
    Output('table_s1_3','data'),
    Output('table_s2_1','data'),
    Output('table_s2_2','data'),
    Output('table_s2_3','data'),
    Output('table_s3_1','data'),
    Output('table_s3_2','data'),
    Output('table_s3_3','data'),
    Output('table_s4_1','data'),
    Output('table_s4_2','data'),
    Output('table_s4_3','data'),
    Output('table_s5_1','data'),
    Output('table_s5_2','data'),
    Output('table_s5_3','data'),
    Output('table_s6_1','data'),
    Output('table_s6_2','data'),
    Output('table_s6_3','data'),
    Input("interval-component", "n_intervals"),
          prevent_initial_call=True)
def Status_buttons(n_intervals):
    df_t1,df_t2,df_t3,df_t4,df_t5,df_t6 = gen_table_s()
    return df_t1[0].to_dict('records'),df_t1[1].to_dict('records'),df_t1[2].to_dict('records'),df_t2[0].to_dict('records'),df_t2[1].to_dict('records'),df_t2[2].to_dict('records'),df_t3[0].to_dict('records'),df_t3[1].to_dict('records'),df_t3[2].to_dict('records'),df_t4[0].to_dict('records'),df_t4[1].to_dict('records'),df_t4[2].to_dict('records'),df_t5[0].to_dict('records'),df_t5[1].to_dict('records'),df_t5[2].to_dict('records'),df_t6[0].to_dict('records'),df_t6[1].to_dict('records'),df_t6[2].to_dict('records')
