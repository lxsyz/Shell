#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import hashlib
from urllib import quote_plus
import requests
import time
import random
import base64
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import traceback
import cv2
import json
import threading
import time

import calc_sim

APP_KEY = "nYZrywHmCICcwzEr"
APP_ID = "2108392408"
URL = "https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr"
# URL = "https://api.ai.qq.com/fcgi-bin/ocr/ocr_handwritingocr"

# def draw_text(text_list, target_file):
#     """
#     绘制文本在画布上
#     Args:
#         text_list: list, 文本属性列表
#         target_file: str, 存储的目标文件
#     Returns:
#         None
#     """
#     # 生成白色绘图画布
#     array = np.ndarray((1288, 797, 3), np.uint8)
#
#     array[:, :, 0] = 255
#     array[:, :, 1] = 255
#     array[:, :, 2] = 255
#
#     image = Image.fromarray(array)
#
#     # 创建绘制对象
#     draw = ImageDraw.Draw(image)
#
#     # 设置宋体
#     font = ImageFont.truetype("C:\Windows\Fonts\simsun.ttc", 14)  # 设置字体
#
#     for res in text_list:
#         draw.text((res[1], res[2]), res[0], (0, 0, 0), font)
#
#     image.save(target_file)

def get_req_sign(params, app_key):
    """
    根据 接口请求参数 和 应用密钥 计算 请求签名
    Returns:
        签名结果
    """
    params = sorted(params.items())
    parse_str = ''
    for item in params:
        if item[1]:
            parse_str += item[0] + '=' + quote_plus(item[1]) + '&'
    parse_str = parse_str + 'app_key=' + app_key

    sign = hashlib.md5(parse_str.encode('utf-8')).hexdigest().upper()
    return sign

def do_http_post(params):
    retry_time = 0
    while retry_time < 3:
        try:
            response = requests.post(url=URL, data=params, headers={'Content-Type': 'application/x-www-form-urlencoded',})
            if response.status_code == 200:
                return response.text
            else:
                print("status_code: " + response.status_code)
                return None
        except Exception as e:
            if retry_time < 3:
                retry_time += 1
                continue
            traceback.print_exc()
        # print(response.status_code)
        # print e.message

def write2file(res, target_filename):
    with open("ocr_result/" + target_filename + ".txt", 'w') as f:
        f.write(res.encode("utf-8"))

def write2html(res, fold_name, target_filename):
    with open(fold_name + '/' + target_filename + ".html", 'w') as f:
        f.write(res.encode("utf-8"))

def write2test(res, target_filename):
    with open("test/" + target_filename + ".html", 'a') as f:
        f.write(res.encode("utf-8"))

def process_result(response, target_file_name):
    html_str = "<html><body>"
    result = json.loads(response)
    print result
    if result['data']:
        item_list = result['data']['item_list']
        res = ""

        last_y = -6

        for item in item_list:
            # itemstring = item['itemstring']
            words = item['words']
            itemcoord = item['itemcoord']
            y = itemcoord[0]['y']
            if abs(y - last_y) > 5:
                if last_y >= 0:
                    html_str += "</p><p>"
                else:
                    html_str += "<p>"
            last_y = y

            for character in words:
                res += character['character']
                confidence = character['confidence']
                output_str = int(confidence * 100 // 10 * 10)
                if output_str >= 90:
                    html_str += character['character']
                elif output_str >= 80:
                    html_str += "<font color='gray'>" + character['character'] + "</font>"
                elif output_str >= 70:
                    html_str += "<font color='green'>" + character['character'] + "</font>"
                elif output_str >= 60:
                    html_str += "<font color='blue'>" + character['character'] + "</font>"
                else:
                    html_str += "<font color='red'>" + character['character'] + "</font>"
                # print(output_str)
                # res += ">" + str(output_str)
            # res += itemstring
            # res += '\n'
            # html_str += "</p>"
        html_str += "</body></html>"
        write2test(html_str, target_file_name)

def process_html_result(response, fold_name, target_filename):
    html_str = "<html><body>"
    result = json.loads(response)
    if result['data']:
        item_list = result['data']['item_list']
        res = ""

        last_y = -6

        for item in item_list:
            # itemstring = item['itemstring']
            words = item['words']
            itemcoord = item['itemcoord']
            y = itemcoord[0]['y']
            if abs(y - last_y) > 5:
                if last_y >= 0:
                    html_str += "</p><p>"
                else:
                    html_str += "<p>"
            last_y = y

            for character in words:
                res += character['character']
                confidence = character['confidence']
                output_str = int(confidence * 100 // 10 * 10)
                if output_str >= 90:
                    html_str += character['character']
                elif output_str >= 80:
                    html_str += "<font color='gray'>" + character['character'] + "</font>"
                elif output_str >= 70:
                    html_str += "<font color='green'>" + character['character'] + "</font>"
                elif output_str >= 60:
                    html_str += "<font color='blue'>" + character['character'] + "</font>"
                else:
                    html_str += "<font color='red'>" + character['character'] + "</font>"
        html_str += "</body></html>"
        write2html(html_str, fold_name, target_filename)

def get_image_content(path):
    with open(path, 'rb') as f:
        image = f.read()
    return base64.b64encode(image)

def is_similar_word(word):
    """
    判断是不是形近字
    :return: Tuple/None, 形近字元组
    """
    for sub_tuple in calc_sim.similar_word:
        if word in sub_tuple:
            return sub_tuple
    return None

def fix_similar_word(words, index, sub_tuple):
    # 与右边的字的组合
    right_combine = []
    left_combine = []
    windows = 1

    for k in range(index + 1, index + windows + 1):
        if k < len(words):
            if words[k]['character'] not in calc_sim.en_punctuation:
                for sub in sub_tuple:
                    if words[k]['character']:
                        diff = k - index
                        if diff == 1:
                            sub += words[k]['character']
                            right_combine.append(sub)
                        elif diff == 2:
                            for i in range(1, diff+1):
                                sub += words[index + i]['character']
                            right_combine.append(sub)
            else:
                break

    for k in range(index - windows, index):
         if k >= 0:
            if words[k]['character'] not in calc_sim.en_punctuation:
                for sub in sub_tuple:
                    if words[k]['character']:
                        diff = index - k
                        if diff == 1:
                            left_combine.append(words[k]['character'] + sub)
                        elif diff == 2:
                            temp = ""
                            for i in range(diff, 0, -1):
                                temp += words[index - i]['character']
                            left_combine.append(temp + sub)
            else:
                break

    # 有上下文的情况下
    if left_combine or right_combine:
        temp_word = calc_sim.max_word(sub_tuple, left_combine, right_combine)
        print temp_word
        return temp_word, False
    return None, True

def is_left_punctuation(character):
    return character in calc_sim.left_en_punctuation

def is_right_punctuation(character):
    return character in calc_sim.right_en_punctuation

def fix_puncuation(words, index, direction):
    if direction == "left":
        index += 1
        while index < len(words):
            character = words[index]
            char_str = character['character']
            output_str = int(character['confidence'] * 100 // 10 * 10)
            if char_str in calc_sim.right_en_punctuation and output_str >= 90:
                pos = calc_sim.right_en_punctuation.index(char_str)
                left_punc = calc_sim.left_en_punctuation[pos]

                print "-------" + left_punc
                return left_punc, False
            index += 1
    elif direction == "right":
        index -= 1
        while index >= 0:
            character = words[index]
            char_str = character['character']
            output_str = int(character['confidence'] * 100 // 10 * 10)
            if char_str in calc_sim.left_en_punctuation and output_str >= 90:
                pos = calc_sim.left_en_punctuation.index(char_str)
                right_punc = calc_sim.right_en_punctuation[pos]
                return right_punc, False
            index -= 1
    return None, True

def process_html_result2(response, fold_name, target_filename):
    html_str = "<html><body>"
    result = json.loads(response)
    if result['data']:
        item_list = result['data']['item_list']
        last_y = -6

        for item in item_list:
            # itemstring = item['itemstring']
            words = item['words']
            itemcoord = item['itemcoord']
            y = itemcoord[0]['y']
            if abs(y - last_y) > 5:
                if last_y >= 0:
                    html_str += "</p><p>"
                else:
                    html_str += "<p>"
            last_y = y

            for index in range(len(words)):
                character = words[index]
                char_str = character['character']
                confidence = character['confidence']
                output_str = int(confidence * 100 // 10 * 10)
                # 如果该字符是形近字，就要计算下概率大的情况
                sub_tuple = is_similar_word(char_str)
                flag = True
                temp_word = ""
                if sub_tuple and output_str < 90 and output_str >= 70:
                    temp_word, flag = fix_similar_word(words, index, sub_tuple)

                # 如果该字是标点符号
                if is_left_punctuation(char_str) and output_str < 90 and output_str >= 70:
                    temp_word, flag = fix_puncuation(words, index, "left")
                elif is_right_punctuation(char_str) and output_str < 90 and output_str >= 70:
                    temp_word, flag = fix_puncuation(words, index, "right")

                if flag:
                    if output_str >= 90:
                        html_str += character['character']
                    elif output_str >= 80:
                        html_str += "<font color='gray'>" + character['character'] + "</font>"
                    elif output_str >= 70:
                        html_str += "<font color='green'>" + character['character'] + "</font>"
                    elif output_str >= 60:
                        html_str += "<font color='blue'>" + character['character'] + "</font>"
                    else:
                        html_str += "<font color='red'>" + character['character'] + "</font>"
                else:
                    html_str += "<font color='deeppink'>" + temp_word + "</font>"
                # html_str += "[" + str(round(confidence, 2)) + "]"
            # print "---------------- one row -----------------------"
        html_str += "</body></html>"
        # write2test(html_str, "fix_test")
        write2html(html_str, fold_name, target_filename)

# page_num = ["binarize_017_180.jpg"]
#
# for filename in page_num:
#     # count += 1
#     print(filename)
#     filepath = filename
#     target_file_name = filename[:filename.find('.')]
#     data = get_image_content(filepath)
#     params = {
#         'app_id': APP_ID,
#         'time_stamp': str(int(time.time())),
#         'nonce_str': '20e3408a79',
#         'sign': '',
#         'image': data,
#     }
#
#     params['sign'] = get_req_sign(params, APP_KEY)
#     # #
#     response = do_http_post(params)
#     # with open("response.html", 'w') as f:
#     #     f.write(response.encode('utf-8'))
#     if response:
#         process_html_result2(response, "test2", target_file_name)
#     time.sleep(1)

start = time.time()
max_thread_nums = 10
threads = []
t1 = threading.Thread()
count = 0
# for i in range(172, 173):
for filename in os.listdir("result3"):
    count += 1
    # filename = str(i) + ".jpg"
    print(filename)
    filepath = 'result3/' + filename
    target_file_name = filename[:filename.find('.')]
    data = get_image_content(filepath)
    params = {
            'app_id': APP_ID,
            'time_stamp': str(int(time.time())),
            'nonce_str': '20e3408a79',
            'sign': '',
            'image': data,
        }

    params['sign'] = get_req_sign(params, APP_KEY)
    #
    response = do_http_post(params)
    if response:
        t = threading.Thread(target=process_html_result2, args=(response, "noise2noise", target_file_name))
        threads.append(t)
        if len(threads) >= max_thread_nums:
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            threads = []
    time.sleep(1)

if threads:
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

end = time.time()
print end - start

# filepath = 'result/169.jpg'
# filename = '169.jpg'
#
# target_file_name = filename[:filename.find('.')]
# data = get_image_content(filepath)
# params = {
#         'app_id': APP_ID,
#         'time_stamp': str(int(time.time())),
#         'nonce_str': '20e3408a79',
#         'sign': '',
#         'image': data,
#     }
#
# params['sign'] = get_req_sign(params, APP_KEY)
# #
# response = do_http_post(params)
# with open("response.html", 'w') as f:
#     f.write(response.encode('utf-8'))
#
# process_result(response, target_file_name)
# time.sleep(2)

