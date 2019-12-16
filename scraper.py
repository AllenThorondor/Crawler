#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup as BS
import requests, re, urllib, sqlite3, os, time
import random


global num_id

NEW_LINK = 1
RETRIEVED_LINK = 2
ILL_LINK = 3

WHEELS_SUCC = 1
WHEELS_GETCONTENTFAIL = 2
WHEELS_GETURLFAIL = 3

class Crawler:
    """
    method:
    1, get_img
    2, get_content
    3, get_title
    4, feed_to_database
    """

    def __init__(self, link_url):
        """
        input: the url link that need to be scrap
        output: the soup object consisting of web text
        """
        self.link_url = link_url
        try:
            url_handler = requests.get(link_url, timeout=3)
            self.soup = BS(url_handler.content, 'html.parser')
        except KeyboardInterrupt:
            print('Crawler: Program interrupted by user...')
        except:
            print("Crawler: Unable to retrieve or parse page")

    def __str__(self):
        return "url: "+ self.link_url

    def get_img(self, max_img, save):
        """
        planned feature:
        1, make a Img_crawler subclass of Crawler
        2, add in the option "max_img" represent the max of img downloaded, return a list of img if
            max > 1, or return img if max = 1
        3, add option "save", if True, save the img in correspond name in the same folder, not if
            False
        """
        tags = self.soup('img')
        img_link_list = list()
        temp_img = "temp_img"
        print("    img to retrive:",max_img)

        for tag in tags:
            imglink = re.findall('src="(.+?\.jpg)"', str(tag))
            if imglink != '':
                img_link_list.extend(imglink)
        print("    total img link in page:",len(img_link_list))

        if max_img == 1:
            if str(img_link_list[0]).startswith("http"):
                img_blob = requests.get(img_link_list[0]).content
                if save:
                    with open('%s.png'%temp_img, 'wb') as f:
                        f.write(img_blob)
                    # urllib.request.urlretrieve(img_link_list[0],'%s.jpg'%temp_img)
                return img_blob
            else:
                img_blob = requests.get('http:' + img_link_list[0]).content
                if save:
                    with open('%s.png'%temp_img, 'wb') as f:
                        f.write(img_blob)
                    # urllib.request.urlretrieve('http:'+img_link_list[0],'%s.jpg'%temp_img)
                    # fp = open('{}.jpg'.format(temp_img), 'rb')
                    # img = fp.read()
                    # fp.close()
                return img_blob
        elif 1 < max_img <= len(img_link_list):
            img_list = list()
            for i in range(max_img):
                if str(img_link_list[i]).startswith('http'):
                    urllib.request.urlretrieve(img_link_list[i],'%s.jpg'%(temp_img+str(i)))
                else:
                    urllib.request.urlretrieve('http:'+img_link_list[i],'%s.jpg'%(temp_img+str(i)))
                fp = open('{}.jpg'.format(temp_img+str(i)), 'rb')
                img = fp.read()
                fp.close()
                if not save:
                    os.remove('{}.jpg'.format(temp_img+str(i)))
                img_list.append(img)
            print("    Done, image save:", save)
            return img_list
        else:
            print("    image quantity limit:", len(img_link_list))
            return None

    def get_content(self):
        tags = self.soup('p')
        content = ''
        for tag in tags:
            if str(tag).startswith('<p>'):
                try:
                    # x = re.findall('(\S+)',str(tag))[1].replace('</p>','')
                    x = tag.text
                    content = content + '\n' + x
                except:
                    print("    get_content", tag, "is something wrong")
                    continue
        return content

    def get_title(self):
        raw = self.soup.title
        title = re.findall('\n(.+?)\n', str(raw))
        return title[0].strip()

    def get_url(self):
        tags = self.soup('a')
        url_list = []
        for tag in tags:
            url = tag.get('href', None)
            if ( url != "") and ( str(url).startswith('javascript:') == False):
                if str(url).endswith("html"):
                    url_list.append(url)
        # print("===>len of url_list: ", len(url_list))
        return url_list


class Teller:
    """

    """

    def __init__(self):
        pass

    def __str__(self):
        pass

    def customer_service(self):
        """
        input: no input should give to an teller object, cause she will ask what
        she need in interaction
        output: self.url, self.web_site_count, self.DB_name

        feature: teller can only create table , but can not muse data in that table
        """
        # url insert
        self.url = input("the web site url: ")
        if len(self.url)<1 :
            self.url = "http://tech.sina.com.cn/csj/2019-09-30/doc-iicezueu9275049.shtml"
        elif self.url.startswith("www"):
            self.url = "https://" + self.url

        #webiste count to scrap
        self.web_site_count = input("the limit of webs: ")
        if len(self.web_site_count) <= 0 or self.web_site_count == 0:
            self.web_site_count = 100
        elif not str(self.web_site_count).isdigit():
            print("digital number is needed for this input")
            self.web_site_count = input("the limit of webs: ")
        print("the url: ", self.url,"\nthe web count: ", self.web_site_count)

        #Database name to create
        self.DB_name = input("database name: ") + ".sqlite"
        if len(self.DB_name) == ".sqlite":
            self.DB_name = "test.sqlite"

        return self.url, self.web_site_count, self.DB_name

    def db_setup(self):
        """
        feature: set up "URLs" and "pages" table
        output: conn, cur
        """
        #database URLs table set up
        conn = sqlite3.connect('{}'.format(self.DB_name))
        cur = conn.cursor()
        cur.execute('CREATE TABLE URLs(url TEXT UNIQUE, label INTEGER)')
        print('database connected, ready for operation')

        #create database work space 'Pages'
        cur.execute('''CREATE TABLE IF NOT EXISTS Pages
        (id INTEGER PRIMARY KEY, url TEXT UNIQUE, html TEXT,
         img BLOB, title TEXT)''')
        cur.close()
        return conn
        #

    def db_openup(self, db_name):
        """
        feature: connect to a existed db and open up created table, read data from 'URLs' table
        and insert data to Pages table
        """
        if db_name.endswith('sqlite'):
            conn = sqlite3.connect(db_name)
        else:
            conn = sqlite3.connect(db_name + ".sqlite")
        return conn



class Scheduler:

    def __init__(self, conn):
        """
        initialize self. retrieved_link and self.ill_link
        """
        self.retrieved_list = list()
        self.ill_list = list()
        self.new_list = list()
        self.conn = conn

    def __str__(self):
        pass

    def update_list(self):
        cur = self.conn.cursor()
        cur.execute('SELECT url FROM URLs WHERE label=?',(RETRIEVED_LINK,))
        for item in cur:
            self.retrieved_list.append(item[0])

        cur.execute('''SELECT url FROM URLs WHERE label = ?''',(ILL_LINK,))
        for item in cur:
            self.ill_list.append(item[0])

        cur.execute('''SELECT url FROM URLs WHERE label =?''',(NEW_LINK,))
        for item in cur:
            if self.check_duplicate(item):
                self.new_list.append(item[0])


    def check_duplicate(self, url):
        """
        feature: cleaner keep a list of retrieved_link and ill_link, and return
        True if url if not in two list, return false otherwise
        """
        if (url in self.retrieved_list) or (url in self.ill_list):
            return False
        else:
            return True

    def feed_to_database(self, url_list):
        cur = self.conn.cursor()
        for url in url_list:
            if self.check_duplicate(url):
                cur.execute('INSERT OR IGNORE INTO URLs(url, label) VALUES(?, ?)',
                (url, NEW_LINK))
                self.conn.commit()




def process_core(conn):
    global num_id

    s = Scheduler(conn)
    s.update_list()
    count = 0
    for url in s.new_list:
        cur = conn.cursor()
        print("### num_id = ", num_id)
        status = wheels(url, conn)
        if status == WHEELS_SUCC:
            num_id += 1
            count += 1
        elif status == WHEELS_GETCONTENTFAIL:
            cur.execute('''UPDATE URLs SET label=? WHERE url=?''', (ILL_LINK, url))
            conn.commit()
            count += 1
        elif status == WHEELS_GETURLFAIL:
            # page already retrieved, try other pages
            cur.execute('''UPDATE URLs SET label=? WHERE url=?''', (RETRIEVED_LINK, url))
            conn.commit()
            num_id += 1
            count += 1
        else:
            print("stack at this url: ", url)
            print("current list of loop: ", len(s.new_list), s.new_list)
            break
    print("completed ", len(s.new_list), "urls, review details:", s.new_list)

    if count > len(s.new_list):
        return 0
    else:
        return 1


def wheels(url, conn):
    """
    input:  url should not contained in the database,
            num_id should fetch from latest 'Pages' id label
            conn normal
    """

    gap = random.random() * 10
    time.sleep(gap)
    c1 = Crawler(url)
    cur = conn.cursor()
    try:
        title = c1.get_title()
        image = c1.get_img(1, False)
        content = c1.get_content()
    except:
        print("wheels: ", url, "get title or image or content fail")
        # cur.execute('''UPDATE URLs SET label=? WHERE url=?''', (ILL_LINK, url))
        return WHEELS_GETCONTENTFAIL

    if len(content) > 200:
        cur.execute('INSERT OR IGNORE INTO Pages (id, url, html, img, title) VALUES(?, ?, ?, ?, ?)',(num_id, url, content, image, title))
        cur.execute('''UPDATE URLs SET label=? WHERE url=?''', (RETRIEVED_LINK, url))
        conn.commit()
    else:
        cur.execute('UPDATE URLs SET label=? WHERE url=?',(ILL_LINK, url))
        print("content is less than 200, pass")

    try:
        url_list = c1.get_url()
        cur.execute("""SELECT url from URLs""")
        exist_list = list()
        pure_list = list()
        for link in cur:
            exist_list.append(link[0])
        print("===>len of exist_list: ",len(exist_list))
        for url in url_list:
            if url not in exist_list:
                pure_list.append(url)
        if len(pure_list) < 1:
            print("no new link to insert")
            return WHEELS_GETURLFAIL

        s1 = Scheduler(conn)
        s1.feed_to_database(pure_list)
        print("===>len of pure_list", len(pure_list))
        del s1
    except:
        # cur.execute('''UPDATE URLs SET label=? WHERE url=?''', (ILL_LINK, url))
        print("wheels: ", url[:30], "get_url fail or feed_to_database fail")
        return WHEELS_GETURLFAIL

    del c1
    return WHEELS_SUCC


def scrap_to_new_database():
    global num_id

    num_id = 0
    t = Teller()
    url, web_count, DB_name = t.customer_service()
    conn = t.db_setup()

    c1 = Crawler(url)
    url_list = c1.get_url()
    del c1
    s = Scheduler(conn)
    s.feed_to_database(url_list)
    del s

    while True:

        flag = process_core(conn)

        if flag == 0:
            print("over loop!")
            break
        elif num_id > web_count - 1:
            print("mission completed")
            break
        elif flag == 1:
            pass
        else:
            print("unknown error, stop!")



def update_existed_database():
    """
    feature: insert data to already existed database and table
    """
    global num_id

    t = Teller()
    url, web_count, DB_name = t.customer_service()
    conn = t.db_openup(DB_name)

    cur = conn.cursor()
    cur.execute("""SELECT id FROM Pages ORDER BY id DESC LIMIT 0, 1""")
    num_id = cur.fetchone()[0]

    while True:

        flag = process_core(conn)

        if flag == 0:
            print("over loop!")
            break
        elif num_id > web_count - 1:
            print("mission completed")
            break
        elif flag == 1:
            pass
        else:
            print("unknown error, stop!")

update_existed_database()
