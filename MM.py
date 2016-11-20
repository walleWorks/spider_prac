#!/usr/bin/env python2
# -*- coding:utf-8 -*-
__author__ = 'jhao'

import urllib
import urllib2
import re
import tool
import os

#抓取MM
class Spider:

    #页面初始化
    def __init__(self):
        self.siteURL = 'http://www.meizitu.com/a/list_1_'
        self.tool = tool.Tool()

    #获取索引页面的内容
    def getPage(self,pageIndex):
        url = self.siteURL +  str(pageIndex) + ".html"
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('gbk')

    #获取索引界面所有MM的信息，list格式
    def getContents(self,pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile('<div class="pic".*?<a.*?href="(.*?)"><img',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            contents.append(item)
        return contents

    #获取MM个人详情页面
    def getDetailPage(self,infoURL):
        response = urllib2.urlopen(infoURL)
        return response.read().decode('gbk')

    #获取个人文字简介
    def getBrief(self,page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        result = re.search(pattern,page)
        return self.tool.replace(result.group(1))

    #获取页面所有图片
    def getAllImg(self,page):
        pattern = re.compile('<div id="picture">.*?<p>(.*?)</p>.*?</div>',re.S)
        #个人信息页面所有代码
        content = re.search(pattern,page)
        #从代码中提取图片
        patternImg = re.compile('<img.*?src="(.*?)"',re.S)
        images = re.findall(patternImg,content.group(1))
        return images


    #保存多张写真图片
    def saveImgs(self,images,name):
        number = 1
        print u"第",name,u"美",u"共有",len(images),u"张照片"
        for imageURL in images:
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = name + "/" + str(number) + "." + fTail
            self.saveImg(imageURL,fileName)
            number += 1

    # 保存头像
    def saveIcon(self,iconURL,name):
        splitPath = iconURL.split('.')
        fTail = splitPath.pop()
        fileName = name + "/icon." + fTail
        self.saveImg(iconURL,fileName)

    #保存个人简介
    def saveBrief(self,content,name):
        fileName = name + "/" + name + ".txt"
        f = open(fileName,"w+")
        print u"正在偷偷保存她的个人信息为",fileName
        f.write(content.encode('utf-8'))


    #传入图片地址，文件名，保存单张图片
    def saveImg(self,imageURL,fileName):
        print imageURL
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
        headers = { 'User-Agent' : user_agent,'Cookie':'__jsluid=4e20473ab5ba881b9e653d82476753a2'}
        request = urllib2.Request(imageURL,None,headers)
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            print(e.code)
            return
        except urllib2.URLError, e:
            print(e.args)
            return
        data = response.read()
        f = open(fileName, 'wb')
        f.write(data)
        print u"正在悄悄保存她的一张图片为",fileName
        f.close()


    #创建新目录
    def mkdir(self,path):
        path = path.strip()
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists=os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            print u"偷偷新建了名字叫做",path,u'的文件夹'
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print u"名为",path,'的文件夹已经创建成功'
            return False

    #将一页淘宝MM的信息保存起来
    def savePageInfo(self,pageIndex):
        #获取第一页
        contents = self.getContents(pageIndex)
        number = 1
        for item in contents:
            #个人详情页面的URL
            detailURL = item
            #得到个人详情页面代码
            detailPage = self.getDetailPage(detailURL)
            #获取个人简介
            images = self.getAllImg(detailPage)
            numstr = str(number)
            self.mkdir(numstr)
            #保存个人简介
            #self.saveBrief(brief,item[2])
            #保存图片

            self.saveImgs(images,numstr)
            number += 1


    #传入起止页码，获取MM图片
    def savePagesInfo(self,start,end):
        for i in range(start,end+1):
            print u"正在偷偷寻找第",i,u"个地方，看看MM们在不在"
            self.savePageInfo(i)


#传入起止页码即可，在此传入了2,10,表示抓取第2到10页的MM
spider = Spider()
spider.savePagesInfo(1,1)
