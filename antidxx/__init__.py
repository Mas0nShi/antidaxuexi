# -*- coding:utf-8 -*-
"""
@Author: Mas0n
@File: __init__.py
@Time: 2022/5/27 17:51
@Desc: It's all about getting better.
"""
from os.path import split as psiplt, realpath, join as pjoin
from requests import Session
from mloguru import logger
from datetime import datetime as dat
from time import strftime as fmt_time, strptime as parse_time
from bs4 import BeautifulSoup
from collections import deque

Version = '1.0.0'
Nl_Join = lambda _s: '\n'.join(_s)
Url_Task_List = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current"

req = Session()
req.headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; ELS-AN00 Build/HUAWEIELS-AN00; wv) AppleWebKit/537.36 (KHTML, "
                  "like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/045811 Mobile Safari/537.36 "
                  "MMWEBID/9942 MicroMessenger/8.0.11.1980(0x28000B3B) Process/tools WeChat/arm64 Weixin "
                  "NetType/WIFI Language/zh_CN ABI/arm64 "
}
Base = psiplt(realpath(__file__))[0]
Template_Message = open(pjoin(Base, "template/message.txt"), "r", encoding="utf-8").read()
Template_Staffs_Group = open(pjoin(Base, "template/staffs.txt"), "r", encoding="utf-8").read().splitlines()
Is_Rotate = Template_Staffs_Group.pop()
Template_Staffs = deque([line.split("|") for line in Template_Staffs_Group])
Template_Sections = open(pjoin(Base, "template/sections.txt"), "r", encoding="utf-8").read().splitlines()
Regex_Start_Div = '<div class="section0 topindex">'
Regex_End_Div = '<script type="text/javascript" src="js'
Option = "ABCDEFG"


@logger.catch
def check_task_update() -> (bool, object):
    """
    check the task update in this week.
    :return: True if the task release or False.
    """
    current = req.get(url=Url_Task_List).json()
    assert current["status"] == 200
    date_diff = (dat.now().date() - dat.strptime(current["result"]["startTime"], "%Y-%m-%d %H:%M:%S").date()).days
    return (True, current) if date_diff < 7 else (False, current)


@logger.catch
def generate_answers(uri: str) -> str:
    """
    generate answers
    :param uri:
    :return:
    """
    # forced request m.html
    res = req.get(url=uri if uri.endswith('m.html') else uri.replace('index.html', 'm.html')).text
    res = res[res.find(Regex_Start_Div):res.rfind(Regex_End_Div) - 4]
    bs = BeautifulSoup(res, 'lxml')
    answers = [[elm.get("data-a") for elm in div.find_all("div") if elm.get("data-a") is not None] for div in bs.find("body") if div != '\n']
    logger.trace(f'step 1: data getting: {answers}')
    for i, answer in enumerate(answers):
        if len(answer) > 4:
            answers[i] = answer[:len(answer) // 2]
    answers = deque(answers)
    logger.trace(f'step 2: data cleaning: {answers}')
    while not answers[0]:
        answers.popleft()
    required = []
    optional = []
    while len(answers) != 0 and answers[0]:
        required.append(answers.popleft())
    if len(answers) != 0:
        answers.popleft()
    while answers:
        optional.append(answers.popleft())
    logger.trace(f'step 3: data splits: {required} / {optional}')
    required = ['{num}. {opt}'.format(num=idx + 1, opt="".join([Option[i] for i, v in enumerate(answer) if v == '1'])) for idx, answer in enumerate(required)]
    optional = ['{num}. {opt}'.format(num=idx + 1, opt="".join([Option[i] for i, v in enumerate(answer) if v == '1'])) for idx, answer in enumerate(optional)]
    logger.trace(f'step 4: generate answer options: {required} / {optional}')
    return f'课堂练习\n{Nl_Join(required)}\n课外习题\n{Nl_Join(optional)}\n'


def generate_staff_group() -> str:
    """
    generate staff groups with queue.
    :return: text.
    """
    global Is_Rotate
    logger.trace(Template_Staffs)
    staffs = []
    for idx, section in enumerate(Template_Sections):
        tmp_st_gp = Template_Staffs[idx]
        staffs.append(f"{section}: {tmp_st_gp[0]}")
        if Is_Rotate == "1":
            tmp_st_gp[0], tmp_st_gp[1] = tmp_st_gp[1], tmp_st_gp[0]
            Template_Staffs[idx] = tmp_st_gp
    if Is_Rotate == "0":
        Template_Staffs.append(Template_Staffs.popleft())
    Is_Rotate = "1" if Is_Rotate == "0" else "0"
    open(pjoin(Base, "template/staffs.txt"), "w", encoding="utf-8").write('{staffs}\n{rot}'.format(staffs=Nl_Join(["|".join(staff) for staff in Template_Staffs]), rot=Is_Rotate))
    return Nl_Join(staffs)


@logger.catch
def generate_notices(_o: object, _staffs: str, _answers: str) -> str:
    date = fmt_time("%m月%d日", parse_time(_o["endTime"], "%Y-%m-%d %H:%M:%S"))
    return Template_Message.format(title=_o["title"], date=date, staffs=_staffs, answers=_answers)


def generate(stdout=False) -> str:
    is_release, obj = check_task_update()
    if is_release:
        logger.success(f"this week's task has been released.")
        staff_list = generate_staff_group()
        logger.trace(staff_list)
        vre = generate_answers(obj["result"]["uri"])
        msg = generate_notices(obj["result"], staff_list, vre)
        if stdout:
            logger.success(msg)
    else:
        logger.info(f"this week's task has not yet been released.")
        return "Fail"
    return msg


if __name__ == '__main__':
    generate(stdout=True)
