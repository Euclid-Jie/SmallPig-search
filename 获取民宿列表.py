# -*- coding: utf-8 -*-
# time: 2022/10/21 23:21
# file: 获取民宿列表.py
# author: Euclid_Jie

from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
import warnings
from tqdm import tqdm

warnings.filterwarnings('ignore')


def rolling_get(cityId, city):
    # 创建储存表，请确定之前的文件已重命名保存，否则同名会被覆盖
    emptyDf = pd.DataFrame({'id': [], 'title': []})
    emptyDf.to_csv(city + '民宿列表' + '.csv', index=False, encoding='utf-8-sig', mode='w')
    # 模拟开浏览器
    option = ChromeOptions()
    option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    driver = Chrome(options=option)  # 模拟开浏览器
    driver.get('https://m.xiaozhu.com/#')
    sleep(3)
    ## TODO 此处的日期适当往后调
    driver.get(
        'https://m.xiaozhu.com/#/result?cityId=' + cityId + '&city=' + city + '&landmark=&timeZone=&checkInDay=2022-10-25&checkOutDay=2022-10-26')
    sleep(1)
    # 循环遍历，当当前页面无法刷新后，将停止，请保证网络连接顺畅，如网速慢，请调高sleepTime时间
    sleepTime = 2
    sleep(sleepTime)
    ## 固定参数，勿动
    oldLen = 0
    newLen = -1
    ## 开始遍历
    while newLen != oldLen:
        oldLen = newLen
        for i in range(0, 3):  # 3代表一次写入30
            ### 滑动到页面底部
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            sleep(sleepTime)
        newLen = get_id_list(city, driver, oldLen)


# 获取元素
def get_id_list(city, driver, oldLen):
    # 获取浏览器元素
    idList = driver.find_elements_by_class_name('list_con')
    soup = BeautifulSoup(idList[0].get_attribute('outerHTML'))
    divs = soup.find_all('div', "list clearfix carnival_item")
    newLen = len(divs)

    if newLen == oldLen:
        for i in range(0, 2):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            sleep(1)

    outData = pd.DataFrame()
    # 输出数据，每面写入一次
    for i in tqdm(range(oldLen, newLen)):
        ## 获取信息
        id = divs[i]['id']
        title = divs[i].find('h5', 'title').text
        data = pd.DataFrame({'id': [str(id)], 'title': [title]})
        outData = pd.concat([outData, data])
    # 写入数据
    outData.to_csv(city + '民宿列表' + '.csv', index=False, encoding='utf-8-sig', mode='a', header=False)
    print('已写入数据至{},本次写入{}条'.format(newLen, newLen - oldLen))
    return newLen


if __name__ == '__main__':
    cityId = '272'
    city = '揭阳市'
    rolling_get(cityId, city)
