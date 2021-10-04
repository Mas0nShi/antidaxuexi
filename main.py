# -*- coding:utf-8 -*-
"""
@Author: Mas0n
@File: info.py
@Time: 2021-09-06 12:23
@Desc: It's all about getting better.
"""
import json
import time
import datetime
import requests as http
from bs4 import BeautifulSoup

startsStr = b""" <div class="section0 topindex">"""
endStr = b'<script type="text/javascript" src="js/order.js"></script>'
optionCond = "ABCDEF"
condTemplate = "{num}. {check}"
msgTemplate = """各位团支书，{title} 青年大学习已经开始了！务必及时通知到班级。注意：这次要求全班所有同学都要做！操作步骤与上次相同。注意：这次我们要收取班级里同学的截图并且在截图上写上名字，然后各个团支书将截图发给对应的组织部干事并且汇报人数情况，在这周日中午前（{day}）将截图和具体情况汇报给组织部相应干事。
{staffList}
注意：不完成的话将会做以下处理：团员不完成不做推优，已是预备党员或者发展对象，放入待观察处理，停滞一年推优！
"""


def writeStaffJson():
    template = {"18": ["a1", "a2"], "19": ["b1", "b2"], "20": ["c1", "c2"], "21": ["d1", "d2"], "check": 0}
    data = json.dumps(template)
    with open("staffs.json", "w") as f:
        f.write(data)
    return data


def checkStaff():
    with open("staffs.json", "r") as f:
        rd = f.read()
    staff = None
    try:
        staff = json.loads(rd)
    except json.JSONDecodeError:
        raise "staff json decode error"
    return staff


def checkUpdate():
    url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current"
    res = http.get(url=url, headers={
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; ELS-AN00 Build/HUAWEIELS-AN00; wv) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/045811 Mobile Safari/537.36 "
                      "MMWEBID/9942 MicroMessenger/8.0.11.1980(0x28000B3B) Process/tools WeChat/arm64 Weixin "
                      "NetType/WIFI Language/zh_CN ABI/arm64 "
    })

    try:
        jStr = res.json()
    except json.JSONDecodeError:
        jStr = {"status": -1}

    if jStr["status"] != 200:
        raise "error"

    # print(json.dumps(jstr, indent=4, ensure_ascii=False))
    return jStr


def genStaffList(staffs: dict):

    StaffList = ""

    for k in staffs:
        if k == "check":
            break
        staff = "{period}级: 组织部 {people}\n".format(period=k, people=staffs[k][staffs["check"]])
        StaffList += staff
    return StaffList[:-1]


def rewriteStaffList(staffs: dict):
    staffs["check"] ^= 1
    with open("staffs.json", "w") as f:
        f.write(json.dumps(staffs))


def parserHtml(url):
    content = http.get(url=url).content
    answerArrs = {"required": [], "optional": []}
    tmp = []
    # print(content.decode())
    sindex = content.find(startsStr)
    eindex = content.rfind(endStr)
    if sindex == -1 or eindex == -1:
        return []
    soup = BeautifulSoup(content[sindex:eindex], 'lxml', from_encoding='utf-8')
    for div in soup.find("body"):
        if div == "\n":
            continue
        answer = []
        for i in div.find_all("div"):
            check = i.get("data-a")
            if check is not None:
                answer.append(check)

        if len(answer) > 4:
            answer = answer[:int(len(answer) / 2)]
        tmp.append(answer)
        # print("--------------------------------------------------------")

    field = "required"
    out = True
    for i, v in enumerate(tmp):
        if out and len(v) == 0 and i > 0 and len(tmp[i - 1]) != 0:
            field = "optional"
            out = False
            continue
        if len(v) != 0:
            answerArrs[field].append(v)

    # process
    output = ""
    if len(answerArrs["required"]) > 0:
        for i, v in enumerate(answerArrs["required"]):
            checks = ""
            for j, v2 in enumerate(v):
                if v2 == "1":
                    checks += optionCond[j]

            output += condTemplate.format(num=i + 1, check=checks)
            output += "\n"

    if len(answerArrs["optional"]) != 0:
        output += "课外习题\n"
        for i, v in enumerate(answerArrs["optional"]):
            checks = ""
            for j, v2 in enumerate(v):
                if v2 == "1":
                    checks += optionCond[j]
            output += condTemplate.format(num=i + 1, check=checks)
            output += "\n"


    # print(answerArrs)
    return output


def testFunc():
    data = http.get("https://h5.cyol.com/special/weixin/sign.json").json()
    for d in data:
        print(data[d]["url"])
        print(parserHtml(data[d]["url"]))


def genMsgText():
    msg = checkUpdate()
    now = datetime.datetime.now()
    st = datetime.datetime.strptime(msg["result"]["startTime"], "%Y-%m-%d %H:%M:%S")
    days = (now - st).days
    if days < 7:
        t = time.strptime(msg["result"]["endTime"], "%Y-%m-%d %H:%M:%S")
        formatDay = time.strftime("%m月%d日", t)
        staffMaps = checkStaff()

        staffList = genStaffList(staffMaps)
        rewriteStaffList(staffMaps)
        rMsg = msgTemplate.format(title=msg["result"]["title"], day=formatDay, staffList=staffList)
        parseAnswer = parserHtml(msg["result"]["uri"])
    else:
        rMsg = "本周暂未更新大学习"
        parseAnswer = None

    return rMsg, parseAnswer


response, answer = genMsgText()
print(response)
print(answer)



