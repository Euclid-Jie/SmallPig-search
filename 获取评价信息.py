# -*- coding: utf-8 -*-
# time: 2022/10/21 23:24
# file: 获取评价信息.py
# author: Euclid_Jie

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import json
import warnings
from tqdm import tqdm

warnings.filterwarnings('ignore')
import numpy as np


def get_luIdList(city):
    luIdList = pd.read_csv(city + '民宿列表.csv')
    return luIdList


def get_comments_item_df(commentsList, luId):
    """
    根据commentslist 遍历获取comments内容
    :return:
    """
    dataDf = pd.DataFrame()
    for comment in commentsList:
        data = json.loads(comment)
        try:
            commentContent = data['content']  # 评论内容
            commentContent = re.sub('[^\u4e00-\u9fa5]+', '', commentContent)
        except:
            commentContent = np.NaN

        try:  # 部分时间缺失
            publishTime = data['createtime']  # 评论时间
        except:
            publishTime = np.NaN
        dataDf = pd.concat(
            [dataDf, pd.DataFrame({'content': [commentContent], 'time': [publishTime], 'roomLuid': [luId]})])
    return dataDf


def get_room_comments_num(luId, headers):
    roomCommentsUrl = 'https://wirelesspub-general.xiaozhu.com/comment/commentlist?luId=' + str(
        luId) + '&offset=0&length=5'
    response = requests.get(roomCommentsUrl, headers=headers, timeout=60)  # 使用request获取网页
    html = response.content.decode('utf-8', 'ignore')  # 将网页源码转换格式为html
    soup = BeautifulSoup(html, features="lxml")  # 构建soup对象
    ## 构建评论list，包含多条评论
    s = r'(?<="commentCount":")\d+(?=")'
    pattern = re.compile(s)
    commentsNum = int(pattern.findall(soup.text)[0])
    return commentsNum


def get_room_comments_data(luId, headers, commentsNum):
    ## 若评价
    if commentsNum == 0:
        output = pd.DataFrame()
    ## 若有评价
    else:
        ### 遍历
        #### 设置参数
        output = pd.DataFrame()
        length = 10  # 一次爬取量
        for offset in range(0, commentsNum, length):  # 遍历起点
            # 获取评论
            roomCommentsUrl = 'https://wirelesspub-general.xiaozhu.com/comment/commentlist?luId=' + str(
                luId) + '&offset=' + str(offset) + '&length=' + str(length)
            response = requests.get(roomCommentsUrl, headers=headers, timeout=60)  # 使用request获取网页
            html = response.content.decode('utf-8', 'ignore')  # 将网页源码转换格式为html
            soup = BeautifulSoup(html, features="lxml")  # 构建soup对象
            ## 构建评论list，包含多条评论
            html = soup.body.p.text
            s = r'{[^{^}]+}'
            pattern = re.compile(s)
            commentsList = pattern.findall(html)
            ## 处理list返回数据
            data_df = get_comments_item_df(commentsList, luId)
            ## 拼接数据
            output = pd.concat([output, data_df])

    return output


if __name__ == '__main__':

    # 设置headers
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.0.0 Safari/537.36 '
    }

    # 设置参数
    city = '湛江市'
    luIdList = get_luIdList(city)

    # 建表存储
    output = pd.DataFrame({'content': [], 'time': [], 'roomLuid': []})
    output.to_csv(city + '民宿评论信息' + '.csv', index=False, encoding='utf-8-sig', mode='w')

    # 遍历luid
    with tqdm(luIdList['id']) as t:
        for luId in t:
            # 设置进度条参数
            t.set_description("luId:{}".format(luId))  # 进度条左边显示信息
            try:
                # 获取评论总条数
                commentsNum = get_room_comments_num(luId, headers)
                t.set_postfix({"状态": "正在写入{}条".format(commentsNum)})  # 进度条右边显示信息
                output = get_room_comments_data(luId, headers, commentsNum)
                output.to_csv(city + '民宿评论信息' + '.csv', index=False, encoding='utf-8-sig', mode='a', header=False)
                t.set_postfix({"状态": "已成功写入{}条".format(len(output))})  # 进度条右边显示信息
            except:
                t.set_postfix({"状态": "获取失败"})  # 进度条右边显示信息
