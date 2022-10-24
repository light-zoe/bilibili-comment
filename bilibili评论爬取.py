import requests
import time
import json
import logging

table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr={}
for i in range(58):
	tr[table[i]]=i
s=[11,10,3,8,4,6]
xor=177451812
add=8728348608

#解码bvid
def dec(x):
	r=0
	for i in range(6):
		r+=tr[x[s[i]]]*58**i
	return (r-add)^xor


replyUrl = 'https://api.bilibili.com/x/v2/reply/main'
replyReplyUrl = "https://api.bilibili.com/x/v2/reply/reply"


bvid = input("输入bv\n")
filte = input("输入过滤词(空字符表示不过滤)\n")
filte = filte.strip()
avid = dec(bvid)
print(f"avid = {avid}")

repls = []

nextPage = 0

isError = False

#二级回复
def secondryReply(rpid):
    pn = 1
    ps = 20
    rs = []
    while(True):
        r = requests.get(replyReplyUrl,params={"type":1,"oid":avid,"root":rpid,"pn":pn,"ps":ps})
        if r.status_code != 200:
            raise Exception("r.status_code != 200")
        resp = r.json()
        if resp["code"] == 0:
            data = resp["data"]
            page = data["page"]
            count = page["count"]
            if not data["replies"] is None:
                rs += data["replies"]
                for reply in data["replies"]:
                    content = reply["content"]["message"]
                    print("===============")
                    print(content)
            if pn * ps >= count:
                break
            else:
                pn += 1
        else:
            raise Exception("resp.code != 0")
        time.sleep(0.3)
    for r in repls:
        if r["rpid"] == rpid:
            r["replies"] = rs

while True:
    print(f"start-------第{nextPage}页----------start")
    try:
        r = requests.get(replyUrl,params={"type":1,"oid":avid,"next":nextPage})
        if r.status_code != 200:
            raise Exception("r.status_code != 200")
        
        resp = r.json()
        
        if resp["code"] == 0:
            data = resp["data"]
            if "replies" in data and isinstance(data["replies"], list) :
                repls += data["replies"]
                for reply in data["replies"]:
                    content = reply["content"]["message"]
                    if filte in content: 
                        print(content)
                        if reply["count"] > 0:  
                            # 二级评论
                            print("--------回复start---------")
                            secondryReply(reply["rpid"])
                            print("--------回复end---------")
                        print("-----------------")
            if data["cursor"]["is_end"]:
                break
            else:
                nextPage = data["cursor"]["next"]
        else:
            raise Exception("resp.code != 0")
    except BaseException as e:
        print("发生错误")
        logging.exception(e)
        isError = True
        break
    time.sleep(0.3)
    print(f"end-------第{nextPage}页----------end")

with open("raw.json","w") as f:
    f.write(json.dumps(repls))

input("---end---")
