
import pandas as pd
import requests
import time
from datetime import datetime, timedelta
import json
import urllib.request

today = datetime.now()
print(today.strftime('%Y-%m-%d'))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
URL_JUCHAO = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'

HEADER = {
    "User-Agent" : UA,
    "Origin"       : "http://www.cninfo.com.cn",
    "Referer": "http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search&lastPage=index",
#     "Upgrade-Insecure-Requests": "1",
    "Cookie": "JSESSIONID=BED249E810CBFB8FD1591D8E2A3C6C3F; _sp_ses.2141=*; _sp_id.2141=6e8c8a15-2bef-44da-85ef-7a61731b0422.1623140236.1.1623140256.1623140236.0ad58ae7-a29c-426c-b11a-4e04ebdd1d9f; routeId=.uc1",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive"
}

# pageNum: current page
# searchKey: 回购, etc.
# seDate: 开始~结束
str_parameter = "pageNum={}&pageSize=30&column=szse&tabName=fulltext&plate=&stock=&searchkey=%E5%9B%9E%E8%B4%AD&secid=&category=&trade=&seDate={}~{}&sortName=&sortType=&isHLtitle=true"
str_parameter.format('1', today.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))
print(str_parameter.format('1', today.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')))

s = requests.Session()

i = 1
while True:
    try:
        r = s.post(URL_JUCHAO, data = str_parameter.format('1', today.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')), headers = HEADER, verify=False)
        if r.status_code == 200 and len(r.text) > 0:
            break
        time.sleep(5 * i)
        i = i + 1
    except Exception as e:
        print(e)
        pass

dic_result = r.json()
print(dic_result.get('totalRecordNum'))
lt_announcements = dic_result.get('announcements')
32
if len(lt_announcements) > 0:
    for announcement in lt_announcements:
        print(announcement.get('secCode'), announcement.get('secName'), announcement.get('announcementTitle'))
        urllib.request.urlretrieve('http://static.cninfo.com.cn/' + announcement.get('adjunctUrl'), announcement.get('announcementTitle').replace('<em>', '').replace('</em>','') + ".pdf")


