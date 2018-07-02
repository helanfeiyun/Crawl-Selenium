# author Helanfeiyun

import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pyquery import PyQuery as pq
import time
import math
import random
from write2excel import writer


#基本信息
url = 'http://oujunxiangshuicheng.fang.com/dianping/s4/'
file = '房天下小区数据.xls'
district = '怀柔区'
title = ['楼盘名称', '综合评分', '总价格', '总地段', '总配套', '总交通', '总环境', '用户评价', '价格', '地段', '交通', '配套','环境','评论','评论时间']
num=1

#设置Chrome
options = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values': {
        'images': 2
    }
}

options.add_experimental_option('prefs', prefs)
options.add_argument('user-agent="Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)"')
browser = webdriver.Chrome(chrome_options=options)
wait = WebDriverWait(browser,3)


# def goComment():
#     get_comment = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.dianping .bigtit .gray6.f14.fr')))
#     time.sleep(3)
#     get_comment.click()

def showMoreInfo():
    global num
    try:
        show_info = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#xfdp_B01_20 > a')))
        time.sleep(1)
        show_info.click()
        num = num + 1
        return 2
    except:
        print('无更多信息')


def getDetailInfo():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#daohang')))
    time.sleep(1)
    while showMoreInfo()== 2 and num <=16 :
        time.sleep(2)
        print("in the more information")
        pass

    html = browser.page_source
    doc = pq(html)
    print(doc)
    houses_name = doc('#xfxq_B03_01').attr('title')
    houses_first = doc('body .Comprehensive_score .mgt_2').text()
    houses_second = re.compile('(.\d\d)').findall(doc('body .Comprehensive_score .fbold14').text())
    houses_score = str(houses_first) + houses_second[0]
    houses_gray = doc('body .Comprehensive_score .font_gray').text()
    houses_price = re.compile('\d.\d\d').findall(houses_gray)[0]
    houses_loc = re.compile('\d.\d\d').findall(houses_gray)[1]
    houses_support = re.compile('\d.\d\d').findall(houses_gray)[2]
    houses_trans = re.compile('\d.\d\d').findall(houses_gray)[3]
    houses_env = re.compile('\d.\d\d').findall(houses_gray)[4]
    houses_info = [houses_name,houses_score,houses_price,houses_loc,houses_support,houses_trans,houses_env]
    items = doc('#dpContentList .comm_list .comm_list_nr').items()
    print('楼盘信息保存完毕')
    for item in items:
        if item == None:
            print("item中没有信息")
        else:
            try:
                list_score = item.find('.comm_list_score .inf').text()
                comm_price = re.compile('(\d)').findall(list_score)[0]
                comm_loc = re.compile('(\d)').findall(list_score)[1]
                comm_trans = re.compile('(\d)').findall(list_score)[2]
                comm_support = re.compile('(\d)').findall(list_score)[3]
                comm_env = re.compile('(\d)').findall(list_score)[4]
                comm_score = (int(comm_price)+int(comm_loc)+int(comm_trans)+int(comm_support)+int(comm_env))/5
                comment = item.find('.comm_list_con').text()
                comment_time = item.find('.look_hou').text()[:10]
                comm_info = [comm_score,comm_price,comm_loc,comm_trans,comm_support,comm_env,comment,comment_time]
                title_info = houses_info + comm_info
                writer(title_info, district, file, interval=False)
            except:
                continue


def main():
    browser.get(url)
    writer(title, district, file, interval=False)
    #goComment()
    getDetailInfo()

if __name__ == '__main__':
    main()




