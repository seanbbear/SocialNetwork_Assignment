from tqdm import tqdm
import json
import os

def getCommonPushdictInOneArticle(push_ids_list_in_article):
    co_push_dict_in_article = {}
    for push_id_A in push_ids_list_in_article:
        for push_id_B in push_ids_list_in_article:
            if push_id_A != push_id_B:
                sorted_name_list = sorted([push_id_A, push_id_B])
                tuple_co_psuh_ids = (sorted_name_list[0], sorted_name_list[1])
                if tuple_co_psuh_ids not in co_push_dict_in_article:
                    co_push_dict_in_article[tuple_co_psuh_ids] = 1
    return co_push_dict_in_article

def getCommonPushdict(push_ids, folder_path, files_name_list):
    print('---start counting co-push number---')
    co_push__dict = {}
    for file_name in tqdm(files_name_list, ascii=True):
        with open(folder_path+file_name, 'r', encoding='utf-8') as fp:
            json_file = json.load(fp)
        articles_list = json_file['articles']
        for article in articles_list:
            messages_list = article['messages']
            push_ids_list_in_article = []
            for message in messages_list:
                if message['push_userid'] not in push_ids_list_in_article and message['push_userid'] in push_ids and message['push_tag'] == "噓":
                    push_ids_list_in_article.append(message['push_userid'])
            co_push_dict_in_article = getCommonPushdictInOneArticle(push_ids_list_in_article)
            for key in co_push_dict_in_article.keys():
                if key in co_push__dict:
                    co_push__dict[key] += 1
                else:
                    co_push__dict[key] = 1
    print('---finished counting co-push number---')
    return co_push__dict

def getCoPushRate(push_ids, co_push_dict):
    print('---finished counting co-push rate---')
    for key in tqdm(co_push_number_dict.keys(), ascii=True):
        A_push_number = push_ids[key[0]]
        B_push_number = push_ids[key[1]]
        co_push_number_dict[key] = co_push_number_dict[key]/(A_push_number+B_push_number)
    print('---finished counting co-push rate---')
    return co_push_dict

def filterCoLowPushRate(co_push_rate_dict,boundary_of_push_rate):
    print('---start filtering out---')
    result_dict = {}
    for key in tqdm(co_push_rate_dict.keys(), ascii=True):
        if co_push_rate_dict[key] >= boundary_of_push_rate:
            result_dict[key] = co_push_rate_dict[key]
    print('---finished filtering out---')
    return result_dict

if __name__ == "__main__":
    path = './HatePolitics/'
    files_name_list = next(os.walk(path))[2]
    push_ids_json_name = 'pull_id_times.json'

    with open(push_ids_json_name, 'r', encoding='utf-8') as fp:
        push_ids = json.load(fp)
    
    co_push_number_dict = getCommonPushdict(push_ids,path,files_name_list)
    co_push_rate_dict = getCoPushRate(push_ids, co_push_number_dict)
    co_push_rate_dict = filterCoLowPushRate(co_push_rate_dict, 0.05)
    # print(co_push_rate_dict.popitem())
    # node的list
    node_list = []
    for key in push_ids.keys():
        node = {}
        node["id"] = key
        node["group"] = 1
        node_list.append(node)
    # 邊的list
    link_list = []
    for key in co_push_rate_dict.keys():
        link_dic = {}
        link_dic["source"] = key[0]
        link_dic["target"] = key[1]
        link_dic["value"] = co_push_rate_dict[key]
        link_list.append(link_dic)
    myObj = {"nodes":node_list,"links":link_list}
    with open('ptt_pull_node_edge.json', 'w', encoding='utf-8') as fp:
            json.dump(myObj,fp,ensure_ascii=False)