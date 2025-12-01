import dash
from dash import Dash, Input, Output, callback, dash_table, ctx, dcc, State, html, clientside_callback, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import sqlite3
import os 

from Common import sql_execute, sql_read

#dash.register_page(__name__)
#http://127.0.0.1:8050/judges
dash.register_page(__name__, path='/judges_room')

color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="switch_judges_room"),
        dbc.Switch( id="switch_judges_room", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="switch_judges_room"),
    ]
)

clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute("data-bs-theme", switchOn ? "light" : "dark");
       return window.dash_clientside.no_update
    }
    """,
    Output("switch_judges_room", "id"),
    Input("switch_judges_room", "value"),
)

def gen_table():

    df = sql_read('select * from Schedule')
    if len(df) == 0:
        r1 = pd.DataFrame(columns=['Match number','Time'])
        r2 = pd.DataFrame(columns=['Team','Division','Status'])
        r3 = pd.DataFrame(columns=['Team','Division','Status'])
        return r1, r2, r3, r1, r2, r3
    else:
        df = df.drop(columns=['index'])


        df_ms = df[df['Division']=='Middle school']
        df_ms = pd.pivot_table(df_ms,values=['Team','Division','Status'],index=['Time','Match number'],columns='Room',aggfunc='sum',fill_value='').reset_index()
        df_ms.columns = ['Time','Match number','Division_r1','Division_r2','Status_r1','Status_r2','Team_r1','Team_r2']

        r1 = df_ms[['Match number','Time']]
        r2 = df_ms[['Team_r1','Division_r1','Status_r1']]
        r2.columns = ['Team','Division','Status']
        r3 = df_ms[['Team_r2','Division_r2','Status_r2']]
        r3.columns = ['Team','Division','Status']




        df_ls = df[df['Division']!='Middle school']
        df_ls = pd.pivot_table(df_ls,values=['Team','Division','Status'],index=['Time','Match number'],columns='Room',aggfunc='sum',fill_value='').reset_index()
        df_ls.columns = ['Time','Match number','Division_r1','Division_r2','Status_r1','Status_r2','Team_r1','Team_r2']

        r4 = df_ls[['Match number','Time']]
        r5 = df_ls[['Team_r1','Division_r1','Status_r1']]
        r5.columns = ['Team','Division','Status']
        r6 = df_ls[['Team_r2','Division_r2','Status_r2']]
        r6.columns = ['Team','Division','Status']    
        # r1 = df_ms[['Time']][df['Room']==1]
        # r2 = df[['Team','Division','Status']][df['Room']==1]
        # r3 = df[['Team','Division','Status']][df['Room']==2]

        # r4 = df_ls[['Time']][df['Room']==3]
        # r5 = df[['Team','Division','Status']][df['Room']==3]
        # r6 = df[['Team','Division','Status']][df['Room']==4]

        x=0
        for x in range(len(r1)):
            if (r2.iloc[x]['Status'] != 'missed' ) and (r2.iloc[x]['Status'] != 'Done' ) and (r2.iloc[x]['Team'] != '' ):
                break
            if (r3.iloc[x]['Status'] != 'missed' ) and (r3.iloc[x]['Status'] != 'Done' ) and (r3.iloc[x]['Team'] != '' ):
                break
        if x != 0 : x = x -1
        l =11
        r1 = r1[x:x+l]
        r2 = r2[x:x+l]
        r3 = r3[x:x+l]


        x=0
        for x in range(len(r3)):
            if (r5.iloc[x]['Status'] != 'missed' ) and (r5.iloc[x]['Status'] != 'Done' ) and (r5.iloc[x]['Team'] != '' ):
                break
            if (r6.iloc[x]['Status'] != 'missed' ) and (r6.iloc[x]['Status'] != 'Done' ) and (r6.iloc[x]['Team'] != '' ):
                break
        if x != 0 : x = x -1
        l =11
        r4 = r4[x:x+l]
        r5 = r5[x:x+l]
        r6 = r6[x:x+l]

    return r1,  r2,   r3,   r4,   r5,   r6



def Update_status(status,team):
        
        #print(team.split(' - '))
        #print(team[0][0])

        sql = f'''
        UPDATE Schedule
        SET Status = "{status}"
        WHERE Team = "{team[0][0]}";
        '''
        
        sql_execute(sql)


        if status == "In progress" and team[1][0] != 'end':
            sql = f'''
            UPDATE Schedule
            SET Status = "Up next"
            WHERE Team = "{team[1][0]}";
            '''
            sql_execute(sql)


button_group = dbc.Container([
    dbc.Row(
    [
        dbc.Col([html.Div(dbc.Button("Scheduled",id="btn_1", color="secondary"),className="d-grid gap-2 col-6 mx-auto")]),
        dbc.Col([html.Div(dbc.Button("In_progress",id="btn_2", color="warning"),className="d-grid gap-2 col-6 mx-auto")]),
        dbc.Col([html.Div(dbc.Button("Done",id="btn_3", color="success"),className="d-grid gap-2 col-6 mx-auto")]),
        dbc.Col([html.Div(dbc.Button("Missed",id="btn_4", color="danger"),className="d-grid gap-2 col-6 mx-auto")]),
    ])],fluid=True)


colours = {'Done':{'bg':'#0b9620','text':'white'},
           'progress':{'bg':'#888B95','text':'white'},
           'missed':{'bg':'#ed1555','text':'white'},
           'next':{'bg':'#ffbf0f','text':'white'},
           'else':{'bg':"#2d2d2d",'text':'white'}
           }

df_t1,df_t2,df_t3,df_t4,df_t5,df_t6  = gen_table()

l = 10
#[0:l]


table1 = dash_table.DataTable(df_t1[0:l].to_dict('records'),[{"name": i, "id": i} for i in df_t1.columns], 
    id='table_j1',style_header = {'display': 'none','backgroundColor':"#000000",'color':"#FFFFFF"},style_as_list_view=True,
    style_data_conditional=[
        {'if': {},'backgroundColor': colours['else']['bg'],'color': colours['else']['text']},
        {'if': {'filter_query': '{Status} contains progress'},'backgroundColor': colours['progress']['bg'],'color': colours['progress']['text']},
        {'if': {'filter_query': '{Status} contains Done'},'backgroundColor': colours['Done']['bg'],'color': colours['Done']['text']},
        {'if': {'filter_query': '{Status} contains missed'},'backgroundColor': colours['missed']['bg'],'color': colours['missed']['text']},
        {'if': {'filter_query': '{Status} contains next'},'backgroundColor': colours['next']['bg'],'color': colours['next']['text']},
        ])

table2 = dash_table.DataTable(df_t2[0:l].to_dict('records'),[{"name": i, "id": i} for i in df_t2.columns], 
    id='table_j2',style_header = {'display': 'none'},style_as_list_view=True,
    style_data_conditional=[
        {'if': {},'backgroundColor': colours['else']['bg'],'color': colours['else']['text']},
        {'if': {'filter_query': '{Status} contains progress'},'backgroundColor': colours['progress']['bg'],'color': colours['progress']['text']},
        {'if': {'filter_query': '{Status} contains Done'},'backgroundColor': colours['Done']['bg'],'color': colours['Done']['text']},
        {'if': {'filter_query': '{Status} contains missed'},'backgroundColor': colours['missed']['bg'],'color': colours['missed']['text']},
        {'if': {'filter_query': '{Status} contains next'},'backgroundColor': colours['next']['bg'],'color': colours['next']['text']},
        ])

table3 = dash_table.DataTable(df_t3[0:l].to_dict('records'),[{"name": i, "id": i} for i in df_t3.columns], 
    id='table_j3',style_header = {'display': 'none'},style_as_list_view=True,
    style_data_conditional=[
        {'if': {},'backgroundColor': colours['else']['bg'],'color': colours['else']['text']},
        {'if': {'filter_query': '{Status} contains progress'},'backgroundColor': colours['progress']['bg'],'color': colours['progress']['text']},
        {'if': {'filter_query': '{Status} contains Done'},'backgroundColor': colours['Done']['bg'],'color': colours['Done']['text']},
        {'if': {'filter_query': '{Status} contains missed'},'backgroundColor': colours['missed']['bg'],'color': colours['missed']['text']},
        {'if': {'filter_query': '{Status} contains next'},'backgroundColor': colours['next']['bg'],'color': colours['next']['text']},
        ])

table4 = dash_table.DataTable(df_t4[0:l].to_dict('records'),[{"name": i, "id": i} for i in df_t4.columns], 
    id='table_j4',style_header = {'display': 'none'},style_as_list_view=True,
    style_data_conditional=[
        {'if': {},'backgroundColor': colours['else']['bg'],'color': colours['else']['text']},
        {'if': {'filter_query': '{Status} contains progress'},'backgroundColor': colours['progress']['bg'],'color': colours['progress']['text']},
        {'if': {'filter_query': '{Status} contains Done'},'backgroundColor': colours['Done']['bg'],'color': colours['Done']['text']},
        {'if': {'filter_query': '{Status} contains missed'},'backgroundColor': colours['missed']['bg'],'color': colours['missed']['text']},
        {'if': {'filter_query': '{Status} contains next'},'backgroundColor': colours['next']['bg'],'color': colours['next']['text']},
        ])

table5 = dash_table.DataTable(df_t5[0:l].to_dict('records'),[{"name": i, "id": i} for i in df_t5.columns], 
    id='table_j5',style_header = {'display': 'none'},style_as_list_view=True,
    style_data_conditional=[
        {'if': {},'backgroundColor': colours['else']['bg'],'color': colours['else']['text']},
        {'if': {'filter_query': '{Status} contains progress'},'backgroundColor': colours['progress']['bg'],'color': colours['progress']['text']},
        {'if': {'filter_query': '{Status} contains Done'},'backgroundColor': colours['Done']['bg'],'color': colours['Done']['text']},
        {'if': {'filter_query': '{Status} contains missed'},'backgroundColor': colours['missed']['bg'],'color': colours['missed']['text']},
        {'if': {'filter_query': '{Status} contains next'},'backgroundColor': colours['next']['bg'],'color': colours['next']['text']},
        ])

table6 = dash_table.DataTable(df_t6[0:l].to_dict('records'),[{"name": i, "id": i} for i in df_t6.columns], 
    id='table_j6',style_header = {'display': 'none'},style_as_list_view=True,
    style_data_conditional=[
        {'if': {},'backgroundColor': colours['else']['bg'],'color': colours['else']['text']},
        {'if': {'filter_query': '{Status} contains progress'},'backgroundColor': colours['progress']['bg'],'color': colours['progress']['text']},
        {'if': {'filter_query': '{Status} contains Done'},'backgroundColor': colours['Done']['bg'],'color': colours['Done']['text']},
        {'if': {'filter_query': '{Status} contains missed'},'backgroundColor': colours['missed']['bg'],'color': colours['missed']['text']},
        {'if': {'filter_query': '{Status} contains next'},'backgroundColor': colours['next']['bg'],'color': colours['next']['text']},

        ])



style_day ={'border-style': 'solid','text-align': 'center','border-radius': '10px','background-color': '#0077C8','font-size': '20px', 'color':'#ffffff'}
style_room ={'text-align': 'center', 'color':'#ffffff'}
style_table ={  'border-top-style': 'none', 'border-right-style': 'solid', 'border-bottom-style': 'none', 'border-left-style': 'none','text-align': 'center'} 
style_table_1 ={  'border-top-style': 'none', 'border-right-style': 'none', 'border-bottom-style': 'none', 'border-left-style': 'none','text-align': 'center'}


layout = dbc.Container([color_mode_switch,
    dbc.Row(
    [
        dbc.Col(style=style_table,children=[html.Div(style=style_room,children="Match number"),table1]),
        dbc.Col(style=style_table,children=[html.Div(style=style_room,children="Room 1"),table2]),
        dbc.Col(style=style_table,children=[html.Div(style=style_room,children="Room 2"),table3]),

        dbc.Col(style=style_table,children=[html.Div(style=style_room,children="Match number"),table4]),
        dbc.Col(style=style_table,children=[html.Div(style=style_room,children="Room 2"),table5]),
        dbc.Col(style=style_table_1,children=[html.Div(style=style_room,children="Room 3"),table6])
    ]),

    dbc.Alert(style=style_room,id='tbl_out'),
    button_group,
    dcc.Store(id='Selected_team')
],fluid=True)




# layout = dbc.Container([color_mode_switch,
#     dbc.Row(
#     [
#         dbc.Col(className="dbc dbc-row-selectable",children=[html.H5("Match number"),table1]),
#         dbc.Col(className="dbc dbc-row-selectable",children=[html.H5("Room 1"),table2]),
#         dbc.Col(className="dbc dbc-row-selectable",children=[html.H5("Room 2"),table3]),

#         dbc.Col(className="dbc dbc-row-selectable",children=[html.H5("Match number"),table4]),
#         dbc.Col(className="dbc dbc-row-selectable",children=[html.H5("Room 2"),table5]),
#         dbc.Col(className="dbc dbc-row-selectable",children=[html.H5("Room 3"),table6])
#     ]),

#     dbc.Alert(className=style_room,id='tbl_out'),
#     button_group,
#     dcc.Store(id='Selected_team')
# ],fluid=True)


@callback(
    Output('table_j1','data'),
    Output('table_j2','data'),
    Output('table_j3','data'),
    Output('table_j4','data'),
    Output('table_j5','data'),
    Output('table_j6','data'),

    Output("table_j2", "active_cell"),
    Output("table_j3", "active_cell"),
    Output("table_j5", "active_cell"),
    Output("table_j6", "active_cell"),

    Output("table_j2", "selected_cells"),
    Output("table_j3", "selected_cells"),
    Output("table_j5", "selected_cells"),
    Output("table_j6", "selected_cells"),
    

    Input("btn_1", "n_clicks"),
    Input("btn_2", "n_clicks"),
    Input("btn_3", "n_clicks"),
    Input("btn_4", "n_clicks"),
    State('Selected_team','data'))
def Status_buttons(btn_1, btn_2, btn_3, btn_4,team):

    button_id = ctx.triggered_id

    if team != None:
        if button_id == "btn_1":
            Update_status("",team)

        elif button_id == "btn_2":
            Update_status("In progress",team)

        elif button_id == "btn_3":
            Update_status("Done",team)

        elif button_id == "btn_4":
            Update_status("missed",team)

    df_t1,df_t2,df_t3,df_t4,df_t5,df_t6 = gen_table()
    l = 10
    return df_t1[0:l].to_dict('records'),df_t2[0:l].to_dict('records'),df_t3[0:l].to_dict('records'),df_t4[0:l].to_dict('records'),df_t5[0:l].to_dict('records'),df_t6[0:l].to_dict('records'), None , None, None, None, [], [], [], []



@callback(
    Output("table_j1", "selected_cells"),
    Output("table_j1", "active_cell"),
    Input('table_j1', 'active_cell'),    
)
def clear(a):
    return [], None


@callback(Output('tbl_out', 'children'), 
          Output('Selected_team','data'),

          Output("table_j2", "active_cell", allow_duplicate=True),
          Output("table_j3", "active_cell", allow_duplicate=True),
          Output("table_j5", "active_cell", allow_duplicate=True),
          Output("table_j6", "active_cell", allow_duplicate=True),

          Output("table_j2", "selected_cells", allow_duplicate=True),
          Output("table_j3", "selected_cells", allow_duplicate=True),
          Output("table_j5", "selected_cells", allow_duplicate=True),
          Output("table_j6", "selected_cells", allow_duplicate=True),

          Input('table_j2', 'active_cell'),
          Input('table_j3', 'active_cell'),
          Input('table_j5', 'active_cell'),
          Input('table_j6', 'active_cell'),

          State("table_j2", "selected_cells"),
          State("table_j3", "selected_cells"),
          State("table_j5", "selected_cells"),
          State("table_j6", "selected_cells"),

          State("table_j2", "data"),
          prevent_initial_call=True)
def update_graphs(active_cell2,active_cell3,active_cell5,active_cell6  ,selected_cells2,selected_cells3,selected_cells5,selected_cells6,  data_2 ):
    graphs_id = ctx.triggered_id
    #print(graphs_id)
    df_t1,df_t2,df_t3,df_t4,df_t5,df_t6 = gen_table()


    if graphs_id == "table_j2" and active_cell2 != None:
        #print(data_2)
        out = str(df_t2.reset_index( drop = True)._get_value(active_cell2['row'], 'Team'))
        t1 = list(df_t2.reset_index( drop = True).iloc[active_cell2['row']])
        if (active_cell2['row']+1) == len(df_t2):
            t2 = 'end'
        else:
            t2 = list(df_t2.reset_index( drop = True).iloc[active_cell2['row']+1])
        return out, [t1,t2], active_cell2 , None, None, None, selected_cells2 , [], [], []

    elif graphs_id == "table_j3":
        out = str(df_t3.reset_index( drop = True)._get_value(active_cell3['row'], 'Team'))
        t1 = list(df_t3.reset_index( drop = True).iloc[active_cell3['row']])
        if (active_cell3['row']+1) == len(df_t3):
            t2 = 'end'
        else:
            t2 = list(df_t3.reset_index( drop = True).iloc[active_cell3['row']+1])
        return  out, [t1,t2], None , active_cell3, None, None, [] , selected_cells3, [], []



    elif graphs_id == "table_j5":
        out = str(df_t5.reset_index( drop = True)._get_value(active_cell5['row'], 'Team'))
        t1 = list(df_t5.reset_index( drop = True).iloc[active_cell5['row']])
        if (active_cell5['row']+1) == len(df_t5):
            t2 = 'end'
        else:
            t2 = list(df_t5.reset_index( drop = True).iloc[active_cell5['row']+1])
        return  out, [t1,t2], None , None, active_cell5, None, [] , [], selected_cells5, []
    
    elif graphs_id == "table_j6":
        out = str(df_t6.reset_index( drop = True)._get_value(active_cell6['row'], 'Team'))
        t1 = list(df_t6.reset_index( drop = True).iloc[active_cell6['row']])
        if (active_cell6['row']+1) == len(df_t6):
            t2 = 'end'
        else:
            t2 = list(df_t6.reset_index( drop = True).iloc[active_cell6['row']+1])
        return  out, [t1,t2], None , None, None, active_cell6, [] , [], [], selected_cells6   
    

    else:
        return "", None, None , None, None, None, [], [], [], []



