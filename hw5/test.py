import numpy as np
from tqdm import tqdm
data = np.load("seg_data.npy",allow_pickle=True)

def get_wordlist(data):
    print("---start getting wordlist---")
    wordlist = []
    for content in tqdm(data):
        for word in content:
            wordlist.append(word)
    return list(set(wordlist))

def chi_square(word):
    pos = 0
    neg = 0
    shitty = 0
    unshitty = 0

    pos_shitty = 0
    pos_unshitty = 0
    neg_shitty = 0
    neg_unshitty = 0
    for i in data:
        if "韓國瑜" in i:
            pos += 1
            if word in i:
                shitty += 1
                pos_shitty += 1
            else:
                unshitty += 1
                pos_unshitty += 1
        else:
            neg += 1
            if word in i:
                shitty += 1
                neg_shitty += 1
            else:
                unshitty += 1
                neg_unshitty += 1

    ex = [pos * (shitty/(shitty+unshitty)), pos * (unshitty/(shitty+unshitty)), neg * (shitty/(shitty+unshitty)), neg * (unshitty/(shitty+unshitty))]
    ob = [pos_shitty,pos_unshitty,neg_shitty,neg_unshitty]

    score = 0
    for i in range(3):
        score += ((ex[i]-ob[i]) ** 2)/ex[i]
    return word,score



if __name__ == "__main__":
    chi_score = {}
    wordlist = get_wordlist(data)
    # print(wordlist[5])
    for word in tqdm(wordlist):
        chi_score[word] = chi_square(word)
        # expect = expectation(word)
        # chi_score[word] = chi_square(expect,observe)

    np.save("chi_score_test.npy",chi_score)