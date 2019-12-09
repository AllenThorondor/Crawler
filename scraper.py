#!/usr/bin/env python
# coding: utf-8

# In[13]:


from bs4 import BeautifulSoup as BS
import requests, re, urllib


# In[14]:


url = "http://tech.sina.com.cn/csj/2019-11-20/doc-iihnzahi2064482.shtml"


# In[15]:


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
        try:
            url_handler = requests.get(link_url, timeout=3)
            self.soup = BS(url_handler.content, 'html.parser')
        except KeyboardInterrupt:
            print('')
            print('Program interrupted by user...')
        except:
            print("Unable to retrieve or parse page")

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

    def feed_to_database(self, cursor):
        for url in self.url_list:
            cursor.execute('INSERT OR IGNORE INTO URLs(url, label) VALUES(?, ?)',(url, NEW_LINK))


# In[ ]:



def online():
    pass

# In[57]:





# In[56]:





# In[79]:





# In[80]:





# In[73]:





# In[93]:






# In[94]:





# In[ ]:





# In[ ]:





# In[ ]:
