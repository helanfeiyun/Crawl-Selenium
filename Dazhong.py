# author Helanfeiyun

import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import time
import math
import random

from write2excel import writer


#基本信息
url = 'http://www.dianping.com/shop/5453109'
num = 12
file = 'excel名称.xls'
district = '海淀区'
shop_name = '商铺名称'
shop_add = '商铺地址'
shop_rank = '星级'
title = ['店名', '地址', '商户等级', '人均', '用户评价','评论','评论时间']
shop_info = [shop_name,shop_add,shop_rank,'240']


#设置Chrome
options = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values': {
        'images': 2
    }
}
#options.add_argument('--proxy-server=http://120.25.164.134:8118')
options.add_experimental_option('prefs', prefs)
#options.add_argument('user-agent="Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50"')
# options.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')

browser = webdriver.Chrome(chrome_options=options)

wait = WebDriverWait(browser,3)




#获取商家主页面
def getMainPage():
    try:
        browser.get(url)
    except TimeoutException:
        return print("获取商家主页面出错")

# 确定评论总页数
def pageNum():
    total = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#avgPriceTitle'))
    )

    total = re.compile('(\d+)').search(total.text).group(1)
    num = math.ceil(int(total) / 20)
    return num

#获取商家信息

def getShopInfo():
    browser.get(url)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#basic-info > div.brief-info'))
    )
    html = browser.page_source
    doc = pq(html)
    avgPrice = re.compile('\d+').search(doc.find('#avgPriceTitle').text())
    print(avgPrice)
    t = re.compile('(\d.?\d?)').findall(doc.find('#basic-info > div.brief-info ').text())[0]
    e = re.compile('(\d.?\d?)').findall(doc.find('#basic-info > div.brief-info ').text())[1]
    s = re.compile('(\d.?\d?)').findall(doc.find('#basic-info > div.brief-info ').text())[2]
    add = doc.find('#basic-info > div.expand-info.address > span.item').text()
    shop_info2 =  [add] + [shop_rank] +[avgPrice,t,e,s]
    shop_info.append(shop_info2)



#进入评论详情页
def detailPage():
    pass
    return None

def transInfo(character):
    if character == "差":
        character = "1"
    elif character == "很差":
        character = "1"
    elif character == "一般":
        character = "2"
    elif character == "好":
        character = "3"
    elif character == "很好":
        character = "4"
    elif character == "非常好":
        character = "5"
    return character


#循环获取详情页面
def search(page):
    try:
        browser.get(url+'/review_more_latest?pageno='+page)
        print(page)
        getDetailInfo()
    except TimeoutException:
        return "获取循环页面出错"

#获取评论信息
def getDetailInfo():
    print('in the getDetailInfo')
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#review-list > div.review-list-container > div.review-list-main > div.review-list-header > h1 > a'))
    )
    html = browser.page_source
    print('got html')
    doc = pq(html)
    items = doc('#review-list .reviews-items .main-review').items()
    for item in items:
        if item == None:
            print("item中没有信息")
        else:
            try:
                title = str(item.find('.sml-rank-stars').attr('class'))[-7]
                if title == '1':
                    title = "很差"
                elif title =='2':
                    title = "一般"
                elif title =='3':
                    title ="好"
                elif title =='4':
                    title = "很好"
                elif title =='5':
                    title = "非常好"
            except:
                continue
            comment = item.find('.review-words').text()
            comment_time = item.find('.time ').text()
            info = [title,comment,comment_time]
            title_info = shop_info + info
            writer(title_info, district, file ,interval=False)

            print(info)
            print('\n')

    return None




def main():

    writer(title,district, file,interval=False)
    sleep_time = random.randint(6,13)
    for page in range(1,num+1):
        time.sleep(sleep_time)
        search(str(page))

if __name__ == '__main__':
    main()