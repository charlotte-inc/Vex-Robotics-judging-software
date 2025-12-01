import json
import pandas as pd 
import requests
from dateutil import parser
from datetime import datetime, timedelta


token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiNTg4OGFiMTVhOWIzZjk4MjM4NmIwNjA5M2M5MzQ0ZWEwMDVlNGI2OTcwYjU5ZjBkYjdkMTMyMzcwNGYwOGJjZTgxNzY2NjljZjkxYzk5NGEiLCJpYXQiOjE3MzM1NTMxMDEuNzA0NTkxLCJuYmYiOjE3MzM1NTMxMDEuNzA0NTkzOSwiZXhwIjoyNjgwMjM3OTAxLjY5NTE1NjEsInN1YiI6IjExNjA1OSIsInNjb3BlcyI6W119.S7U4y2C5cpZfBr81JtEE8r9dAF7jAWYvw3JScGhgn3A_-iKjczJg1PshspZf9xk165Ax36H696t2y4KLfT1M_3EZ0Q0ndWRhcM9b6LLZ7I6NqUguUQDzlgIq7ljkiCOQ6SB2r7Sq6JvKJliho-yfI_Wmhio798kwQ8CvuZaJr7jlK36Eyju7M3vv4eJv7R6FZ8wU_TawBxkLOjstV3ToSp60TXeiCd4x2NsoYsWFw0LY0_gbfMsiybrnoZwHMdikdaUtQLs-IRUOJ1LBGrB_n0Yd_yJmnpIrqvC3Nsoy5yJEJH1e7HYLo_BcOxtKoUumxnKd1i8YTlF6DhuBOJUNqbuQ91cJkehqdGFium5J7jVXaQ8KGVrCcZ-YFY4GrrMyKQb4-JNZdZaOlnBKc-Q44sCLr6Xds_rxd8XQ_FlasdUNBySyrJh7DKncT7-majcMhez_7-Bq2juBXv6JlLijoHpgnh0Ci_6zuVo-W03WOvMl8z7zsTtULPv5DiAAlRVVx34kUHUQP8AGLTim7qdcxqcegidyMmkmpziK2CaT-DEz8Vvw_ytMOE5aYK59K_g1R84GSkN4Sny4e3VLN2QV5Px8LKKosG5JEXy9_jUP764ZIfju-dG_dizxKbRjIVPiozWnx8_TxpcMzY6lMElsnhFy3lXGpf0IKFHy7LsMR5U'
headers = {"Authorization": f"Bearer {token}"}


def get_schedule(Division):   
    if Division == 'Middle school':
        response_q = requests.get("https://www.robotevents.com/api/v2/events/56495/divisions/1/matches?&per_page=250", headers=headers)
    else:
        response_q = requests.get("https://www.robotevents.com/api/v2/events/56493/divisions/1/matches?&per_page=250", headers=headers)

    data_q =response_q.json()

    q_list = []
    for x in data_q['data']:
        #print(x['round'],x['matchnum'],x['scheduled'],x['name'],'\n',x['alliances'][0]['score'],'\n',x['alliances'][1])
        if x['round'] != 15:
            #q_list.append([x['round'],x['matchnum'],x['scheduled'],x['name'],x['alliances'][0]['teams'][0]['team']['name'],x['alliances'][1]['teams'][0]['team']['name']])
            if x['round'] == 0:
                type_M = 'Practice'
            else:
                type_M = 'TeamWork'

            q_list.append([x['scheduled'],
                           x['name'],
                           x['alliances'][0]['teams'][0]['team']['name'],
                           x['alliances'][1]['teams'][0]['team']['name'],
                           x['alliances'][0]['score'],
                           x['alliances'][1]['score'],
                           type_M                         
                           ])

    df=pd.DataFrame(q_list,columns =['Datetime','match','Red Team 1','Blue Team 1','Red Score','Blue Score','Match_type'])
    df['Datetime'] = df['Datetime'].apply(lambda x: parser.parse(x).replace(tzinfo=None)+ timedelta(hours=18))

    return df




def get_team_list(Division):   
    if Division == 'Middle school':
        response_q = requests.get("https://www.robotevents.com/api/v2/events/56495/teams?&per_page=250&page=1", headers=headers)
    else:
        response_q = requests.get("https://www.robotevents.com/api/v2/events/56493/teams?&per_page=250&page=1", headers=headers)
    data_q =response_q.json()

    q_list = []
    for x in data_q['data']:
        #print(x)
        q_list.append([x['number'],
                    x['team_name'],   
                    x['grade'],   
                    ])
            #print(x['round'],x['matchnum'])
    df=pd.DataFrame(q_list,columns =['Team','Team_name','Grade'])
    return df



