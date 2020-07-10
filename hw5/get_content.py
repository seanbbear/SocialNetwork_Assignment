import os
import json 
from tqdm import tqdm,trange
from udicOpenData.stopwords import *
import numpy as np


def getContent(allFileList):
    content_list = []
    for files in tqdm(allFileList):
        with open(path + files,"r",encoding='UTF-8') as f:
            jf = json.load(f)
            articles_list = jf['articles']
            for article in articles_list:
                if article['article_title']:
                    content_list.append(article['content'])
    return content_list
                    # words = jieba.cut(article['content'])
                    # for word in words:
                    #     print(word)
                    # if "韓國瑜" in article['content']:
                    #     has_han += 1
                    # else:
                    #     unhan += 1
    # print(has_han,unhan)
def content_seg(content_list):
    seg_content = []
    for content in tqdm(content_list):
        seg_content.append(list(rmsw(content)))
        # for i in list(rmsw(content)):
        #     if i in seg_content:
        #         seg_content[i] += 1
        #     else:
        #         seg_content[i] = 1
    return seg_content

if __name__ == "__main__":
    path =  "Gossiping/"
    allFileList = os.listdir(path)
    content_list = getContent(allFileList)
    seg_content = content_seg(content_list)

    # print(seg_content[0])
    np.save("seg_data",seg_content)
    # with open("data","w",encoding='UTF-8') as f:
    #     f.write(seg_content)
    