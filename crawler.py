__author__ = 'LHQ'
# -*- coding:utf-8 -*-
import urllib
import urllib.error
import urllib.request
import re


# 百度贴吧爬虫类
class BDTB:

    # 初始化，传入基地址，是否只看楼主的参数
    def __init__(self, baseUrl, fileName):
        self.baseURL = baseUrl
        self.page = self.getPage(self.baseURL, 0)
        self.tool = Tool()
        self.file = open(fileName, 'w')
        #print(self.page)

    def getAllContent(self):
        num = int(self.getNumOfPosts())
        print("该贴吧共有"+str(num)+"贴")
        index = 0
        while num > 0:
            pattern = re.compile('<a rel=.*? href="/p/(.*?)" title="(.*?)".*?</a>', re.S)
            urls = re.findall(pattern, self.page)
            index += len(urls)
            self.page = self.getPage(self.baseURL, index)
            num -= len(urls)
            if urls:
                for url in urls:
                    print('title'+url[1])
                    currUrl = 'https://tieba.baidu.com/p/'+url[0]+'?'
                    print(currUrl)
                    currPage = self.getPage(currUrl, 0)
                    numPage = self.getNumOfPages(currPage)
                    self.getContent(currUrl, 1, int(numPage))


    # 传入页码，获取该页帖子的代码
    def getPage(self, url, pageNum):
        try:
            pn = ''
            if pageNum:
                pn = '&pn='+str(pageNum)
            url = url + pn
            response = urllib.request.urlopen(url)
            return response.read().decode('utf-8')
        except urllib.error.URLError as e:
            if hasattr(e, "reason"):
                print(u"连接百度贴吧失败,错误原因", e.reason)
                return None

    def getTitle(self):
        pattern = re.compile('<title>(.*)</title>', re.S)
        result = re.search(pattern, self.page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getNumOfPosts(self):
        pattern = re.compile('共有主题数<span class="red_text">(.*?)</span>', re.S)
        result = re.search(pattern, self.page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getNumOfPages(self, currPage):
        pattern = re.compile('<span class="red">(.*?)</span>', re.S)
        result = re.search(pattern, currPage)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getContent(self, url, startPage, endPage):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        posts = []
        for i in range(startPage, endPage+1):
            page = self.getPage(url, i);
            post = re.findall(pattern, page)
            for rep in post:
                if rep != '':
                    text = self.tool.replace(rep)
                    posts.append(text)
                    self.file.writelines(text)
        return posts


# 处理页面标签类
class Tool:
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    # remove slashes and backslashes
    removeSlash = re.compile('/|\\\\')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.removeSlash, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()


baseURL = 'https://tieba.baidu.com/f?ie=utf-8&kw=%E7%8E%8B%E7%82%B8%E7%9A%84%E9%BA%BB%E8%A2%8B'
bdtb = BDTB(baseURL, 'wangzhademadai.txt')
bdtb.getAllContent()
