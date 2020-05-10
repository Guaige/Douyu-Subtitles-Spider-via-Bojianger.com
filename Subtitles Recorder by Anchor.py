import requests
import time


def fetch_sub(rid, date):
    url = "https://www.bojianger.com/data/api/auth/anchor_detail_danmu.do?date=" + date + "&rid=" + rid + "&uid=0" + "&order=-1&time=-1&duration=0+~24&pageNum=1&pageSize=20"
    ret = requests.get(url, headers=header)
    user = ret.json()['data']['name']
    try:
        pages = int(ret.json()['data']['page']['pages'])
        totalcount = int(ret.json()['data']['page']['totalCount'])
        last_count = totalcount - 20*(pages-1)
        filename = "直播间_" + user + '_' + date + ".txt"
        file = open(filename, "w", encoding='utf-8')
        file.write(user + "\r弹幕数 : "+str(totalcount)+'\r')
        for i in range(1, pages+1):
            url = "https://www.bojianger.com/data/api/auth/anchor_detail_danmu.do?date=" + date + "&rid=" + rid + "&uid=0" + "&order=-1&time=-1&duration=0+~24&pageNum=" + str(i)
            ret = requests.get(url, headers=header)
            if i == pages:
                range_num = last_count
            else:
                range_num = 20
            for j in range(0, range_num):
                if len(ret.json()['data']['page']['rows'][j]['uname']) > 4:
                    str_tab = "\t\t"
                else:
                    str_tab = "\t\t\t"
                file.write(ret.json()['data']['page']['rows'][j]['update_time'] + '\t' + ret.json()['data']['page']['rows'][j]['uname'] + str_tab)
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
date = year_month + day
date_prev = year_month + str(int(day)-1)
file_rid = open("rid.txt", encoding='utf8')
while 1:
    rid = file_rid.readline()
    if rid == '':
        break
    fetch_sub(rid, date)
    fetch_sub(rid, date_prev)
file_rid.close()


