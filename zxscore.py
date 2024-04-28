#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 4/28/2024 8:55 PM
# @Author : tiantian520
# @Description: 通过解析html获得智学网分数
# @Joke: 致敬传奇程序员jmning，它在2019/3/12为我们留下了机会（
#         他的代码：<!--屏蔽题卡未关联试题解析页得分相关信息 -edited by jmning 2019/3/12-->
#         滑稽的注释屏蔽法(

import requests
import lxml
import json
from bs4 import BeautifulSoup


# 登录智学网PC端，点击成绩报告，历次学情中本次的考试，选择全科页面/单科页面，右键 另存为(save as) 保存到本文件目录下方，名为page.html
# 查询各题分析情况：点开“解析” 右键 另存为(save as) 保存到本文件目录下方，名为page.html
html = open("page.html", 'r', encoding="UTF-8").read()

# 考试总分
totalScore = 800
# 单科总分
singleScore = 100

#搜索类型 1: 总分 0: 单科 2: 单科各题分析
searchType = 2

soup = BeautifulSoup(html, 'html.parser')

print('='*20 + '智学网SearcherV1' + '='*20)

# 分析考生资料
# <span id="paperCommitTime">2024-04-28</span>
print("考生姓名：", str(soup.find(name='span', attrs={"id":"userName"})).split('>')[1].replace('</span', ''))

if searchType == 1:
    print("分析总分：")
    print(totalScore * float(str(soup.find_all(name='div',attrs={"class":"class-running"})).replace('[<div class="class-running" style="left: ', '').split(';')[0].replace('%','')) / 100)
    if (totalScore * float(str(soup.find_all(name='div',attrs={"class":"class-running"})).replace('[<div class="class-running" style="left: ', '').split(';')[0].replace('%','')) / 100) % 0.5 != 0:
        print("[?] 分数似乎存在误差。它可能更趋向于", round(totalScore * float(str(soup.find_all(name='div',attrs={"class":"class-running"})).replace('[<div class="class-running" style="left: ', '').split(';')[0].replace('%','')) / 100), 'Points.')
elif not searchType:
    print("分析单科分数：")
    print(str(soup.find_all(name='div', attrs={"class":"zx-tab-item tab-item current-tab"})).replace('[<div class="zx-tab-item tab-item current-tab" data-v-b19093d6=""><div class="zx-tab-item-label"><span data-v-b19093d6="" style="position: relative; display: inline-block;"><span data-v-b19093d6="">', '').split("</span>")[0], end=': ')
    print(singleScore * float(str(soup.find_all(name='div',attrs={"class":"class-running"})).replace('[<div class="class-running" style="left: ', '').split(';')[0].replace('%','')) / 100)
    if (singleScore * float(str(soup.find_all(name='div',attrs={"class":"class-running"})).replace('[<div class="class-running" style="left: ', '').split(';')[0].replace('%','')) / 100) % 0.5 != 0:
        print("[?] 分数似乎存在误差。它可能更趋向于", round(singleScore * float(str(soup.find_all(name='div',attrs={"class":"class-running"})).replace('[<div class="class-running" style="left: ', '').split(';')[0].replace('%','')) / 100), 'Points.')
elif searchType == 2:
    print("逐题分析中...")
    scoreSum = 0
    avgSum = 0
    for question in soup.find_all(name='div', attrs={"class":"tk_analytic_item mt10"}):
        scoreSum += float(str(question.find(name='div', attrs={"class":"total"})).split('<em class="green">')[1].split('</em>')[0])
        avgSum += float(str(question.find(name='div', attrs={"class":"total"})).split('满分')[1].split('分')[0]) * float(str(question.find(name='div', attrs={"class":"total"})).split('<i>')[1].split('</i>')[0].replace('%','')) / 100
        print("第", str(question.find(name='span', attrs={"class":"fl"})).replace('<span class="fl">','').replace("</span>", ""), "题")
        print('    得分：', str(question.find(name='div', attrs={"class":"total"})).split('<em class="green">')[1].split('</em>')[0])
        print('    总分：', str(question.find(name='div', attrs={"class":"total"})).split('满分')[1].split('分')[0])
        print('    扣分：', float(str(question.find(name='div', attrs={"class":"total"})).split('满分')[1].split('分')[0]) - float(str(question.find(name='div', attrs={"class":"total"})).split('<em class="green">')[1].split('</em>')[0]))
        print('    班级平均得分率：', str(question.find(name='div', attrs={"class":"total"})).split('<i>')[1].split('</i>')[0])
        print('    你的得分率：', str(question.find(name='div', attrs={"class":"total"})).split('<i>')[2].split('</i>')[0])
    print("本卷得分：", str(scoreSum))
    print("班级均分：", str(avgSum))
