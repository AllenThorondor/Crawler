#!/usr/bin/env python
# coding: utf-8

# # Crawler for AcaGrid

# In[2]:


"""
from selenium import webdriver
import time
import builtwith
import whois
import json
import re
url = 'https://www.acagrid.com/user/entry/signin#email'
t = builtwith.parse(url)
#print(t)
#print(whois.whois('www.acagrid.com'))

username = '13823356269'
password = 'hike8484'


profile=webdriver.FirefoxProfile()
profile.accept_untrusted_certs=True
driver=webdriver.Firefox(firefox_profile=profile)
driver.get("https://www.acagrid.com/user/entry/signin#email")
driver.find_element_by_link_text(u'账户登录').click()
driver.find_element_by_name("email").is_displayed()
driver.find_element_by_name("email").send_keys(username)
driver.find_element_by_name("password").send_keys(password)
driver.find_element_by_css_selector(".btn").click()
cookies = driver.get_cookies()[0]
print(cookies)
"""
import requests
import json
import re
import time

#一开始用selenium获取cookies，发现获取的cookies没法用，于是手动copy了一份
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
}
cookies = {
    'fc_md5rand': '4df37bec8a6485af920515aa070fb801',
    'Hm_lpvt_9f0d0c268381e49041b4be33dc9a86cb': '1577555078',
    'Hm_lvt_9f0d0c268381e49041b4be33dc9a86cb': '1577555075',
    'MEIQIA_TRACK_ID': '1Vcawfkx1iee7SXZAppiIsWaWMC',
    'MEIQIA_VISIT_ID': '1VcawfRzxboyyHcq4WekcMdYRTQ',
    'PHPSESSID': 'jk9nncfpsb5ea7kg27q7g5jcq2'
}

params = {
    "page": "1",
    "doc_status": "0",
    "model": "paper",
    "view_order": "time:asc"
}
#ajax 拉取的page最大值居然就在返回的json里（毕竟只有4页），索性手动设定了page最大值
page=5
list1 = []
index = []
for index in range(page)[1:]:
    params = {
    "page": index,
    "doc_status": "0",
    "model": "paper",
    "view_order": "time:asc"
    }
    time.sleep(1)
    
    url = 'https://www.acagrid.com/api/factory/get_paginate_docs_by_filter?'
    t = requests.get(url=url, params=params, headers=headers, cookies=cookies)
    s = t.json()
    index = list(s['data']['docs']['dataset'][0].keys())
    print(len(s['data']['docs']['dataset']))
    list1.extend(s['data']['docs']['dataset'])
    
#写入csv文件
import csv
# index = ['title', 'jurnal', 'sci_inter_jcr', 'impact_factor', 'wos', 'co_authors', 'jurnal_puttime', 'page_index', 'rank', 'issn', 'batch']
with open("test4.csv","w") as csvfile: 
    writer = csv.writer(csvfile)

    #先写入columns_name
    writer.writerow(index)
    #然后循环写入row
for i in list1:
    row = []
    for j in index:
        value = i[j] if j != 'co_authors' else [i[j][x]['realname'] for x in range(len(i['co_authors']))]
        row.append(value)
    with open('test4.csv','a') as csvfile:
        writer=csv.writer(csvfile)
        writer.writerow(row)


# In[ ]:




