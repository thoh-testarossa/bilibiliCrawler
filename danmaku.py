#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import sqlite3
import time
import requests
from bs4 import BeautifulSoup


def WriteData(aid=None, cid=None, data=None):
    try:
        aid = int(aid)
        cid = int(cid)
        if not data:
            return None
    except TypeError:
        return None
    try:
        #danmaku_date, danmaku_time, danmaku_type, danmaku_font, danmaku_color, danmaku_crc, danmaku_string, danmaku_7
        #curs.execute('''CREATE TABLE IF NOT EXISTS danmakulist 
        #    (Aid INT, Cid INT, DDate CHAR(20), DTime FLOAT, Type INT, Font INT, Color CHAR(10), Crc CHAR(10), String CHAR(1000), Se7en INT PRIMARY KEY)''')
        ins = 'INSERT OR REPLACE INTO danmakulist VALUES({aid}, {cid}, ?, ?, ?, ?, ?, ?, ?, ?)'.format(aid=aid, cid=cid)
        curs.execute(ins, data)
        database.commit()
    except:
        print('sql error')


def GetDanmaku(aid=None, page=None):
    if not page:
        page = 1
    try:
        aid = int(aid)
    except TypeError:
        return None
    url = "http://www.bilibili.com/widget/getPageList?"
    params = {'aid': aid}
    # headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"}
    response = requests.get(url=url, params=params, timeout=300)
    try:
        plist = json.loads(response.text)
        for i in range(len(plist)):
            cid = plist[i]['cid']
            # print(cid)
            url_danmu = 'http://comment.bilibili.com/{cid}.xml'.format(cid=cid)
            danmu_xml = requests.get(url=url_danmu, timeout=300)
            content = BeautifulSoup(danmu_xml.text, "xml")
            # <d p="190.56399536133,5,25,15138834,1465868252,0,61dba469,1957402211">弹幕字幕</d>
            danmaku_raw = [x for x in content.select('i')[0].select('d')]
            danmaku_string = [x.string for x in danmaku_raw]
            danmaku_attrs = [x.attrs['p'] for x in danmaku_raw]
            danmaku_time = [float(x.split(',')[0]) for x in danmaku_attrs]
            danmaku_type = [int(x.split(',')[1]) for x in danmaku_attrs]
            danmaku_font = [int(x.split(',')[2]) for x in danmaku_attrs]
            danmaku_color = [("#%06x" % int(x.split(',')[3], 10)).upper() for x in danmaku_attrs]
            danmaku_date = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(x.split(',')[4]))) for x in danmaku_attrs]
            # danmaku_5 = [x.split(',')[5] for x in danmaku_attrs]
            danmaku_crc = [x.split(',')[6] for x in danmaku_attrs]
            danmaku_7 = [int(x.split(',')[7]) for x in danmaku_attrs]
            danmaku_data = list(zip(danmaku_date, danmaku_time, danmaku_type, danmaku_font, danmaku_color, danmaku_crc, danmaku_string, danmaku_7))
            for danmaku in danmaku_data:
                try:
                    WriteData(aid, cid, danmaku)
                    # print(danmaku)
                except UnicodeEncodeError:
                    pass
    except:
        pass

def GetMaxID():
    url = 'http://www.bilibili.com/newlist.html'
    tmp = requests.get(url=url)
    html = BeautifulSoup(tmp.text, 'lxml')
    maxid = html.select('li[class=l1]')[0].a.attrs['href'].replace('/video/av','').replace('/','')
    return int(maxid)


if __name__ == "__main__":
    try:
        database = sqlite3.connect('danmaku.db')
        curs = database.cursor()
        curs.execute('''CREATE TABLE IF NOT EXISTS danmakulist 
            (Aid INT, Cid INT, DDate CHAR(20), DTime FLOAT, Type INT, Font INT, Color CHAR(10), Crc CHAR(10), String CHAR(1000), Se7en INT PRIMARY KEY)''')
        curs.execute('''SELECT MAX(Aid) FROM danmakulist''')
        rows = curs.fetchall()
        minid, = rows[0] if rows[0] != (None,) else (1,)
    except:
        minid = 1
    maxid = GetMaxID();
    for avid in range(minid - 1, maxid):
        print(avid)
        GetDanmaku(avid)
    #GetDanmaku(3110165)
