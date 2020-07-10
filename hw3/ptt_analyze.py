import os
import json 
from tqdm import tqdm 
from itertools import combinations

def getPushIdsDict(path,file_name_list,push_tag):
    print('---get push ids dict start---')
    push_ids_dict = {}
    for i in range(len(file_name_list)):
        with open(path + file_name_list[i],"r",encoding='UTF-8') as f:
            jf = json.load(f)  
            articles_list = jf['articles']
            for article in articles_list:
                messages_list = article['messages']
                push_ids_list_in_article = []
                for message in messages_list:
                    if message['push_userid'] not in push_ids_list_in_article and message['push_tag'] == push_tag:
                        push_ids_list_in_article.append(message['push_userid'])
                for push_id in push_ids_list_in_article:
                    if push_id in push_ids_dict:
                        push_ids_dict[push_id] += 1
                    else:
                        push_ids_dict[push_id] = 1
        
    print('---get push ids dict finish---')
    return push_ids_dict

def filterLowPushId(push_ids_dict, boundary_of_push_number):
    print('---start filter---')
    result_dict = {}
    for push_id in tqdm(push_ids_dict.keys()):
        if push_ids_dict[push_id] >= boundary_of_push_number:
            result_dict[push_id] = push_ids_dict[push_id]
    print('---finish filter---')
    return result_dict

if __name__ == "__main__":
    path = "./HatePolitics/"
    file_name_list = next(os.walk(path))[2]

    push_ids_dict = getPushIdsDict(path,file_name_list,"推")
    pull_ids_dict = getPushIdsDict(path,file_name_list,"噓")


    print(len(push_ids_dict))
    print(len(pull_ids_dict))
    push_ids_dict = filterLowPushId(push_ids_dict,100)
    pull_ids_dict = filterLowPushId(pull_ids_dict,100)
    print(len(push_ids_dict))
    print(len(pull_ids_dict))
    with open("push_id_times.json","w",encoding='UTF-8') as f:
        json.dump(push_ids_dict,f,ensure_ascii=False)
    with open("pull_id_times.json","w",encoding='UTF-8') as f:
        json.dump(pull_ids_dict,f,ensure_ascii=False)
