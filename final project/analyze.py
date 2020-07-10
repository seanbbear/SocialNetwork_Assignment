import os
import json 
import re
from itertools import combinations 
from tqdm import tqdm


def getContent(allFileList,application_type, lower_price,upper_price):
    price_regex = r"總價 \(未稅/含稅\)：(\d+)"
    link_list = []
    for files in allFileList:
        with open(path + files,"r",encoding='UTF-8') as f:
            jf = json.load(f)
            articles_list = jf['articles']
            for article in articles_list:
                if article['article_title']:
                    if "菜單" in article['article_title']:
                        if application_type in article["content"] or application_type in article['article_title']:
                            if filterItem(article["content"]):
                                price = re.search(price_regex, article["content"])
                                if price and  lower_price < int(price.group(1)) and int(price.group(1)) < upper_price:
                                    # print(re.search(price_regex, article["content"]).group(1))
                                    CPU, MB, RAM, VGA, PSU = filterItem(article["content"])
                                    comb = combinations([checkinList("CPU",CPU),checkinList("MB",MB),checkinList("RAM",RAM),checkinList("VGA",VGA),checkinList("PSU",PSU)],2)
                                    for i in list(comb):
                                        link_list.append([i[0],i[1]]) 
    return link_list    

def getLinkList(link_list):
    link_list_count = []
    for i in range(len(link_list)):
        link = {}
        link["source"] = link_list[i][0]
        link["target"] = link_list[i][1]
        link["value"] = int(link_list.count(link_list[i]))
        link_list_count.append(link)
    print(len(link_list_count))
    return link_list_count

def filterItem(content):
    regex_CPU = r"CPU(.*)MB"
    matches_CPU = re.findall(regex_CPU, content)

    regex_MB= r"CPU(.*)RAM"
    matches_MB = re.findall(regex_MB, content)

    regex_RAM= r"RAM(.*)VGA"
    matches_RAM = re.findall(regex_RAM, content)

    regex_VGA= r"VGA(.*)SSD"
    matches_VGA = re.findall(regex_VGA, content)

    # regex_SSD= r"SSD(.*)HDD"
    # matches_SSD = re.findall(regex_SSD, content)

    regex_PSU= r"MB(.*)CHASSIS"
    matches_PSU = re.findall(regex_PSU, content)

    
    if matches_CPU and matches_MB and matches_RAM and matches_VGA and  matches_PSU:
        return filterSpace(matches_CPU[0]),filterSpace(matches_MB[0]),filterSpace(matches_RAM[0]),filterSpace(matches_VGA[0]),filterSpace(matches_PSU[0])

def filterSpace(content):
    content = content.lower()
    content = content.replace(" ","")
    content = content.replace("-","")
    content = content.lower()
    return content

def checkinList(Itype,item):
    All_CPU = ["r93950x","amd3700x",'a89600', 'athlon', '3000g','3200g', '3400g', '3100', '3300x', '3500x', '3600', '3600x', '3700x', '73800x', '3900x',"3900", 'tr3960x', 'tr3970x', 'tr3990x', '10400', '10700k', '10900k', '9100f', '9100', '9400f', '9400', '9500', '9600kf', '9600k', '9700f', '9700', '9700kf', '9700k', '9900kf', '3500', '2200g','8400', '9900k', 'g4930', 'g5400', 'i38100', 'i38350k', 'i58500', 'e52620', 'i57640x', 'i79800x', 'i99900x', 'i99920x', 'i910920x', 'i910940x', 'w3175x']
    All_MB = ['b85g43','b150m','c6h','z370m','tuf450','maximusxihero','hairvihero','jetson', 'c246', 'x299', 'c621', 'h110', 'h310', 'b360', 'b365', 'h370', 'z390', 'z490', 'h61', 'b75m', 'h81m', 'b85m', 'a320m', 'b350m','b350', 'b450', 'x470', 'x570', 'x399', 'trx40']
    All_RAM = ['2400', '2666', '3000', '3200', '3600', '3466', '4000', '1333', '1600']
    All_VGA = ['內顯','沿用','p620','560','p2000','1060','710', '730', '1030', '1050ti', '1650s', '1650', '1660s', '1660ti', '1660', '2060s', '2060', '2070s', '2070', '2080s', '2080ti', '2080', '5700xt', '5700', '570', '580', '5500', '5600']
    All_PSU = ['300', '350', '400', '450', '500', '550', '600', '650', '700', '750', '800', '850', '900', '950', '1000', '1200', '1300', '2000', '1050']

    if Itype == "CPU":
        for i in All_CPU:
            if i in item:
                return i
        return "none"
    elif Itype == "MB":
        for i in All_MB:
            if i in item:
                return i
        return "none"
    elif Itype == "RAM":
        for i in All_RAM:
            if i in item:
                return i
        return "none"
    elif Itype == "VGA":
        for i in All_VGA:
            if i in item:
                return i
        return "none"
    elif Itype == "PSU":
        for i in All_PSU:
            if i in item:
                return i
        return "none"

def getNodeList():
    node_list = []
    All_CPU = ["r93950x","amd3700x",'a89600', 'athlon', '3000g','3200g', '3400g', '3100', '3300x', '3500x', '3600', '3600x', '3700x', '73800x', '3900x',"3900", 'tr3960x', 'tr3970x', 'tr3990x', '10400', '10700k', '10900k', '9100f', '9100', '9400f', '9400', '9500', '9600kf', '9600k', '9700f', '9700', '9700kf', '9700k', '9900kf', '3500', '2200g','8400', '9900k', 'g4930', 'g5400', 'i38100', 'i38350k', 'i58500', 'e52620', 'i57640x', 'i79800x', 'i99900x', 'i99920x', 'i910920x', 'i910940x', 'w3175x']
    All_MB = ['b85g43','b150m','c6h','z370m','tuf450','maximusxihero','hairvihero','jetson', 'c246', 'x299', 'c621', 'h110', 'h310', 'b360', 'b365', 'h370', 'z390', 'z490', 'h61', 'b75m', 'h81m', 'b85m', 'a320m', 'b350m','b350', 'b450', 'x470', 'x570', 'x399', 'trx40']
    All_RAM = ['2400', '2666', '3000', '3200', '3600', '3466', '4000', '1333', '1600']
    All_VGA = ['內顯','沿用','p620','560','p2000','1060','710', '730', '1030', '1050ti', '1650s', '1650', '1660s', '1660ti', '1660', '2060s', '2060', '2070s', '2070', '2080s', '2080ti', '2080', '5700xt', '5700', '570', '580', '5500', '5600']
    All_PSU = ['300', '350', '400', '450', '500', '550', '600', '650', '700', '750', '800', '850', '900', '950', '1000', '1200', '1300', '2000', '1050']
    facility_list = [All_CPU,All_MB,All_RAM,All_VGA,All_PSU]
    for facility in facility_list:
        for item in facility:
            node = {}
            node["id"] = item
            node["group"] = 1
            node_list.append(node)
    node = {}
    node["id"] = "none"
    node["group"] = 1
    node_list.append(node)
    return node_list



    
if __name__ == "__main__":
    boardName = "./PttData"
    folder = '/2020/'
    path = boardName + folder
    allFileList = os.listdir(path)

    application_type = "影音"
    lower_price = 35000
    upper_price = 100000
    link_list = getLinkList(getContent(allFileList,application_type,lower_price,upper_price))
    node_list = getNodeList()
    
    myObj = {"nodes":node_list,"links":link_list}   
    with open('./2020/' + application_type + str(lower_price) + '_' + str(upper_price) + ".json","w",encoding='UTF-8') as f:
        json.dump(myObj,f,ensure_ascii=False)     
 
    # print(link_list)
