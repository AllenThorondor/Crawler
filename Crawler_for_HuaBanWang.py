#!/usr/bin/env python
# coding: utf-8

# # Proxy

# In[96]:


import sqlite3
db_name = 'Huaban.db'
conn = sqlite3.connect(db_name)
cur = conn.cursor()
cur.execute('CREATE TABLE Proxies(ip TEXT UNIQUE, port TEXT, tag TEXT, type TEXT, belong TEXT, delay TEXT, time TEXT, label INTEGER)')

cur.execute('CREATE TABLE Picture(pinId TEXT UNIQUE, status TEXT, label TEXT, tag TEXT, storagePath TEXT , propertyId TEXT )')


# In[87]:





# In[93]:





# In[94]:





# In[95]:





# In[ ]:





# In[ ]:





# In[97]:


def mainland():
    '''
    input: none
    output: ip_list
    '''
    import requests
    mainland_url = "https://www.kuaidaili.com/free/"
    oversea_url = "https://free-proxy-list.net/"
    resp = requests.get(mainland_url, timeout=3)   
    from bs4 import BeautifulSoup as BS
    soup = BS(resp.content)
    raw = soup('tr')
    
    import re
    ip_list = []
    for item in raw:
        ip = re.findall('"IP">(.+)</td>', str(item))
        port = re.findall('"PORT">(.+)</td>', str(item))
        if len(ip)>0:
            ip_list.append((ip[0] + ":" + port[0]))
    return ip_list

def oversea():
    '''
    input: none
    output: ip_list (to be fixed)
    '''
    import requests
    #国内高匿代理
    mainland_url = "https://www.kuaidaili.com/free"
    #国内普通代理
    #mainland_url = "https://www.kuaidaili.com/free/intr"
    
    oversea_url = "https://free-proxy-list.net/"
    resp = requests.get(oversea_url, timeout=3)   
    from bs4 import BeautifulSoup as BS
    soup = BS(resp.content)
    raw = soup('tr')
    
    import re
    ip_list = []
    for item in raw:
        ip = re.findall('"IP">(.+)</td>', str(item))
        port = re.findall('"PORT">(.+)</td>', str(item))
        if len(ip)>0:
            ip_list.append((ip[0] + ":" + port[0]))
    return ip_list

def get_proxy():
    """
    input: turn is string out of 'inland' or 'oversea'
    output: random selet one ip address
    format: { "http": xx.xx.xx.xx:nnnn } 
    planed feature: ProxyPool
    """
    cur = conn.cursor()
    
    chioce = cur.execute("""SELECT * FROM Proxies ORDER BY RANDOM() LIMIT 1""").fetchone()
  
    return chioce


# # proxy pool

# In[98]:


import requests
from parsel import Selector
import time
import os


# In[99]:


def insert_to_db(url):
    for i in range(5)[1:]:
        t = requests.get(url+str(i), timeout=3)
        time.sleep(2)
        sel = Selector(t.text)
        s = sel.css('tr').extract()

        for i in s:
            sub_sel = Selector(i)

            ip = sub_sel.css('td::text').extract()
            if len(ip) > 1 :

                cur.execute(''' INSERT OR IGNORE INTO Proxies(ip, port, tag, type, belong, delay, time, label) VALUES(?, ?, ?, ?, ?, ?, ?, ?) '''
                            ,(ip[0], ip[1], ip[2], ip[3], ip[4], ip[5], ip[6], 1))
                conn.commit()
                
                


# In[100]:


baseurl = {
    'high_anonymity_base' : "https://www.kuaidaili.com/free/inha/",
    'tedious_rear_base' : "https://www.kuaidaili.com/free/intr/"
}

for url in baseurl.values():
    insert_to_db(url)

    


# # entry

# In[101]:


def get_pinId(num, choice):
    '''
    input: none for this moment
    output: a list of sorted pinid 
    '''
    import requests
    from parsel import Selector
    import re

    baseurl = "https://huaban.com" + nav_link(choice)
    

    params = {
        'k4pnbii0': '', 
        'max': num,
        'limit': '20',
        'wfl': '1'
    }
    try:
        z = requests.get(url=baseurl, params=params, headers=headers)
        print(z.status_code)
    except requests.ConnectionError as e:
        return e
    

    pinid_list = []
    for i in z.json()['pins']:
        pinid_list.append(i['pin_id'])
        
    pinid_list = sorted(pinid_list) 
    for pinId in pinid_list:
        cur = conn.cursor()
        cur.execute(""" INSERT OR IGNORE INTO Picture(pinId, status, label) VALUES(?, ?, ?) """,(pinId, "Unretrieved", choice))
        conn.commit()
    return pinid_list


# In[112]:


def get_propertyId(pinid_list):
    '''
    input: none for this moment
    output: none
    function: download the image to the picture_temp folder for now
    '''
    
    import requests
    from parsel import Selector
    import re
    
    #generate image_file_list
    image_file_list = []
    for i in pinid_list:
        baseurl = 'https://huaban.com/pins/'
        detailurl = baseurl + str(i) + '/'
        z3 = requests.get(url=detailurl, headers=headers)
        time.sleep(1)
        sel1 = Selector(text=z3.text)
        try:
            jscode = sel1.xpath("//p[contains(., 'pin')]/text()").extract_first()
            s = re.findall('.+"key":"(.+?)"',jscode[:200])[0]
        except:
            s = "error on %s"%i
            continue
        print(s)
        
        image_file_list.append(s)
        cur.execute("""UPDATE Picture SET propertyId = ? WHERE pinid = ?""",(s, i))
        conn.commit()
        
    return image_file_list
        
def download(image_file_list, choice):
    #download the image accordingly to the folder
    import urllib
    import time
    import os
    downloadurl = 'https://hbimg.huabanimg.com/'
    cur = conn.cursor()
    for i in image_file_list:
        urllib.request.urlretrieve(downloadurl+i,'./{}/{}.jpg'.format(choice, i))
        time.sleep(5)
        cur.execute("""UPDATE Picture SET storagePath = ? WHERE propertyId = ?""",(os.getcwd()+'/{}/{}.jpg'.format(choice, i), i))
        conn.commit()


# In[103]:


false = False
what = {"imgHosts":{"muse-img":"muse-img.huabanimg.com", "hbimg":"hbimg.huabanimg.com", "hbimg_http":"hbimg.huabanimg.com", "hbimg-other":"hbimg-other.huabanimg.com"}, "hbfile":{"hbfile":"hbfile.huabanimg.com", "hbimg2":"hbimg2.huabanimg.com", "hbmedia":"video.huaban.com"}, "minImageWidth":16, "categories":[{"id":"web_app_icon", "name":"UI/UX", "col":1, "nav_link":"/favorite/web_app_icon/"}, {"id":"design", "name":"平面", "col":1, "nav_link":"/favorite/design/"}, {"id":"illustration", "name":"插画/漫画", "col":1, "nav_link":"/favorite/illustration/"}, {"id":"photography", "name":"摄影", "col":2, "nav_link":"/favorite/photography/"}, {"id":"games", "name":"游戏", "nav_link":"/favorite/games/"}, {"id":"anime", "name":"动漫", "nav_link":"/favorite/anime/"}, {"id":"industrial_design", "name":"工业设计", "col":2, "nav_link":"/favorite/industrial_design/"}, {"id":"architecture", "name":"建筑设计", "nav_link":"/favorite/architecture/"}, {"id":"art", "name":"人文艺术", "nav_link":"/favorite/art/"}, {"id":"home", "name":"家居/家装", "col":1, "nav_link":"/favorite/home/"}, {"id":"apparel", "name":"女装/搭配", "col":1, "nav_link":"/favorite/apparel/"}, {"id":"men", "name":"男士/风尚", "col":2, "nav_link":"/favorite/men/"}, {"id":"modeling_hair", "name":"造型/美妆", "nav_link":"/favorite/modeling_hair/"}, {"id":"diy_crafts", "name":"手工/布艺", "nav_link":"/favorite/diy_crafts/"}, {"id":"food_drink", "name":"美食", "nav_link":"/favorite/food_drink/"}, {"id":"travel_places", "name":"旅行", "nav_link":"/favorite/travel_places/"}, {"id":"wedding_events", "name":"婚礼", "col":2, "nav_link":"/favorite/wedding_events/"}, {"id":"kids", "name":"儿童", "nav_link":"/favorite/kids/"}, {"id":"pets", "name":"宠物", "nav_link":"/favorite/pets/"}, {"id":"quotes", "name":"美图", "nav_link":"/favorite/quotes/"}, {"id":"people", "name":"明星", "nav_link":"/favorite/people/"}, {"id":"beauty", "name":"美女", "nav_link":"/favorite/beauty/"}, {"id":"desire", "name":"礼物", "nav_link":"/favorite/desire/"}, {"id":"geek", "name":"极客", "nav_link":"/favorite/geek/"}, {"id":"data_presentation", "name":"数据图", "nav_link":"/favorite/data_presentation/"}, {"id":"cars_motorcycles", "name":"汽车/摩托", "nav_link":"/favorite/cars_motorcycles/"}, {"id":"film_music_books", "name":"电影/图书", "nav_link":"/favorite/film_music_books/"}, {"id":"tips", "name":"生活百科", "nav_link":"/favorite/tips/"}, {"id":"education", "name":"教育", "nav_link":"/favorite/education/"}, {"id":"sports", "name":"运动", "nav_link":"/favorite/sports/"}, {"id":"funny", "name":"搞笑", "nav_link":"/favorite/funny/"}, {"id":"fitness", "name":"健身/舞蹈", "display":false, "nav_link":"/favorite/fitness/"}, {"id":"other", "name":"其它", "display":false, "nav_link":"/favorite/other/"}, {"id":"digital", "name":"3C数码", "display":false, "selectable":false, "nav_link":"/favorite/digital/"}], "muse_categories":[{"id":"ui_designer", "name":"UI设计师"}, {"id":"designer", "name":"平面设计师"}, {"id":"photographer", "name":"摄影师"}, {"id":"illustrator", "name":"插画师"}, {"id":"graphic", "name":"漫画师"}, {"id":"animator", "name":"动画师"}, {"id":"household_desiger", "name":"家居设计师"}, {"id":"interior_designer", "name":"室内设计师"}, {"id":"architect", "name":"建筑设计师"}, {"id":"costume_designer", "name":"服装设计师"}, {"id":"industrial_designer", "name":"工业设计师"}, {"id":"stylist", "name":"造型师"}, {"id":"game_designer", "name":"游戏美术师"}, {"id":"artisan", "name":"手工艺人"}, {"id":"other", "name":"其它"}], "default_avatars":[391521, 389119, 504, 558, 4421412, 155485, 160341, 1087857, 767469, 3813778, 610, 4420875, 5437689], "default_avatar_img":{"bucket":"hbimg", "farm":"farm1", "frames":1, "height":300, "id":102890808, "key":"654953460733026a7ef6e101404055627ad51784a95c-B6OFs4", "type":"image/jpeg", "width":300}, "ios_version":"2016-04-29"}
temp_list = [what['categories'][i]['id'] for i in range(len(what['categories']))]    
temp_list


# In[104]:


def nav_link(choice):
    '''
    input: the keyword shown on HuaBanWang 
    output: interceptive fragment of nav_link 
    '''
    false = False
    what = {"imgHosts":{"muse-img":"muse-img.huabanimg.com", "hbimg":"hbimg.huabanimg.com", "hbimg_http":"hbimg.huabanimg.com", "hbimg-other":"hbimg-other.huabanimg.com"}, "hbfile":{"hbfile":"hbfile.huabanimg.com", "hbimg2":"hbimg2.huabanimg.com", "hbmedia":"video.huaban.com"}, "minImageWidth":16, "categories":[{"id":"web_app_icon", "name":"UI/UX", "col":1, "nav_link":"/favorite/web_app_icon/"}, {"id":"design", "name":"平面", "col":1, "nav_link":"/favorite/design/"}, {"id":"illustration", "name":"插画/漫画", "col":1, "nav_link":"/favorite/illustration/"}, {"id":"photography", "name":"摄影", "col":2, "nav_link":"/favorite/photography/"}, {"id":"games", "name":"游戏", "nav_link":"/favorite/games/"}, {"id":"anime", "name":"动漫", "nav_link":"/favorite/anime/"}, {"id":"industrial_design", "name":"工业设计", "col":2, "nav_link":"/favorite/industrial_design/"}, {"id":"architecture", "name":"建筑设计", "nav_link":"/favorite/architecture/"}, {"id":"art", "name":"人文艺术", "nav_link":"/favorite/art/"}, {"id":"home", "name":"家居/家装", "col":1, "nav_link":"/favorite/home/"}, {"id":"apparel", "name":"女装/搭配", "col":1, "nav_link":"/favorite/apparel/"}, {"id":"men", "name":"男士/风尚", "col":2, "nav_link":"/favorite/men/"}, {"id":"modeling_hair", "name":"造型/美妆", "nav_link":"/favorite/modeling_hair/"}, {"id":"diy_crafts", "name":"手工/布艺", "nav_link":"/favorite/diy_crafts/"}, {"id":"food_drink", "name":"美食", "nav_link":"/favorite/food_drink/"}, {"id":"travel_places", "name":"旅行", "nav_link":"/favorite/travel_places/"}, {"id":"wedding_events", "name":"婚礼", "col":2, "nav_link":"/favorite/wedding_events/"}, {"id":"kids", "name":"儿童", "nav_link":"/favorite/kids/"}, {"id":"pets", "name":"宠物", "nav_link":"/favorite/pets/"}, {"id":"quotes", "name":"美图", "nav_link":"/favorite/quotes/"}, {"id":"people", "name":"明星", "nav_link":"/favorite/people/"}, {"id":"beauty", "name":"美女", "nav_link":"/favorite/beauty/"}, {"id":"desire", "name":"礼物", "nav_link":"/favorite/desire/"}, {"id":"geek", "name":"极客", "nav_link":"/favorite/geek/"}, {"id":"data_presentation", "name":"数据图", "nav_link":"/favorite/data_presentation/"}, {"id":"cars_motorcycles", "name":"汽车/摩托", "nav_link":"/favorite/cars_motorcycles/"}, {"id":"film_music_books", "name":"电影/图书", "nav_link":"/favorite/film_music_books/"}, {"id":"tips", "name":"生活百科", "nav_link":"/favorite/tips/"}, {"id":"education", "name":"教育", "nav_link":"/favorite/education/"}, {"id":"sports", "name":"运动", "nav_link":"/favorite/sports/"}, {"id":"funny", "name":"搞笑", "nav_link":"/favorite/funny/"}, {"id":"fitness", "name":"健身/舞蹈", "display":false, "nav_link":"/favorite/fitness/"}, {"id":"other", "name":"其它", "display":false, "nav_link":"/favorite/other/"}, {"id":"digital", "name":"3C数码", "display":false, "selectable":false, "nav_link":"/favorite/digital/"}], "muse_categories":[{"id":"ui_designer", "name":"UI设计师"}, {"id":"designer", "name":"平面设计师"}, {"id":"photographer", "name":"摄影师"}, {"id":"illustrator", "name":"插画师"}, {"id":"graphic", "name":"漫画师"}, {"id":"animator", "name":"动画师"}, {"id":"household_desiger", "name":"家居设计师"}, {"id":"interior_designer", "name":"室内设计师"}, {"id":"architect", "name":"建筑设计师"}, {"id":"costume_designer", "name":"服装设计师"}, {"id":"industrial_designer", "name":"工业设计师"}, {"id":"stylist", "name":"造型师"}, {"id":"game_designer", "name":"游戏美术师"}, {"id":"artisan", "name":"手工艺人"}, {"id":"other", "name":"其它"}], "default_avatars":[391521, 389119, 504, 558, 4421412, 155485, 160341, 1087857, 767469, 3813778, 610, 4420875, 5437689], "default_avatar_img":{"bucket":"hbimg", "farm":"farm1", "frames":1, "height":300, "id":102890808, "key":"654953460733026a7ef6e101404055627ad51784a95c-B6OFs4", "type":"image/jpeg", "width":300}, "ios_version":"2016-04-29"}
    categories = what['categories']
    for item in categories:
        if item['id'] == choice:
            return item['nav_link']


# In[110]:


headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept": '"application"',
        "X-Request": "JSON",
        "X-Requested-With": "XMLHttpRequest"
    }
for i in temp_list:
    path = '%s'%i
    print(i)
    if os.path.exists(path):
        continue
    try:
        os.mkdir(path)
    except FileExistsError:
        os.mkdir(path+'_temp')
    except:
        print('there is error')

def entry(choice):
    nav_link(choice)
    cur = conn.cursor()
    print(choice)
    good = cur.execute("""SELECT pinId FROM Picture WHERE label = ? ORDER BY pinId DESC LIMIT 0, 1""", (choice, )).fetchone()
    base = good if good != None else 2894354944
    print(base)
    pinid_list = get_pinId(base, choice)
    image_file_list = get_propertyId(pinid_list)
    download(image_file_list, choice)
    


# In[113]:


for category in temp_list:
    entry('digital')


# In[ ]:





# In[ ]:





# In[70]:



        


# In[107]:




entry('digital')


# In[109]:



        
        


# In[80]:


import requests
from parsel import Selector
import json
headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept": '"application"',
        "X-Request": "JSON",
        "X-Requested-With": "XMLHttpRequest"
    }

baseurl = 'https://huaban.com/pins/'
detailurl = baseurl + str(2894354944) + '/'
z3 = requests.get(url=detailurl, headers=headers)
sel1 = Selector(text=z3.text)
#jscode = sel1.xpath("//p[contains(., 'pin')]/text()").extract_first()
#s = re.findall('.+"key":"(.+?)"',jscode[:200])[0]



# In[ ]:





# In[65]:





# In[ ]:





# In[ ]:





# In[113]:





# In[ ]:





# In[59]:



        


# In[ ]:







# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




