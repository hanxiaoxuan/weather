# -*- coding: utf-8 -*-
from aip import AipSpeech
import requests
import re
from bs4 import BeautifulSoup
import time
import datetime
import commands
import os
'''
爬取天气网-chuzhou
http://www.weather.com.cn/weather/101190201.shtml
'''
def getHtmlText(url,code='utf-8'):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ''
def makeSoup(html):
    wstr = ''
    #print html
    if html == '':
        return '哎呀~今天我也不知道滁州天气了'
    else:
        soup = BeautifulSoup(html,'html.parser')
        soup1 = soup.find_all('li',attrs = {'class':'on'})[1]
        str1 = re.findall(r'>(.*)</',str(soup1))
        b = ''
        try:
            slist = re.findall(r'^(.*)</span>(.*)<i>(.*)$',str1[4])
            #print slist
            for x in range(len(slist[0])):
                b += slist[0][x]
        except:
            b = str1[4]
        if '/' in b:
            b = b.replace('/','-')
        str1[4] = '滁州的温度是'+b
        #print(str1[4])
        str1[6] = '小风风是'+str1[6]
        for i in str1:
            if i != '':
                wstr = wstr +i
        if '雨' in wstr:
            wstr += '今天一定要有好心情！'
        #print(wstr)
        return wstr
'''
用百度的AIP
把文字变成mp3文件
'''
def stringToMp3(strings_txt):
    strings_txt = '起床了~韩哥~起床啊,韩哥~~~要上班啦！今天是  ' + '2018年8月'+datetime.datetime.now().strftime('%d')+strings_txt
    APPID = '11626606'
    APIKey = 'yzcBEk1fz6G3LI2mTIFyk8Md'
    SecretKey = 'maHA7mT06BzYqOw5fo20aaH162nBTB55'

    aipSpeech = AipSpeech(APPID,APIKey,SecretKey)
    result = aipSpeech.synthesis(strings_txt,'zh','1',\
                                {'vol':8,
                                'per':0,
                                'spd':3})
    if not isinstance(result,dict):
        with open('test_tmp.mp3','wb') as f:
            f.write(result)

'''
执行的主函数
'''
def main():
    #url = 'http://www.weather.com.cn/weather/101190201.shtml'
    url='http://www.weather.com.cn/weather/101221101.shtml'
    #url ='http://nb.zj.weather.com.cn'
    html=getHtmlText(url)
    stringToMp3(makeSoup(html))
    os.system('mplayer test_tmp.mp3')
    
if __name__ == '__main__':
    main()
