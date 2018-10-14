from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pymongo
import re
import records


male = True
MONGO_URL = 'localhost'
MONGO_DB = 'jia36'
MONGO_DB2 = 'jia39'
# MONGO_COLLECTION = 'users_female'
MONGO_COLLECTION = 'user_male'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

client2 = pymongo.MongoClient(MONGO_URL)
db2 = client[MONGO_DB2]
collection2 = db2[MONGO_COLLECTION]

User = '18081406220'
Password = '180212'
browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
loginUrl = 'http://search.jiayuan.com/v2/'
browser.get(loginUrl)

def login():
    print('login')
    try:
        inputUser = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#login_email_new')))
        inputPass = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#login_password_new')))
        button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'input[class="login_btn"]')))
        inputUser.clear()
        inputUser.send_keys(User)
        inputPass.send_keys(Password)
        inputPass.send_keys(Keys.ENTER)
    except TimeoutException as e:
        print(e)
def get_basic():
    listInfo = []
    html = browser.page_source
    bsObj = BeautifulSoup(html)
    infos = bsObj.findAll('div',{"class":{"hy_box"}})
    for info in infos:
        userId = info.attrs["onmouseover"]
        userId = re.findall(r"'(.+?)'",userId)
        userId = userId[0]
        userId = userId[8:]
        print(userId)
        name = info.find('div',{"class":{"user_name"}}).find('a').get_text()
        print(name)
        age = info.find('p',{"class":{"user_info"}}).get_text()
        print(age)
        height = info.find('p',{"class":{"zhufang"}}).find('span').get_text()
        print(height)
        listInfo.append({'userid':userId,'name':name,'age':age,'height':height})
    save_db(collection,listInfo)
def get_detail():
    pass
def save_info():
    pass
def skip_next():
    skipButton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'li[id="select_box"] + li a')))
    skipButton.click()
def switch_to_male():
    try:
        time.sleep(5)
        listButton1 = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div[data-index="4"] span[class="JY-title"] i[class="JY-item-arr"]')))
        print(listButton1.get_attribute('class'))
        listButton1.click()
        selectMale = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'select[name="height2"] option[value="190"]')))
        print(selectMale.get_attribute('value'))
        selectMale.click()
        maleButton = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="JY-sp sg"] button[class="JY-sp-b"]')))
        maleButton.click()

            # gender
        time.sleep(5)
        listButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'i[class="JY-item-arr"]')))
        listButton.click()
        selectMale = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select[name="Sex"] option[value="1"]')))
        print(selectMale.get_attribute('value'))
        selectMale.click()
        maleButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="JY-sp-b"]')))
        maleButton.click()

    except Exception as e:
        print(e)
def close_win():
    listButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id="jy_bottom_avatar"] div' )))
    listButton.click()
def save_db(collect,result):
    try:
        if collect.insert(result):
            print('c')
    except Exception as e:
        print(e)



login()
if male == True:
    close_win()
    switch_to_male()
for i in range(100):
    browser.forward()
    browser.forward()
    time.sleep(3)
    get_basic()
    time.sleep(4)
    skip_next()

detail_infos_list = []
detail_infos = {}
num1 = 0

# 优化方法同时交给多个线程做处理

for i in collection.find():
    detail_infos = {}
    num1 = num1 + 1
    if num1 == 10:
        save_db(collection2, detail_infos_list)
        num1 = 0
        detail_infos_list = []
    time.sleep(1)
    url = 'http://www.jiayuan.com/'+ i["userid"]
    try:
        browser.get(url)
        html = browser.page_source
        bsobj = BeautifulSoup(html)
    except Exception as e:
        print(e)
    try:
        lis = bsobj.find('ul',{'class':{'member_info_list fn-clear'}})
        for li in lis.findAll('li'):
            key = li.find('div',{'class':{'fl f_gray_999'}}).get_text()
            key = re.sub('\n+','',key)
            value = li.find('div',{'class':{'fl pr'}}).get_text()
            value = re.sub('\n+','',value)
            detail_infos[key] = value
        # img_url
        img_url = bsobj.find('img',{'class':{'img_absolute'}})
        detail_infos['img_url'] = img_url.attrs['src']
        #
        uls = bsobj.findAll('ul',{'class':{'js_list fn-clear'}})
        for ul in uls:
            lis = ul.findAll('li',{'class':{'fn-clear'}})
            for li in lis:
                title = li.find('span').get_text()
                title = re.sub(' ','',title)
                title = re.sub('\xa0', '', title)
                value_new = li.find('div').get_text()
                if value_new is None:
                    value_new = li.find('div').find('em').get_text()
                detail_infos['r'+title] = value_new
        age = bsobj.find('h6',{'class':{'member_name'}})
        detail_infos['age'] = age.get_text()
        detail_infos['id'] = i["userid"]
        detail_infos_list.append(detail_infos)
        print(detail_infos)
    except Exception as e:
        print(e)