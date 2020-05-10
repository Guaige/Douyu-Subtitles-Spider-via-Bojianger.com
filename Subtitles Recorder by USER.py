import requests
import time


def get_page(totalcount):
    return int(totalcount/20)+1


def lastcount(totalcount):
    return totalcount%20


def fetch_sub(uid, date):
    url = "https://www.bojianger.com/data/api/auth/audience_detail_danmu.do?date=" + date + "&rid=0&uid=" + uid + "&order=-1&time=-1&duration=0+~24&pageNum=1&pageSize=20"
    ret = requests.get(url, headers=header)
    user = ret.json()['data']['name']
    try:
        totalcount = int(ret.json()['data']['page']['totalCount'])
        filename = user + '_' + date + ".txt"
        file = open(filename, "w", encoding='utf-8')
        file.write(user + "\r弹幕数 : "+str(totalcount)+'\r')
        for i in range(1, get_page(totalcount)+1):
            url = "https://www.bojianger.com/data/api/auth/audience_detail_danmu.do?date=" + date + "&rid=0&uid=" + uid + "&order=-1&time=-1&duration=0+~24&pageNum=" + str(i)
            ret = requests.get(url, headers=header)
            if i == get_page(totalcount):
                range_num = lastcount(totalcount)
            else:
                range_num = 20
            for j in range(1, range_num):
                if len(ret.json()['data']['page']['rows'][j]['anchorName']) > 4:
                    str_tab = "\t\t"
                else:
                    str_tab = "\t\t\t"
                file.write(ret.json()['data']['page']['rows'][j]['update_time'] + '\t' + ret.json()['data']['page']['rows'][j]['anchorName'] + str_tab)
                file.write(ret.json()['data']['page']['rows'][j]['txt']+'\r')
                print('\r' + ret.json()['data']['page']['rows'][j]['txt'], end='', flush=True)
        file.close()
    except KeyError:
        print("\rNo Data\t" + user + '\t' + date)


header = {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzI0MDM3MTI5NSIsImlhdCI6MTU4ODY4OTE0MSwiZXhwIjoxNTg5MjkzOTQxfQ.70F5VVeE4bSRgX4n2g23V3VmAIk-4_QBxBTJ1MpisZn6oUb_edHCIxV6VWLMg9urjSwLzDZDq3xPJQ8ruXgNcg",
}
year_month = time.strftime("%Y-%m-", time.localtime())
day = time.strftime("%d", time.localtime())
#time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
uid = "17444333"
date = year_month + day
date_prev = year_month + str(int(day)-1)
file_uid = open("uid.txt", encoding='utf8')
while 1:
    uid = file_uid.readline()
    if uid=='':
        break
    fetch_sub(uid, date)
    fetch_sub(uid, date_prev)
file_uid.close()


