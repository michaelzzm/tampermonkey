# May need to run "python -m pip install requests" first
import requests 
import time
from datetime import datetime, timedelta
import json
import urllib.request
import os
import sys
import urllib.parse

today = datetime.now()
yesterday = today - timedelta(days=1)
print(today.strftime('%Y-%m-%d'), yesterday.strftime('%Y-%m-%d'))

# Define data file path
file_path = 'C:\\上市公司公告\\回购\\'
if len(sys.argv) > 1:
    file_path = sys.argv[1]
print(file_path)

if not os.path.exists(file_path + today.strftime('%Y-%m-%d')):
    os.makedirs(file_path + today.strftime('%Y-%m-%d'))
# CNINFO's metadata
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
str_parameter = "pageNum={}&pageSize=30&column=szse&tabName=fulltext&plate=&stock=&searchkey=" + urllib.parse.quote('回购') + "&secid=&category=&trade=&seDate={}~{}&sortName=&sortType=&isHLtitle=true"
# str_parameter.format('1', today.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))

ALL_STOCKS_INFO = "http://www.cninfo.com.cn/new/data/szse_stock.json"

# Start to extract pdfs
s = requests.Session()
page = 1

while True:
    i = 1
    while True:
        try:
            r = s.post(URL_JUCHAO, data = str_parameter.format(str(page), yesterday.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')), headers = HEADER, verify=False)
            if r.status_code == 200 and len(r.text) > 0:
                break
            time.sleep(5 * i)
            i = i + 1
        except Exception as e:
            print(e)
            pass

    dic_result = r.json()
    
    print('Page', page)
    
    lt_announcements = dic_result.get('announcements')
    if len(lt_announcements) > 0:
        for announcement in lt_announcements:
            print(announcement.get('secCode'), announcement.get('secName'), announcement.get('announcementTitle'))
            if announcement.get('announcementTitle').find('法律意见') < 0:
                urllib.request.urlretrieve('http://static.cninfo.com.cn/' + announcement.get('adjunctUrl'), file_path + today.strftime('%Y-%m-%d') + '/' + announcement.get('secCode') + '_' + announcement.get('secName') + '_' + announcement.get('announcementTitle').replace('<em>', '').replace('</em>','') + ".pdf")

    if page > int(dic_result.get('totalRecordNum') / 30):
        print('Total', dic_result.get('totalRecordNum') ,'records. Done!')
        break
    else:
        page = page + 1

