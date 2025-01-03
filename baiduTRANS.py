# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 17:08:52 2023

@author: wangzheng3
"""

#request模块中，通过往Request对象添加HTTP头，模拟浏览器发送post请求
from urllib import request
from urllib import parse
import json

def get_word():
    word = input('输入文字查找翻译：')
    while len(word) < 1:
        word = input('不能为空，请重新输入：')
    return word

def make_header(word):
    raw_data = {'kw': word}  #需要输入的data有哪些，被称作kw是如何知道的？F12的network中，sug的payload页面能够看到
    data = parse.urlencode(raw_data).encode('utf-8')
    req = request.Request(url = 'https://fanyi.baidu.com/sug', data = data)   #继续学习：我怎么知道网站的sug代表了那个文本输入框？在网页尝试操作，看network下的name会多出哪些项
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36')
    req.add_header('Cookie', 'BIDUPSID=1A9192918EA58125904BD08A0A3885E1; PSTM=1689666919; BAIDUID=1A9192918EA58125D1CE1A7155940804')  #登录百度翻译需校验baiduuid cookie，为空会导致翻译接口校验不通过（注意一年后过期）
    return req

def output_makeup(text):
        print('\n***以下是得到的翻译内容***')
        i = 0
        while i <len(text['data']):
            print('"%s" : %s;' %(text['data'][i]['k'], text['data'][i]['v'] ))
            i = i + 1
        print('*******结束*******\n')

def main():
    word = get_word()
    req = make_header(word)

    with request.urlopen(req) as f:
        print('Status:', f.status, f.reason)
        if (f.status == 200)&(f.reason == 'OK'):
            print('省略header信息...')
        else:
            for k, v in f.getheaders():  #继续学习：我怎么知道k和v代表网站的输入和输出内容？似乎是网站通用配置。通过浏览器F12的nework中，sug的response/preview页面预览到
                print('%s: %s' % (k, v))
        '''print('Data:', f.read().decode('utf-8'))'''
        text = json.loads(f.read().decode('utf-8'))
        output_makeup(text)


if __name__ == '__main__':
    while True :
        main()
        user_input = input("任意键回车继续，输入“exit”或“bye”退出程序...")
        if user_input.lower() == "exit" or user_input.lower() == "bye":
            break
        

