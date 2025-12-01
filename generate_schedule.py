from datetime import datetime, timedelta
import pandas as pd
import copy
import numpy as np
from geneticalgorithm2 import geneticalgorithm2 as ga
import math
import random
import numpy as np
import time
from robot_events_api import *


model_done = False
current_division=1

slots = []

target_gap_min = 20
match_time = 3.5 #min
gap_t = 10

# target_gap_min = 10
# match_time = 1 #min
# gap_t = 0

def main():


    print("\n\n\n---------------------------------------")
    global gap_t

    f2 = get_schedule('Elementary school')
    f1 = get_schedule('Middle school')
    
    f1_len = len(pd.concat([f1['Blue Team 1'], f1['Red Team 1']]).unique())
    f2_len = len(pd.concat([f2['Blue Team 1'], f2['Red Team 1']]).unique())
    print(len(pd.concat([f2['Blue Team 1'], f2['Red Team 1']]).unique()))
    print(len(pd.concat([f1['Blue Team 1'], f1['Red Team 1']]).unique()))

    if f1_len > f2_len:
        input_big = f1.values.tolist()
        input_little = f2.values.tolist()
        input_big_l = 'Elementary'
        input_little_l = 'Middle School'
    else:
        input_big = f2.values.tolist()
        input_little = f1.values.tolist()
        input_little_l = 'Elementary'
        input_big_l = 'Middle School'



    slots_main = []
    team_list= [] 
    schedule = []
    schedule_teams = []

    team_list_a= [] 
    schedule_a = []

    team_list_b= [] 
    schedule_b = []

    



 
    # input_big
    #-----------Create list for storing schedule
    for x in input_big:
        #schedule_a.append([x[3],[x[5],x[8]],[],datetime.strptime(x[17], '%Y-%m-%d %H:%M:%S')])
        schedule_a.append([x[1],[x[2],x[3]],[],x[0]])
    #-----------Get list of unique teams
    for x in schedule_a:
        team_list_a = team_list_a + x[1]
    team_list_a=pd.unique(pd.Series(team_list_a))
    #----------- Add E for Elementary
    for x in team_list_a:
        team_list.append([x,'a'])


    # input_little
    #-----------Create list for storing schedule
    for x in input_little:
        #schedule_b.append([x[3],[x[5],x[8]],[],datetime.strptime(x[17], '%Y-%m-%d %H:%M:%S')])
        schedule_b.append([x[1],[x[2],x[3]],[],x[0]])
    #-----------Get list of unique teams
    for x in schedule_b:
        team_list_b = team_list_b + x[1]
    team_list_b=pd.unique(pd.Series(team_list_b))
    #----------- Add E for Elementary
    for x in team_list_b:
        team_list.append([x,'b'])



    # Combine schedules
    schedule = schedule_a +schedule_b
    for y in team_list:
        schedule_teams.append([y,[]])

    # print("\n\n\n")
    # for a in schedule:
    #      print(a)

    # Add matches to team list
    for x in range(len(schedule_teams)):
        for y in schedule:
            #print(schedule_teams[x][0][0], y[1])
            if schedule_teams[x][0][0] in y[1]:
                schedule_teams[x][1].append([y[0],y[3]])

    # print("\n\n\n")
    # for a in schedule_a:
    #      print(a)

    # Generate list of Interview times
    slots_main.append([0,schedule_a[0][3],[],[0,0,0]])
    for x in range(len(schedule_a)):
        time1 = schedule_a[x][3]-slots_main[-1][1]
        time1 = time1.total_seconds() / 60
        if time1 >= target_gap_min:
            slots_main.append([x,schedule_a[x][3],[],[0,0,0]])


    print("\n\n\n")
    for a in slots_main:
         print(a)

    

    result_f =[]
    target_a_f = 0
    start_time = time.time()
    end_time = 30*2
    gap_t = 0


    # # ------ Manual test code
    # target_a  = match_time*3

    # result, gaps = main_ga(copy.deepcopy(schedule_teams),len(team_list),len(team_list_a),len(team_list_b) , slots_main , 10 + target_a , target_a)
    # print("\n",gaps)
    # df = pd.DataFrame(result, columns=['Match number','time','team','Division','room'])
    # print(pd.pivot_table(df, values=['team'], index=['Match number','time'],columns=['room'],aggfunc="sum").reset_index())


    #aaaaaaaaaaaaaaaaaaaa

    loop_stop = False
    x=0
    while not(loop_stop):
        x += 1
        target_a  = match_time*x 
        while True:
            if (time.time()-start_time) > end_time:
                print("\nout of time")
                loop_stop = True
                break
    
            result, gaps = main_ga(copy.deepcopy(schedule_teams),len(team_list),len(team_list_a),len(team_list_b) , slots_main , 10 + target_a , target_a)
            #print("\n",gaps,result,"\n")
            if result == "na":
                print(" - ",x," - ",target_a,"mins is not possabile")
                loop_stop = True
                break

            elif gaps <= gap_t:
                print("   ------------------------   ",x," - ",target_a,"mins, time =",round((time.time()-start_time)/end_time*100,0),"%")
                result_f = copy.deepcopy(result)
                target_a_f = copy.deepcopy(target_a)
                break
            else:
                print(" - ",target_a,"m, gaps =",gaps,", time =",round((time.time()-start_time)/end_time*100,0),"%")

    print("\n\n",target_a_f," mins for output")
 

    df_out = pd.DataFrame(result_f, columns=['Match number','Time','Team','Division','Room'])
    df_out['Status']=''


    time_l = list(df_out['Time'])
    time_p = []
    a = 1
    for x in range(len(time_l)):
        if x == 0:
            time_p.append(a)
        else:
            d = (time_l[x]-time_l[x-1])
            if d > timedelta(hours = 1):
                a = a +1
            time_p.append(a)
            #print(d, d > timedelta(hours = 1))
            #if 
    df_out['time_p']=time_p

    #print('\n\nbefore')
    #print(df_out)

    # df_out_a = df_out[df_out['Division']=='a']
    # match_out = []
    # for x in range(len(df_out_a)):
    #     for y in input_big:
    #         if y[0] == df_out_a.iloc[x]['Time']:
    #             match_out.append(y[1])
    #             break
    #     else:
    #         print('eeeeeeeee')
    # df_out_a['Match number']=match_out

    # df_out_a = df_out[df_out['Division']=='a']
    # match_out = []
    # for x in range(len(df_out_a)):
    #     for y in input_big:
    #         if y[0] == df_out_a.iloc[x]['Time']:
    #             match_out.append(y[1])
    #             break
    #     else:
    #         print('eeeeeeeee')
    # df_out_a['Match number']=match_out
    print('big = ', input_big_l)
    print('little = ', input_little_l)

    df_out_a = df_out[df_out['Division']=='a']
    match_out = []
    for x in range(len(df_out_a)):
        best = [10000000,'','']
        for y in input_big:
            a = abs((y[0] - df_out_a.iloc[x]['Time']).total_seconds())
            if best[0] > a:
                 best = [a,y[1],y[0]]
        match_out.append(best[1])
    df_out_a['Match number']=match_out


    df_out_b = df_out[df_out['Division']=='b']
    match_out = []
    for x in range(len(df_out_b)):
        best = [10000000,'','']
        for y in input_little:
            #print(a)
            a = abs((y[0] - df_out_b.iloc[x]['Time']).total_seconds())
            if best[0] > a:
                 best = [a,y[1],y[0]]
        match_out.append(best[1])
    #print(len(df_out_b),match_out)
    #print(input_little)
    df_out_b['Match number']=match_out
    df_out_b['Room'] = df_out_b['Room'] + 1 
    #print('\n\nafter')
    
    #print(df_out_a)

    #print(df_out_b)


    df_out =pd.concat([df_out_a, df_out_b])
    df_out['Room'] = df_out['Room'] + 1 
    #print(df_out)

    df_out['Division']=df_out['Division'].replace(to_replace=["a", "b"],value=[input_big_l,input_little_l])
    df_out = df_out.sort_values(by=['Time'],ascending=True)
    #print(df_out.head(10))
    print(df_out)
    import sqlite3

    conn = sqlite3.connect('judging_database.db')

    df_out['judging_team'] = df_out['Room'].astype(str)

    df_out['judging_team'] = df_out['judging_team'].str.replace('1', 'A')
    df_out['judging_team'] = df_out['judging_team'].str.replace('2', 'B')
    df_out['judging_team'] = df_out['judging_team'].str.replace('3', 'C')
    df_out['judging_team'] = df_out['judging_team'].str.replace('4', 'D')
    #,'2', 'B','3', 'C','4', 'D'
    df_out.to_sql(name='Schedule', con=conn,if_exists='replace') 


    df_Schedule = pd.read_sql('select * from Schedule', conn)
    df_teams = pd.read_sql('select * from teams', conn)

    print(df_teams)
    df_teams = df_teams.drop(columns=['Room','judging_team','index'])
    df_teams = pd.merge(df_teams, df_Schedule[['Room','Team','judging_team']], how='left', on='Team')


    

    print(df_teams)
    df_teams.to_sql(name='teams', con=conn,if_exists='replace')
    conn.close()


def main_ga(teams,rows,t_a,t_b,slots_pass,target_after,target_before):
    global slots , Team_Quantity
    Team_Quantity = [t_a,t_b]
    slots=copy.deepcopy(slots_pass)
    schedule = []
    team_list= []
    schedule_teams = []

    #input = df.values.tolist()  
    # Generate schedule from import spreadsheet

    # for x in input:
    #     schedule.append([x[3],[x[5],x[6],x[8],x[9]],datetime.strptime(x[17], '%Y-%m-%d %H:%M:%S')])
    
    # #Create list of teams
    # for x in schedule:
    #     team_list=team_list+x[1]
    # team_list=pd.unique(team_list)

    # Generate schedule_teams Stores every match for each team
    for y in team_list:
        schedule_teams.append([y,[]])

    # Adds in match times for schedule_teams
    for x in range(len(schedule_teams)):
        for y in schedule:
            if  schedule_teams[x][0] in y[1]:
                schedule_teams[x][1].append([y[0],y[2]])

    #print(schedule_teams)

    #print(teams)

    #print(t_a)

    #print('target_after = ',target_after,'   target_before = ',target_before)

    for z in range(len(slots)): 
        for x in teams:
            after=[1000]
            before=[1000]
            #print(x[1])
            for y in range(len(x[1])): 
                temp = (x[1][y][1]-slots[z][1]).total_seconds() / 60
                if temp >= 0: after.append((x[1][y][1]-slots[z][1]).total_seconds() / 60)
                else: before.append((x[1][y][1]-slots[z][1]).total_seconds() / 60 *-1)  
            if target_after < min(after) and target_before < min(before):
                slots[z][2].append(x[0])


    # print('slots')
    # for x in range(len(slots)):
    #     print(slots[x][0],slots[x][1],len(slots[x][2]))



    # print('')
    # print(len(slots[0][2]))
    # print(len(slots_pass[0][2]))



    #for x in slots:
    #    if len(x[2]) == 0:
    #        return "na" , "na"
        
    # for x in slots:    
    #     if len(x[2]) == 1:
    #         print('\n\n',x,'\n\n')
    
   

    # print(rows)
    
    #import random
    
    # varbound= []
    # for x in range(rows):
    #     varbound.append(random.uniform(0, 1))
    #varbound = [[0, 1]] * rows
    #print(varbound)
    #print(rows//3)
    #print(t_a-rows//3,t_b-rows//3)
    
    # print('\n\n')

    done = []
    a=0
    b=0

    Pre_op_schedule = []
    for x in range(len(slots)):
        Pre_op_schedule.append(['','','',''])
        for y in [0,1,2]:
            if a + b >= rows:
                break
            else:
                if   not(y == 0 or (y == 1  and (x//3)%2 == 0)) and b != Team_Quantity[1]: # ---- b ----
                    Pre_op_schedule[x][y]='b'
                    a=a+1
                else:
                    Pre_op_schedule[x][y]='a'
                    b=b+1


    # for x in Pre_op_schedule:
    #     print(x)

    #aaaaaaaaaaaaaaaaaa


    # Test if it is possible
    Not_possible = 0
    for x in range(len(slots)):
        a=0
        b=0
        for y in [0,1,2]:
            if Pre_op_schedule[x][y] == 'a':a=a+1
            elif Pre_op_schedule[x][y] == 'b':b=b+1
        if not(a == 0 or b == 0):
            time_slot = [ele for ele in slots[x][2] if not(ele in done)]
            time_slot_a = [ele for ele in time_slot if ele[1] == 'a']
            time_slot_b = [ele for ele in time_slot if ele[1] == 'b']
            if len(time_slot_a)-a <= -1 or len(time_slot_b)-b <= -1:
                Not_possible=Not_possible+1

    
    if Not_possible > 0:
        #print('Not possible ' ,Not_possible)
        return "na" , "na"


    #teams_out = f1(varbound,True)
    #df = pd.DataFrame(teams_out, columns=['Match number','time','team','Division','room'])

    #print(pd.pivot_table(df, values=['team'], index=['Match number','time'],columns=['room'],aggfunc="sum").reset_index())

  
    
    #rows=len(team_list)
    varbound = [[0, 1]] * rows

    #print(rows,varbound)

    algorithm_param = {'max_num_iteration': 500,
                       'population_size': 200,
                       'mutation_probability': 0.5,
                       'mutation_discrete_probability': None,
                       'elit_ratio': 0.1,
                       'parents_portion': 0.3,
                       'crossover_type': 'shuffle',
                       'mutation_type': 'gauss_by_x',
                       'mutation_discrete_type': 'uniform_discrete',
                       'selection_type': 'stochastic',
                       'max_iteration_without_improv': 200}
    
    model = ga(function=f1, dimension=rows, variable_type='real', variable_boundaries=varbound,
               algorithm_parameters=algorithm_param)
    
    result_model = model.run(stop_when_reached =0,no_plot =True,progress_bar_stream =None,disable_printing =True)

    result_model = model.run(stop_when_reached =gap_t,no_plot =True,disable_printing =True)

    #return 1, 1
    return f1(result_model.variable, True)



def f1(num, r_team = False):    
    #print(num)
    #print(Team_Quantity)
    #print(slots[1][2])
    output = []
    done = []
    #print('\n')

    a=0
    b=0
    e=0


    for x in range(len(slots)):
  

        time_slot = [ele for ele in slots[x][2] if not(ele in done)]
        time_slot_a = [ele for ele in time_slot if ele[1] == 'a']
        time_slot_b = [ele for ele in time_slot if ele[1] == 'b']

        #print (x,'---',a,'/',Team_Quantity[0],' - ',b,'/',Team_Quantity[1],e)

        for y in [0,2,1]:
            #print (y,(x//3)%2)

            if a + b >= len(num):
                break
            else:
                if   not(y == 0 or ((y == 1  and (x//3)%2 == 0) ))and b != Team_Quantity[1] : # ---- b ----
                    
                    if len(time_slot_b) == 0:
                        #print('e',end=',')
                        e = e +1
                    else:
                        #print('b',end=',')
                        index = int(round(num[b]*(len(time_slot_b)-1),0))
                        team = time_slot_b[index]
                        done.append(team)
                        time_slot_b.remove(team)
                        output.append([slots[x][0],slots[x][1],team[0],team[1],y])
                        b = b + 1

                else : # ---- a ----
                        if y != 2:
                            if len(time_slot_a) == 0:
                                #print('e',end=',')
                                e = e +1
                            else:
                                #print('a',end=',')
                                index = int(round(num[a+Team_Quantity[1]]*(len(time_slot_a)-1),0))
                                team = time_slot_a[index]
                                done.append(team)
                                time_slot_a.remove(team)
                                output.append([slots[x][0],slots[x][1],team[0],team[1],y])
                                a = a + 1
        #print('')
 

    #print (x,'---',a,'/',Team_Quantity[0],' - ',b,'/',Team_Quantity[1],e)

    if r_team:
        return output, e
    else:
        return e



if __name__ == "__main__":
    main()