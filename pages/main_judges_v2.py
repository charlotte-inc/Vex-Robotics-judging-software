import dash
from dash import Dash, Input, Output, callback, dash_table, ctx, dcc, State, html, ALL
import pandas as pd
import dash_bootstrap_components as dbc
import sqlite3
from furl import furl
import math

from Common import sql_execute, sql_read

dash.register_page(__name__, path='/judges_v2')



def gen_table_main():
    df = sql_read(f'''select 
                  Team,
                  notebook_link,
                  Notebook_status,
                  interview_status,
                  Interview_Total,
                  Notebook_Total,
                  Grade,
                  Notebook_status_2,
                  judging_team,
                  Excellence_criteria

                  from teams
                  ''')
    df['Total']= df['Notebook_Total'] + df['Interview_Total']

    return df.reset_index(drop=False)

def gen_table_Interview(team):
    #print(team)
    df = sql_read(f'''select 
                    Team,
                    Interview_Total,
                    Interview_status,
                    I1, I2, I3,
                    I4, I5, I6,
                    I7, I8, 
                    I9, I_notes
                from teams
                WHERE team='{team}';
                ''')
    return df

def gen_table_Notebook(team):
    df = sql_read(f'''select 
                    Team,
                    Notebook_Total,
                    Notebook_status,
                    Notebook_status_2,
                    notebook_link,
                    N1, N2, N3,
                    N4, N5, N6,
                    N7, N8, N9, 
                    N10,N11,
                    N_notes
                from teams WHERE team='{team}';
                ''')
    return df
 






tab1_content =html.Div([
    dbc.Row([
        dbc.Col([html.H6('Sort by'),  dbc.RadioItems(
            options=[
                {"label": "Team number", "value": 1},
                {"label": "Notebook score", "value": 2},
                {"label": "Interview score", "value": 3},
                {"label": "Total score", "value": 4},
            ],value=1,id="s1",inline=True,
        )],className="g-0 p-3 border", width=3),

        dbc.Col([html.H6('Filter by Grade level'),  dbc.Checklist(
            options=[
                {"label": "Elementary School", "value": "Elementary School"},
                {"label": "Middle School", "value": "Middle School"},
            ],value=["Elementary School","Middle School"],id="f1",inline=True,switch=True,
        )],className="g-0 p-3 border", width=2),

        dbc.Col([html.H6('Filter by Notebook status'),  dbc.Checklist(
            options=[
                {"label": "Not submitted", "value": "Not submitted"},
                {"label": "Developing", "value": "Developing"},
                {"label": "Not marked", "value": "Not marked"},
                {"label": "In progress", "value": "In progress"},
                {"label": "Marked - Innovation", "value": "Marked - Innovation"},
                {"label": "Marked", "value": "Marked"},
            ],value=["Not submitted","Developing","Not marked","In progress","Marked","Marked - Innovation"],id="f2",inline=True,switch=True,
        )],className="g-0 p-3 border", width=3),

        dbc.Col([html.H6('Filter by Interview team'),  dbc.Checklist(
            options=[
                {"label": "Team A", "value": 'A'},
                {"label": "Team B", "value": 'B'},
                {"label": "Team C", "value": 'C'},
                {"label": "Team D", "value": 'D'},
            ],value=['A','B','C','D'],id="f3",inline=True,switch=True,
        )],className="g-0 p-3 border", width=2),

        dbc.Col([html.H6('Filter by Excellence criteria'),  dbc.Checklist(
            options=[
                {"label": "yes", "value": 'yes'},
                {"label": "no", "value": 'no'},
            ],value=['yes','no'],id="f4",inline=True,switch=True,
        )],className="g-0 p-3 border", width=2),

        ],className="g-0"),
    dbc.Row(dbc.Col('',id='cards'),className="p-3")
])

#tab2_content = html.Div('Sort by',id='test')

tab2_content =html.Div([
    html.Div(id='team_number'),
    html.Div([
                dbc.Accordion([
                        dbc.AccordionItem(
                            children =[html.Div(id="accordion-contents1", className="mt-3")],
                            title=f'Engineering Notebook',item_id="item_1",),
                        dbc.AccordionItem(
                            children =[html.Div(id="accordion-contents2", className="mt-3")],
                            title=f'Team interview',item_id="item_2",),],
                    id="accordion",start_collapsed=True,),
            ]),
])


layout = [dcc.Location(id='url', refresh=False),dcc.Interval(id='interval_j',interval=5*1000, n_intervals=0),
        dbc.Tabs([
        dbc.Tab(tab1_content, label="Teams",tab_id="tab_1"),
        dbc.Tab(tab2_content, label="Data entry",tab_id="tab_2"),
    ],id="tabs"
)]

@callback(Output("cards", "children"), 
        Input("s1", "value"),
        Input("f1", "value"),
        Input("f2", "value"),
        Input("f3", "value"),
        Input("f4", "value"),
        Input("tabs", "active_tab"),
        Input('interval_j', 'n_intervals')
        )
def Update_table(s1,f1,f2,f3,f4,tab,t):
    df_data_team =gen_table_main()
    #print(df_data_team)
    #print(s1,f1,f2,f3,tab)
    if tab =='tab_1':
        #print('-----')
        #print('judging_team before',len(df_data_team))
        if len(df_data_team[df_data_team['judging_team'].isin(f3)])!= 0:
            df_data_team = df_data_team[df_data_team['judging_team'].isin(f3)]
        #print('judging_team after',len(df_data_team))
        #print('-----')
        #print(df_data_team['Grade'].unique(),f1)
        #print('grade_level before',len(df_data_team))
        df_data_team = df_data_team[df_data_team['Grade'].isin(f1)]
        #print('grade_level after',len(df_data_team))
        #print('-----')
        #print(df_data_team['Notebook_status'].unique(),f2)
        #print('judging_team before',len(df_data_team))
        df_data_team = df_data_team[df_data_team['Notebook_status'].isin(f2)]

        df_data_team = df_data_team[df_data_team['Excellence_criteria'].isin(f4)]
        #print('judging_team after',len(df_data_team))
        #print('-----')

        if s1 == 1:
            df_data_team = df_data_team.sort_values(by=['Team'],ascending=False)
        elif s1 == 4:
            df_data_team = df_data_team.sort_values(by=['Total'],ascending=False)
        elif s1 == 2:
            df_data_team = df_data_team.sort_values(by=['Notebook_Total'],ascending=False)
        elif s1 == 3:
            df_data_team = df_data_team.sort_values(by=['Interview_Total'],ascending=False)


        # Generate list of cards
        data_team = df_data_team.values.tolist()
        cards = []
        card_grid =[]
        for y in range(len(data_team)) :
            x = data_team[y]

            Status_text_nb = x[3]
            if x[3] == "Not submitted": 
                card_color ='secondary'
                card_inverse=True
            elif x[3] == "Developing": 
                card_color ='secondary'
                card_inverse=True
            elif x[3] == "Not marked": 
                card_color ='danger'
                card_inverse=True
            elif x[3] == "In progress": 
                card_color ='warning'
                card_inverse=True
                Status_text_nb = x[3] +' - ' +x[8]
            elif x[3] == "Marked": 
                card_color ='success'
                card_inverse=True
            elif x[3] == "Marked - Innovation": 
                card_color ='success'
                card_inverse=True

            if x[3] != 'Not submitted' and x[3] != 'Developing':
                n_text = dbc.Col(html.P([f'Engineering notebook', html.Br(),Status_text_nb , html.Br(), f'{x[6]}/55'], className="card-title"))
            else:
                n_text = dbc.Col(html.P([f'Engineering notebook', html.Br(), Status_text_nb], className="card-title"))
            cards.append(dbc.Col(dbc.Card([
                    dbc.CardHeader(
                        [dbc.Row([
                        dbc.Col(html.H4(x[1], className="card-title")),
                        dbc.Col(dbc.Button("Edit", color="primary",id={"type": "card_button","team": x[1],"index": y})),
                        dbc.Col(html.H4(x[9].upper(), className="card-title")),
                        dbc.Col(html.P(x[7]))
                        ])]),
                    dbc.CardBody(
                        [dbc.Row([
                        n_text,
                        dbc.Col(html.P([f'Interview Rubric', html.Br(), x[4], html.Br(), f'{x[5]}/45'], className="card-title"))
                        ],className="g-1")]
                    )], color=card_color,inverse=card_inverse),className="g-1"))
        card_grid =dbc.Row(cards,className="row-cols-4")
        return card_grid


# Set the selected team and move to the data entry page
@callback(Output('url', 'href'),
          Output('team_number', 'children'),

          Output("tabs", "active_tab"),

          Input({"type": "card_button", "team": ALL, "index": ALL}, "n_clicks"),
          State('url', 'href'),)
def set_team(value,href):
    #print(ctx.triggered_id)
    f = furl(href)
    if ctx.triggered_id is not None:
        if value[ctx.triggered_id.index]  is not None:
            f.args['team'] =ctx.triggered_id['team']
            return f.url, ctx.triggered_id['team'],  "tab_2"
    f.args['team'] = 'na'
    return f.url, 'Please select a team',  "tab_1"   


@callback(
    Output("accordion-contents1", "children"),
    Output("accordion-contents2", "children"),
    Input("accordion", "active_item"),
    Input('url', 'href'),)
def accordion_change_item(tab,url):
    f = furl(url)
    team = f.args['team']
    #print(team)
    if team != 'na':

        if tab == 'item_1':
            notebook_d = gen_table_Notebook(team).iloc[0]
            Notebook_sliders_text = [['IDENTIFY THE PROBLEM','N1'],
                        ['BRAINSTORM, DIAGRAM, OR PROTOTYPE SOLUTIONS','N2'],
                        ['SELECT BEST SOLUTION','N3'],
                        ['BUILD AND PROGRAM THE SOLUTION','N4'],
                        ['TEST SOLUTION','N5'],
                        ['REPEAT DESIGN PROCESS','N6'],

                        ['INDEPENDENT INQUIRY','N7'],
                        ['USEABILITY AND COMPLETENESS','N8'],
                        ['ORIGINALITY & QUALITY','N9'],
                        ['ORGANIZATION / READABILITY','N10'],
                        ['RECORD OF TEAM AND PROJECT MANAGEMENT','N11']]
            
            if notebook_d['Notebook_status'] == "Not submitted":
                Notebook_b =dbc.Button('No Notebook submitted',id='button_notebook', 
                                                  color="primary",href=notebook_d['notebook_link'],external_link= 'True',
                                                  target='_blank',disabled=True,className="d-grid gap-2")
                return html.Div(Notebook_b),html.Div()
            else:
                Notebook_b =dbc.Button('Open notebook',id='button_notebook', 
                                                  color="primary",href=notebook_d['notebook_link'],external_link= 'True',
                                                  target='_blank',disabled=False,className="d-grid gap-2")               
                Notebook_sliders= [dbc.Row([
                        dbc.Col(Notebook_b),
                        dbc.Col(dbc.Checklist(
                        options=[
                            {"label": "Developing", "value": "Developing"},
                            {"label": "In progress", "value": "In progress"},
                            {"label": "Marked - Innovation", "value": "Marked - Innovation"},
                        ],value=[notebook_d['Notebook_status']],id="Notebook_Switch",inline=True,switch=True,),)
                        ])]
                for x in range(len(Notebook_sliders_text)):
                    input_b = dbc.Row([
                        dbc.Col(Notebook_sliders_text[x][0]),
                        dbc.Col(dcc.Slider(min=0, max=5, step=1, value=notebook_d[Notebook_sliders_text[x][1]], id='n_s_'+str(x+1)))])
                    Notebook_sliders.append(input_b)
                
                Notebook_sliders.append(dbc.InputGroup(
                [dbc.InputGroupText("Notes"), dbc.Input(placeholder="",id='n_s_text')],
                className="mb-3",))
            

                return html.Div(Notebook_sliders),html.Div()
        
        elif tab == 'item_2':
            Interview_d = gen_table_Interview(team).iloc[0]
            Interview_sliders_text = [['ENGINEERING DESIGN PROCESS','I1'],
                        ['GAME STRATEGIES','I2'],
                        ['ROBOT DESIGN','I3'],
                        ['ROBOT BUILD','I4'],
                        ['ROBOT PROGRAMMING','I5'],
                        ['CREATIVITY / ORIGINALITY','I6'],
                        ['TEAM AND PROJECT MANAGEMENT','I7'],
                        ['TEAMWORK, COMMUNICATION, PROFESSIONALISM','I8'],
                        ['RESPECT, COURTESY, POSITIVITY','I9']]
            print(Interview_d)
            Interview_sliders= [dbc.Row([
                    dbc.Col(dbc.Checklist(
                    options=[
                        {"label": "Missed Interview", "value": "Missed Interview"},
                    ],value=[Interview_d['interview_status']],id="Interview_Switch",inline=True,switch=True,),)
                    ])]
            for x in range(len(Interview_sliders_text)):
                input_b = dbc.Row([
                    dbc.Col(Interview_sliders_text[x][0]),
                    dbc.Col(dcc.Slider(min=0, max=5, step=1, value=Interview_d[Interview_sliders_text[x][1]], id='i_s_'+str(x+1)))])
                Interview_sliders.append(input_b)
            
            Interview_sliders.append(dbc.InputGroup(
            [dbc.InputGroupText("Notes"), dbc.Input(placeholder="",id='i_s_text')],
            className="mb-3",))


            return html.Div(),html.Div(Interview_sliders)

    return html.Div(),html.Div()

    

# Save data for Notebook data sliders
@callback(
        Input("Notebook_Switch", "value"),
        Input('n_s_1', 'value'),
        Input('n_s_2', 'value'),
        Input('n_s_3', 'value'),
        Input('n_s_4', 'value'),
        Input('n_s_5', 'value'),
        Input('n_s_6', 'value'),
        Input('n_s_7', 'value'),
        Input('n_s_8', 'value'),
        Input('n_s_9', 'value'),
        Input('n_s_10', 'value'),
        Input('n_s_11', 'value'),
        Input('n_s_text', 'value'),
        State('url', 'href'),
        prevent_initial_call=True)
def Notebook_data_entry(b1,n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,ntext,href):

    f = furl(href)
    team = f.args['team']
    t = n1 + n2 + n3 + n4 + n5 + n6 + n7 + n8 + n9 + n10 + n11

    name = ''
    if "Developing" in b1:
        status = 'Developing'
    elif "In progress" in b1:
        status = 'In progress'
        name = f.args['name']
    elif "Marked - Innovation" in b1:
        status = 'Marked - Innovation' 
    elif  t != 0:
        status = 'Marked'
    else:
        status = 'Not marked'

    sql_execute(f'''UPDATE teams  
                    SET Notebook_Total = {t},
                    Notebook_status= '{status}',
                    Notebook_status_2 = '{name}',
                    N1 = {n1},N2 = {n2},
                    N3 = {n3},N4 = {n4},
                    N5 = {n5},N6 = {n6},
                    N7 = {n7},N8 = {n8},
                    N9 = {n9},N10 = {n10},
                    N11 = {n11},
                    N_notes = '{ntext}'

                WHERE team='{team}';
                ''')
    return  

# Save data for interview data sliders
@callback(
        Input("Interview_Switch", "value"),
        Input('i_s_1', 'value'),
        Input('i_s_2', 'value'),
        Input('i_s_3', 'value'),
        Input('i_s_4', 'value'),
        Input('i_s_5', 'value'),
        Input('i_s_6', 'value'),
        Input('i_s_7', 'value'),
        Input('i_s_8', 'value'),
        Input('i_s_9', 'value'),
        Input('i_s_text', 'value'),
        State('url', 'href'),
        prevent_initial_call=True)
def Interview_data_entry(b1,n1,n2,n3,n4,n5,n6,n7,n8,n9,ntext,href):
    print('Interview_data_entry')
    f = furl(href)
    team = f.args['team']
    t = n1 + n2 + n3 + n4 + n5 + n6 + n7 + n8 + n9 

    if "Missed Interview" in b1:
        status = 'Missed Interview'
    elif  t != 0:
        status = 'Marked'
    else:
        status = 'Not marked'

    sql_execute(f'''UPDATE teams  
                    SET Interview_Total = {t},
                    interview_status = '{status}',
                    I1 = {n1},
                    I2 = {n2},
                    I3 = {n3},
                    I4 = {n4},
                    I5 = {n5},
                    I6 = {n6},
                    I7 = {n7},
                    I8 = {n8},
                    I9 = {n9},
                    I_notes = '{ntext}'
                WHERE team='{team}';
                ''')

    return    
        #return f'Engineering Notebook {t}/50'

