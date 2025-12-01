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

target_gap_min = 14 # time for each slot
#match_time = 3.5 #min
number_of_rooms = 2

#gap_t = 10
# target_gap_min = 10
# match_time = 1 #min
# gap_t = 0

def main():


    print("\n\n\n---------------------------------------")
    #global gap_t


    #f1 = get_schedule('Middle school')
    


    def gen_one_lot(f1,d_name,room_offset):

        print("\n\n\n")
        print("------------",d_name)


        input_teams = f1.values.tolist()




        slots_main = []
        slots_main_temp = []
        team_list= [] 
        schedule = []
        schedule_teams = []

        team_list= [] 
        schedule = []

        team_list_a= [] 

    



 

        #-----------Create list for storing schedule
        for x in input_teams:
            #schedule_a.append([x[3],[x[5],x[8]],[],datetime.strptime(x[17], '%Y-%m-%d %H:%M:%S')])
            schedule.append([x[1],[x[2],x[3]],[],x[0]])
        #-----------Get list of unique teams
        for x in schedule:
            team_list_a = team_list_a + x[1]
        team_list_a=pd.unique(pd.Series(team_list_a))
        #----------- Add E for Elementary
        for x in team_list_a:
            team_list.append([x,'a'])

        #----------- work out match_time
        #print((schedule[-1][3]-schedule[-2][3]).total_seconds()/60)

        match_time = (schedule[-1][3]-schedule[-2][3]).total_seconds()/60
        print('- time ',match_time)
        # Combine schedules
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
        slots_main_temp.append([0,schedule[0][3],[],[0,0]])
        for x in range(len(schedule)):
            time1 = schedule[x][3]-slots_main_temp[-1][1]
            time1 = time1.total_seconds() / 60
            if time1 >= target_gap_min:
                slots_main_temp.append([x,schedule[x][3],[],[0,0]])



        # for a in slots_main:
            
        #     if a[1] > datetime(2024, 12, 7, 15, 0, 0) and a[1] < datetime(2024, 12, 7, 15, 30, 0):
        #         print('--------',a)
        #     else:
        #         print(a)
        for a in slots_main_temp:
            if d_name == 'Middle school':
                if not(a[1] > datetime(2024, 12, 7, 15, 0, 0) and a[1] < datetime(2024, 12, 7, 15, 30, 0)):
                    slots_main.append(a)
                else:
                    print('--------',a)
            else:
                if not(a[1] > datetime(2024, 12, 7, 15, 0, 0) and a[1] < datetime(2024, 12, 7, 15, 30, 0)):
                    slots_main.append(a)
                else:
                    print('--------',a)

        # for a in slots_main:
        #     print(a)
        result_f =[]
        target_a_f = 0
        start_time = time.time()


        end_time = 30*2


        # # ------ Manual test code
        # target_a  = match_time*3

        # result_f, gaps = main_ga(copy.deepcopy(schedule_teams),len(team_list), slots_main , 10 + target_a , target_a)





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
        
                result, gaps = main_ga(copy.deepcopy(schedule_teams),len(team_list), slots_main , 10 + target_a , target_a)
                #print("\n",gaps,result,"\n")
                if result == "na":
                    print(" - ",x," - ",target_a,"mins is not possabile")
                    loop_stop = True
                    break

                elif gaps <= 0:
                    print("   ------------------------   ",x," - ",target_a,"mins, time =",round((time.time()-start_time)/end_time*100,0),"%")
                    result_f = copy.deepcopy(result)
                    target_a_f = copy.deepcopy(target_a)
                    break
                else:
                    print(" - ",target_a,"m, gaps =",gaps,", time =",round((time.time()-start_time)/end_time*100,0),"%")

        print("\n\n",target_a_f," mins for output")
    

        df_out = pd.DataFrame(result_f, columns=['Match number','Time','Team','Division','Room'])
        df_out['Status']=''

        #print("\n",gaps)
        #print(pd.pivot_table(df_out, values=['Team'], index=['Match number','Time'],columns=['Room'],aggfunc="sum").reset_index())
        

        
        
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


        
        
        match_out = []
        for x in range(len(df_out)):
            best = [10000000,'','']
            for y in input_teams:
                a = abs((y[0] - df_out.iloc[x]['Time']).total_seconds())
                if best[0] > a:
                    best = [a,y[1],y[0]]
            match_out.append(best[1])
        df_out['Match number']=match_out




        df_out['Room'] = df_out['Room'] + 1 + room_offset
        df_out['Division'] = d_name

        print(df_out.tail(1))
        return df_out


    df_out_a = gen_one_lot(get_schedule('Middle school'),'Middle school',0)
    df_out_b = gen_one_lot(get_schedule('Elementary school'),'Elementary school',2)
    

    
    df_out = pd.concat([df_out_a,df_out_b])

    df_out = df_out.sort_values(by=['Time'],ascending=True)

    #print(df_out)


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

    #print(df_teams)
    df_teams = df_teams.drop(columns=['Room','judging_team','index'])
    df_teams = pd.merge(df_teams, df_Schedule[['Room','Team','judging_team']], how='left', on='Team')


    

    #print(df_teams)
    df_teams.to_sql(name='teams', con=conn,if_exists='replace')
    conn.close()


def main_ga(teams,rows,slots_pass,target_after,target_before):
    global slots , Team_Quantity
    Team_Quantity = rows
    slots=copy.deepcopy(slots_pass)
    schedule = []
    team_list= []
    schedule_teams = []


    # Generate schedule_teams Stores every match for each team
    for y in team_list:
        schedule_teams.append([y,[]])
    # Adds in match times for schedule_teams
    for x in range(len(schedule_teams)):
        for y in schedule:
            if  schedule_teams[x][0] in y[1]:
                schedule_teams[x][1].append([y[0],y[2]])

    # print('slots')
    # for x in range(len(slots)):
    #     print(slots[x][0],slots[x][1],len(slots[x][2]))

    for z in range(len(slots)): 
        for x in teams:
            after=[1000]
            before=[1000]
            
            for y in range(len(x[1])): 
                temp = (x[1][y][1]-slots[z][1]).total_seconds() / 60
                if temp >= 0: after.append((x[1][y][1]-slots[z][1]).total_seconds() / 60)
                else: before.append((x[1][y][1]-slots[z][1]).total_seconds() / 60 *-1)  
            if target_after < min(after) and target_before < min(before):
                slots[z][2].append(x[0])

    # print(teams[1])

    # print('slots')
    # for x in range(len(slots)):
    #     print(slots[x][0],slots[x][1],len(slots[x][2]))


    done = []
    a=0


    # Test if it is possible
    Not_possible = 0
    for x in range(len(slots)):
        a=2
        if not(a == 0 ):
            time_slot = [ele for ele in slots[x][2] if not(ele in done)]
            time_slot_a = [ele for ele in time_slot if ele[1] == 'a']
            if len(time_slot_a)-a <= -1 :
                Not_possible=Not_possible+1

    #print(time_slot)
    #print(Not_possible)
    if Not_possible > 0:
        return "na" , "na"
  
    
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

    #result_model = model.run(stop_when_reached =gap_t,no_plot =True,disable_printing =True)

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
 
    e=0


    for x in range(len(slots)):
  

        time_slot = [ele for ele in slots[x][2] if not(ele in done)]
        #time_slot_a = [ele for ele in time_slot if ele[1] == 'a']


        #print (x,'---',a,'/',Team_Quantity[0],' - ',b,'/',Team_Quantity[1],e)

        for y in [0,1]:
            #print (y,(x//3)%2)

            if a >= len(num):
                break
            else:
                if len(time_slot) == 0:
                    #print('e',end=',')
                    e = e +1
                else:
                    #print('a',end=',')
                    index = int(round(num[a]*(len(time_slot)-1),0))
                    team = time_slot[index]
                    done.append(team)
                    time_slot.remove(team)
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