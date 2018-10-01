#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import threading
import requests
from requests import exceptions
import time

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# 形似字集
similar_word = [
    (u"哀", u"衰", u"衷"),
    (u"嗳", u"暧", u"暖"),
    (u"巴", u"巳"),
    (u"拔", u"拨"),
    (u"斑", u"班"),
    (u"人", u"入"),
    (u"一", u"-"),
    (u"二", u"="),
    (u"戋", u"践"),
]

# 中文标点集
left_punctuation = [u"【", u"{", u"《", u"（"]
right_punctuation = [u"】", u"}", u"》", u"）"]
# 英文标点集
en_punctuation = [u",", u"[", u"]", u"{", u"<", u">", u"(", u")", u";", u"、", u"；", u"，"]
left_en_punctuation = [u"[", u"{", u"<", u"("]
right_en_punctuation = [u"]", u"}", u">", u")"]

url = "https://www.baidu.com/s?wd="

def get_html(key_word):
    max_retry_time = 5
    for retry_time in range(max_retry_time):
        try:
            response = requests.get(url + key_word, headers=header)
        except exceptions.ConnectionError as e:
            if retry_time < 5:
                continue
            print("连接失败" + str(e.message))
        except exceptions.HTTPError as e:
            if retry_time < 5:
                continue
            print('http请求错误:' + str(e.message))
        else:
            if response.status_code == 200:
                write2html(response.text.encode("utf-8"))
                return response.text.encode("utf-8")

def extract_text(text):
    soup = BeautifulSoup(text, 'lxml')
    res_text = ""
    for item in soup.find_all(name="div", attrs={'class': 'c-abstract'}):
        item_text = item.text
        res_text += item_text
    return res_text

def get_count(key_word):
    """
    爬取网页，获取出现的词频
    :param key_word:
    :return:
    """
    # res_text = extract_text(get_html(key_word))
    res_text = get_html(key_word.encode("utf-8"))
    # print key_word.encode("utf-8")
    # print res_text.count(key_word.encode("utf-8"))
    return res_text.count(key_word.encode("utf-8"))

def write2html(response):
    with open("cal_sim.html", "w") as f:
        f.write(response)

def max_word(sub_tuple, left_list, right_list):
    length = len(sub_tuple)
    left_count = []
    right_count = []
    for left_word in left_list:
        left_count.append(get_count(left_word))
    for right_word in right_list:
        right_count.append(get_count(right_word))

    total_count = []
    if left_count and right_count:
        short_len = len(left_count) if len(left_count) < len(right_count) else len(right_count)
        for i in range(short_len):
            total_count.append(left_count[i]+right_count[i])
    else:
        temp_count = left_count if left_count else right_count
        for i in range(len(temp_count)):
            total_count.append(temp_count[i])

    index = total_count.index(max(total_count))
    return sub_tuple[index % length]

def run():
    print max_word((u"拨", u"拔"), [], [u"拨配备科", u"拔配备科"])
    print max_word((u"人", u"入"), [u"陈烨人",u"陈烨入"], [u"人选教", u"入选教"])
    # print max_word((u"二", u"="), [u"家二", u"家="], [u"二等", u"=等"])
# run()



# threads = []
# start = time.time()
# for i in range(10):
#     print i
#     run()
#     # t = threading.Thread(target=run)
#     # threads.append(t)
#     # if len(threads) == 5:
#     #     for thread in threads:
#     #         thread.start()
#     #     for thread in threads:
#     #         thread.join()
#     #     threads = []
#
# end = time.time()
# print end - start