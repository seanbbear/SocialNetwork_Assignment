import os
import json
import datetime
from datetime import date
from tqdm import tqdm
import numpy as np

def getIDlist(path):
    with open(path,"r",encoding='UTF-8')  as f:
        jf = json.load(f)
        ID_list = []
        for key in jf:
            ID_list.append(key)
        return ID_list

# 字串轉換為時間
def strTodatetime(year,datestr):
    if len(datestr) == 11:
        return datetime.datetime.strptime(year+"/"+datestr, "%Y/%m/%d %H:%M")
    # else:
    #     print(year,datestr)
    #     return datetime.datetime.strptime("2019"+"/"+"09/01 00:00", "%Y/%m/%d %H:%M")

def getIDtime(id_list,week):
    path = "./HatePolitics/"
    file_name_list = next(os.walk(path))[2]
    id_times = {}
    for i in range(len(id_list)):
        id_times[id_list[i]] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for files in tqdm(file_name_list):
        with open(path + files,"r",encoding='UTF-8') as f:
            jf = json.load(f)
            articles_list = jf['articles']
            for article in articles_list:
                for message in article["messages"]:
                    if message["push_userid"] in id_list:
                        datestr = message["push_datetime"]
                        for i in range(24):
                            s = str(i).zfill(2)
                            if (s == datestr[6:8] and datestr[:2] != "" and datestr[3:5] != ""):
                                if datestr[:2] != "01" :
                                    weekday = date(2019, int(datestr[:2]) ,int(datestr[3:5])).weekday()
                                    if weekday == week:
                                        id_times[message["push_userid"]][i] += 1
                                else  :
                                    weekday = date(2020, int(datestr[:2]) ,int(datestr[3:5])).weekday()
                                    if weekday == week:
                                        id_times[message["push_userid"]][i] += 1
                            
    return id_times
if __name__ == "__main__":
    push_id = getIDlist("./push_pull/push_id_times.json")
    pull_id = getIDlist("./push_pull/pull_id_times.json")
    # print(push_id)
    # print(len(pull_id))
    data = {}
    for key in pull_id:
        data[key] = []

    for i in range(7):
        d = getIDtime(pull_id,i)
        for key in d :
            data[key].append(d[key])
    print(data)
        
        

        

    with open('pull.json', 'w', encoding='utf-8') as fp:
            json.dump(data,fp,ensure_ascii=False)


    
    
