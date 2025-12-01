import sqlite3
import pandas as pd


from Common import sql_execute, sql_read

#conn = sqlite3.connect(r'C:\Users\charlotte\Documents\vex robotics\Judges_display\data\Schedule.db')

df_Schedule = sql_read(f'''select *
                from Schedule
                ''')
#t_Exists = True
t_Exists = False
if t_Exists:
    
    print('Updating links in existing table')
    df_teams = sql_read(f'''select *
                    from teams
                    ''')
    df_teams = df_teams.drop(columns=['notebook_link','grade_level'])
    print(df_teams)

    Notebooks = pd.read_excel(r"C:\Users\CXC308\OneDrive - Powerco Limited\Documents\vex\Judges_display_v2\gen_data\DigitalEngineeringNotebooks.xlsx")
    Notebooks = Notebooks[['team','grade_level','notebook_link']]

    df_teams = pd.merge(df_teams, Notebooks, on="team")

    df_teams_1 =df_teams[df_teams['notebook_link']== 'none']
    df_teams_1['Notebook_status']='Not submitted'
    df_teams_2 =df_teams[df_teams['notebook_link']!= 'none']

    df_teams = pd.concat([df_teams_1, df_teams_2]).drop(columns=['index'])
    print(df_teams.columns)

    db = r'C:\Users\CXC308\OneDrive - Powerco Limited\Documents\vex\Judges_display_v2\data\Schedule.db'
    conn = sqlite3.connect(db)

    df_teams.to_sql(name='teams', con=conn,if_exists='replace')

if not t_Exists:
    print('Generating new table from scratch')
    df =df_Schedule[['Team','Room','judging_team']]
    df.columns = ['team','Room','judging_team']
    df['notebook_link'] = 'na'

    df['Notebook_status'] = 'Not marked'
    df['Notebook_status_2'] = ''

    df['interview_status'] = 'Not started'
    

    df['Interview_Total'] = 0
    df['Notebook_Total'] = 0
    df['grade_level'] = ''

    df['N1'] = 0
    df['N2'] = 0
    df['N3'] = 0
    df['N4'] = 0
    df['N5'] = 0
    df['N6'] = 0
    df['N7'] = 0
    df['N8'] = 0
    df['N9'] = 0
    df['N10'] = 0
    df['N_notes'] = ''

    df['I1'] = 0
    df['I2'] = 0
    df['I3'] = 0
    df['I4'] = 0
    df['I5'] = 0
    df['I6'] = 0
    df['I7'] = 0
    df['I8'] = 0
    df['I9'] = 0

    df['I_notes'] = ''



    db = r'C:\Users\CXC308\OneDrive - Powerco Limited\Documents\vex\Judges_display_v2\data\judging_database.db'
    conn = sqlite3.connect(db)
    print(df.columns)
    df.to_sql(name='teams', con=conn,if_exists='replace')





# df = pd.read_csv(r'C:\Users\charlotte\Documents\vex robotics\Judges_display\data\Schedule.csv')

# df =df.drop(columns=['Unnamed: 0'])

# input_list = list(df.to_numpy())
# work_list = []
# for x in input_list:
#     for y in range(3):
#         if x[2+y] != '0':
#             work_list.append([int(x[0].split(' - ')[1]),x[1],x[2+y],'Scheduled',f'{str(y+1)}'])

# c = ['Match number','Time','Team','Status','Room']

# df = pd.DataFrame(work_list, columns=c)

# df.to_sql(name='Schedule', con=conn,if_exists='replace')

                #   team,
                #   notebook_link,
                #   Notebook_status,
                #   interview_status,
                #   Interview_Total,
                #   Notebook_Total,
                #   grade_level
                #   from teams