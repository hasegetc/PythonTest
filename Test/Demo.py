# -*- coding: utf-8 -*-
__author__ = 'liuyuchao'

import re
import os
from urllib.request import urlopen
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
import functools
import time


from bs4 import BeautifulSoup

# 创建新目录/http://www.22ddrr.com/html/article/254399.html
def mkdir(path):
    path = path.strip()
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print(u"偷偷新建了名字叫做",path,u'的文件夹')
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(u"名为",path,'的文件夹已经创建成功')
        return False


# # 传入图片地址，文件名，保存单张图片
# def saveImg(imageURL,fileName):
#      u = urllib.request.urlopen(imageURL)
#      data = u.read()
#      f = open(fileName, 'wb')
#      f.write(data)
#      print(u"正在悄悄保存她的一张图片为",fileName)
#      f.close()

def saveImgByUrl(url, doc):
    imgName = url[url.rindex("/"):]
    imgName = doc + imgName
    # saveImg(url, doc + imgName)
    try:
        print(url)
        data = urlopen(url).read()
        f = open(imgName, 'wb')
        f.write(data)
        print(u"正在悄悄保存她的一张图片为", imgName)
        f.close()
    except Exception as e:
        print(e)
        return

def imgWithoutWidth(tag):
    return tag.name == 'img' and not tag.has_attr('width')

url = "http://www.22ddrr.com/html/article/254399.html"
while 1:


    try:

        print("处理如下链接：" + url)


        response = urlopen(url)
        soup = BeautifulSoup(response.read(), 'html.parser')
        url = "http://www.22ddrr.com" + soup.select(".next > h3 > a")[0]['href']
        title = soup.title.string

        mkdir(title)
        urlset = set()
        for i in soup.find_all(imgWithoutWidth):
            urls=re.findall('src="?\'?([^"\'>]*)',str(i),re.I)
            for i in urls:
                urlset.add(i)

        # for i in urlset:
        #     imgName = i[url.rindex("/"):]
        #     saveImg(i, title + imgName)

        # Make the Pool of workers
        pool = Pool(4)
        # Open the urls in their own threads
        # and return the results
        saveImgWithUrl = functools.partial(saveImgByUrl, doc=title)

        results = pool.map(saveImgWithUrl, urlset)
        # close the pool and wait for the work to finish
        pool.close()
        pool.join()

        time.sleep(1)
        print("next url %s " % url)
        if(len(url) == 0):
            break
    except Exception as e:
        print(e)
        continue

