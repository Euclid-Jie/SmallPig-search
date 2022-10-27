# -*- coding: utf-8 -*-
# time: 2022/10/22 10:35
# file: 获取房东信息.py
# author: Euclid_Jie
import re
from time import sleep

import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm
import warnings

warnings.filterwarnings('ignore')


def get_luIdList(city):
    luIdList = pd.read_csv(city + '民宿列表.csv')
    return luIdList


def get_data(luId, driver):
    # 模开网页
    driver.get('https://m.xiaozhu.com/#/detail?luId=' + str(luId))
    WebDriverWait(driver, 10).until(lambda x: x.find_elements_by_class_name("fd_name.bold"))

    # 尝试点击操作
    try:  ## 部分介绍较短无需展开
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        # p = driver.find_elements_by_class_name("checkMoreDescri.pink")
        p = WebDriverWait(driver, 5).until(lambda x: x.find_elements_by_class_name("checkMoreDescri.pink"))
        p[0].click()
    except:
        pass

    # 获取内容
    data = driver.find_elements_by_class_name("infor_colunm")
    soup = BeautifulSoup(data[0].get_attribute('outerHTML'), features="lxml")
    datadf = pd.DataFrame({'luId': [''], '个性描述': [''], '内部情况': [''], '交通情况': ['']})
    datadf.loc[0]['luId'] = luId
    for item in soup.body.div.div.find_all('div'):
        datadf.loc[0][re.sub('[^\u4e00-\u9fa5]+', '', item.p.text)] = item.find_all('span')[1].text
    return datadf


if __name__ == '__main__':

    option = ChromeOptions()
    option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    driver = Chrome(options=option)  # 模拟开浏览器
    driver.get('https://m.xiaozhu.com/#')
    sleep(1)

    city = '广州'
    luIdList = get_luIdList(city)

    # 建表存储
    output = pd.DataFrame({'luId': [], '个性描述': [], '内部情况': [], '交通情况': []})
    output.to_csv(city + '民宿房东介绍' + '.csv', index=False, encoding='utf-8-sig', mode='w')

    # 遍历luid
    with tqdm(luIdList['id']) as t:
        for luId in t:
            t.set_description("luId:{}".format(luId))  # 进度条左边显示信息
            try:
                output = get_data(luId, driver)
                output.to_csv(city + '民宿房东介绍' + '.csv', index=False, encoding='utf-8-sig', mode='a', header=False)
                t.set_postfix({"状态": "成功写入"})  # 进度条右边显示信息
            except:
                t.set_postfix({"状态": "获取失败"})  # 进度条右边显示信息
