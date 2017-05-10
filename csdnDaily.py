#_*_coding:utf8_*_

import urllib2,urllib
from bs4 import BeautifulSoup
import os,threading

'''
创建一个csdn_daily的对象，实现了对于每天日报中文章的链接爬取
'''
class csdn_daily(object):

    def __init__(self,csdn_url='http://blog.csdn.net/column/details/14549.html?&page=1'):
        self.page_urls = []                             #放页面中视频地址的列表
        self.article_urls = []                          #放下载视频地址的列表
        self.column_url = csdn_url                      #爬虫的专栏入口链接
        self.domain = 'http://www.csdn.net'             #域名
        self.article_date = []                          #存储日报日期
        self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.15 Safari/537.36'}

    def __request(self,url):
        self.url = url                                                      #传入进来的url地址
        self.req = urllib2.Request(url=self.url,headers=self.header)        #url的request请求头
        self.page_info = urllib2.urlopen(self.req).read().decode('utf-8')   #html的源码
        self.soup = BeautifulSoup(self.page_info,'html.parser')             #实例化soup对象，以bs4的格式化实现
        return self.soup

    def _get_page_urls(self):                                               #得到日报页面的地址
        self.search_list = self.__request(self.column_url)
        self.ul_list = self.search_list.find_all('ul', attrs={"class": "detail_list"})
        for ul in self.ul_list:
            self.a_list = ul.find_all('a')                                  #得到当前页面中的a标签的列表
            for a in self.a_list:
                try:
                    url = a['href']                                         #获取a标签中的href的内容
                except Exception as e:
                    pass
                else:
                    if url.startswith('http://blog.csdn.net/blogdevteam/article/details/'):  #得到a标签href中的以固定形式开头的内容
                        self.page_urls.append(url)                              #把正确的匹配结果放到日报页的列表中

        return self.page_urls                   

    def _get_article_urls(self):                                            #得到博文链接地址
        self.urls = self._get_page_urls()
        tmp_urls = []                                                       #新建一个临时列表，用来存放每个页面的博文链接，方便去重后添加到self.article_urls
        for page in self.urls:
            soup = self.__request(page)
            title = str(soup.find('title'))[17:26]
            self.article_urls.append('----%s----\n'%title)
            div_list = soup.find_all('div', attrs={"id":"article_content","class": "article_content"})
            for div in div_list:
                article_list = div.find_all('a')
                for article_url in article_list:
                    try:
                        url =  article_url['href']
                    except Exception as e:
                        pass
                    else:
                        if url.startswith('http://blog.csdn.net') and ('article/details/' in url) and ('broadview2006' not in url):
                            tmp_urls.append(url+'\n')
            self.article_urls.extend(list(set(tmp_urls)))
            tmp_urls = []

        return self.article_urls

    def saveArticleUrls(self,save_path):  #保存博文链接的方法
        self.save_path = save_path
        self._get_article_urls()
        with open(self.save_path, 'w') as f:
            for url in self.article_urls:
                f.writelines(url)
                print '%s saved..'%url

def getDesktopPath():
	return os.path.join(os.path.expanduser("~"), 'Desktop')

if __name__ == '__main__':
    csdnDaily = csdn_daily()   #实例化
    savePath = getDesktopPath() + r'\articleUrls.txt'
    #print savePath
    csdnDaily.saveArticleUrls(savePath)

