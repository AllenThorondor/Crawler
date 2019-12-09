#!/usr/bin/env python
# coding: utf-8

# In[20]:


from bs4 import BeautifulSoup as BS
import requests, re, urllib, sqlite3, os


# In[21]:


NEW_LINK = 1
RETRIEVED_LINK = 2
ILL_LINK = 3


# In[22]:


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
            print('')
            print('Program interrupted by user...')
        except:
            print("Unable to retrieve or parse page")
            
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
        print("img to retrive:",max_img)

        for tag in tags:
            imglink = re.findall('src="(.+?\.jpg)"', str(tag))
            if imglink != '':
                img_link_list.extend(imglink)
        print("total img link in page:",len(img_link_list))

        if max_img == 1:
            if str(img_link_list[0]).startswith("http"):
                urllib.request.urlretrieve(img_link_list[0],'%s.jpg'%temp_img)
            else:
                urllib.request.urlretrieve('http:'+img_link_list[0],'%s.jpg'%temp_img)
            fp = open('{}.jpg'.format(temp_img), 'rb')
            img = fp.read()
            fp.close()
            return img
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
            print("Done, image save:", save)
            return img_list
        else:
            print("image quantity limit:", len(img_link_list))
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
                    print("----", tag, "is something wrong")
                    continue
        return content

    def get_title(self):
        raw = self.soup.title
        title = re.findall('\n(.+?)\n', str(raw))
        return title[0].strip()

    def get_url(self):
        tags = self.soup('a')
        self.url_list = []
        for tag in tags:
            url = tag.get('href', None)
            if ( url != "") and ( str(url).startswith('javascript:') == False):
                if str(url).endswith("html"):
                    self.url_list.append(url)
        #print(self.url_list)
        return self.url_list

    def feed_to_database(self, conn, cursor):
        for url in self.url_list:
            cursor.execute('INSERT OR IGNORE INTO URLs(url, label) VALUES(?, ?)',(url, NEW_LINK))
            conn.commit()


# In[23]:


class Teller:
    """
     
    """
    
    def __init__(self):
        pass
        
    def __str__(self):
        pass
    
    def customer_service(self):
        """
        input: no input should give to an teller object, cause she will ask what she need in interaction
        output: self.url, self.web_site_count, self.DB_name
        
        feature: teller can only create table , but can not muse data in that table
        """
        # url insert
        self.url = input("the web site url: ")
        if len(self.url)<1 : 
            self.url = "http://tech.sina.com.cn/csj/2019-11-20/doc-iihnzahi2064482.shtml"
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
        """
        #database URLs table set up
        conn = sqlite3.connect('{}'.format(self.DB_name))
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS URLs')
        cur.execute('CREATE TABLE URLs(url TEXT UNIQUE, label INTEGER)')
        print('database connected, ready for operation')
        
        #create database work space 'Pages'
        cur.execute('''CREATE TABLE IF NOT EXISTS Pages
        (id INTEGER PRIMARY KEY, url TEXT UNIQUE, html TEXT,
         img BLOB, title TEXT)''')
        return conn, cur
        #


# In[24]:


def scrap_to_database():
    """
    input:
    output:
    features:
    """
    
    t = Teller()
    url, web_count, DB_name = t.customer_service()
    conn, cur = t.db_setup()
    
    #add in original urls in URLs table (by crawler only)
    c1 = Crawler(url)
    url_list = c1.get_url()
    c1.feed_to_database(conn, cur)
    
    #while condition start
    count = 0
    while True:
        if count > int(web_count):
            break
        cur.execute('''SELECT url, label FROM URLs''')
        
        num = 0
        webs = list()
        for row in cur:
            if (row[1] == NEW_LINK) and (num < 5):
                webs.append(str(row[0]))
                num += 1
        if len(webs) < 1:
            print("no available url in database")
            break
        #iterate all the links in webs
        for url in webs:
            #should insert sleep function to avoid IP block
            c1 = Crawler(url)
            try:
                title = c1.get_title()
                image = c1.get_img(1, False)
                content = c1.get_content()
            except:
                print("get title or image or content fail")
                title = ""
                image = None
                content = ""
                
                
            try:
                url_list = c1.get_url()
                c1.feed_to_database(conn, cur)
            except:
                cur.execute('''UPDATE URLs SET label=? WHERE url=?''', (ILL_LINK, url))
                print(url, "has unsolved problem")
                continue
                    
            if len(content) > 100:
                cur.execute('INSERT OR IGNORE INTO Pages (id, url, html, img, title) VALUES(?, ?, ?, ?, ?)',(count, url, content, image, title))
                cur.execute('''UPDATE URLs SET label=? WHERE url=?''', (RETRIEVED_LINK, url))
                count += 1
                print(count)
            conn.commit()


# In[25]:


scrap_to_database()


# In[ ]:





# In[ ]:





# In[5]:


url = "http://tech.sina.com.cn/csj/2019-11-20/doc-iihnzahi2064482.shtml"


# In[6]:


c1 = Crawler(url)


# In[7]:


t = Teller()


# In[8]:


t.customer_service()


# In[9]:


t.db_setup()


# In[10]:


c1.get_title()


# In[11]:


c1.get_content()


# In[14]:


c1.get_img(5,False)


# In[ ]:




