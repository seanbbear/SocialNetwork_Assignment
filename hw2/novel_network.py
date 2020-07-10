#coding=utf-8
import json

with open("./novel.txt","r") as f:
    all_lines = f.readlines()


name_list = ["小魚兒","花無缺","鐵心蘭","蘇櫻","燕南天","路仲遠","江楓","邀月","憐星","花月奴","荷露","鐵萍姑","杜殺","屠嬌嬌","哈哈兒","李大嘴","陰九幽","鐵戰","軒轅三光","蕭咪咪","歐陽丁","歐陽當","白開心","萬春流","慕容依","慕容雙","慕容珊珊","慕容四姑娘","慕容五姑娘","慕容六姑娘","慕容七姑娘","慕容八姑娘","慕容九","張菁","顧人玉","黑蜘蛛","江別鶴","江玉郎","魏無牙","黃牛","白山君","胡藥師","碧蛇神君","馬亦雲","白羊","獻果神君","司晨客","黑犬星","黑面君","桃花"
,"海紅珠","段三姑","神錫道長","柳玉如","馮天雨","趙全海","王一抓","黃雞大師","嘯雲居士","孫天南","邱清波"]

node_list = []
for i in range(len(name_list)):
    node = {}
    node["id"] = name_list[i]
    node["group"] = 1
    node_list.append(node)
print(node_list) #output nodes


link_list = []
for i in range(len(all_lines)):
    for j in range(len(name_list)):
        for k in range(len(name_list)):
            if name_list[j] != name_list[k] and name_list[j] in all_lines[i] and name_list[k] in all_lines[i]:
                # link = {}   
                # link["source"] = name_list[j]
                # link["target"] = name_list[k]
                if ([name_list[k],name_list[j]]) in link_list:
                    link_list.append([name_list[k],name_list[j]])
                else: 
                    link_list.append([name_list[j],name_list[k]])

# print(link_list)
link_list_count = []
for i in range(len(link_list)):
    link_dic = {}
    link_dic["source"] = link_list[i][0]
    link_dic["target"] = link_list[i][1]
    link_dic["value"] = int(link_list.count(link_list[i])/2)
    link_list_count.append(link_dic)

new_link_list = []
for i in link_list_count:
    if not i in new_link_list:
        new_link_list.append(i)
print (new_link_list) # output links
            

myObj = {"nodes":node_list,"links":new_link_list}

with open("data.json","w",encoding='UTF-8') as f:
    json.dump(myObj,f,ensure_ascii=False)