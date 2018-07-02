# author Helanfeiyun

import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pyquery import PyQuery as pq
from selenium.webdriver.common.keys import Keys
import time
import math

from write2excel import writer



#基本信息
url = 'http://www.mafengwo.cn/poi/10123.html'
file = '这是测试马蜂窝景点数据4.xls'
name ="鸟巢"
num = 21
district = '海淀'+ name
title = ['景点名称','用户打分','评论','评论时间']
name_info = [name]


#设置Chrome
options = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values': {
        'images': 2
    }
}

options.add_experimental_option('prefs', prefs)
#options.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')
#options.add_argument('user-agent="Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50"')
browser = webdriver.Chrome(chrome_options=options)
browser.maximize_window()
wait = WebDriverWait(browser,2)

def getDetailInfo():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '._j_commentlist')))

    for i in range(1,num+1):
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'._j_commentlist')))
        html = browser.page_source
        doc = pq(html)

        items = doc('.rev-list .rev-item').items()
        for item in items:
            if item == None:
                print("item中没有信息")
            else:
                title = str(item.find('.s-star').attr('class'))[-1]
                if title == '1':
                    title = "很差"
                elif title == '2':
                    title = "一般"
                elif title == '3':
                    title = "好"
                elif title == '4':
                    title = "很好"
                elif title == '5':
                    title = "非常好"
                comment = item.find('.rev-txt').text()
                comment_time = item.find('.time').text()[:11]
                info = [title, comment, comment_time]
                title_info = name_info + info
                writer(title_info, district, file, interval=False)

        print(i)
        nextPage()


def nextPage():
    next_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,'.pg-next'))
    )
    time.sleep(1)
    next_button.click()
    # while cur_num != str(num) :
    #     print(cur_num,str(num))
    #     input.clear()
    #     input.send_keys(num)
    #     #submit = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#cPageBtn')))
    #     input.send_keys(Keys.ENTER)
    #     cur_num = doc('#divCtripComment > div.c_page_box > div > div.c_page_list.layoutfix > a.current').text()

def main():
    browser.get(url)
    writer(title,district, file,interval=False)
    getDetailInfo()


if __name__ == '__main__':
    main()
