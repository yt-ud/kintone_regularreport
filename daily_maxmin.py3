import requests
import datetime
# pdf生成
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import cm
# 配列演算
import numpy as np
# グラフ生成
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import ticker
from matplotlib import dates as mdates


# 部屋番号リスト
roomnum = [1, 2, 3]
# レポート日
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
reportdate = str(yesterday)
# kintoneアクセスへのクエリ＆APIトークン
APP = "app=17"
DATE = "date%20%3D%20%22"+reportdate+"%22%20"
ASC = "order%20by%20%24id%20asc%20"
LIMIT = "limit%20500"
URL = []
for x in roomnum:
    QUERY = "query="+DATE+"and"+"%20room_id%20%3D%20%22"+str(x)+"%22%20"+ASC+LIMIT
    tmp = "https://garagelabo.cybozu.com/k/guest/5/v1/records.json?"+APP+"&"+QUERY
    URL.append(tmp)
API_TOKEN = "AIk30Q18ivSZNA97oW3PdCSnbPUdtVNtnXpGFZmp"
# pdf生成
pdffile = canvas.Canvas('./' + reportdate + '.pdf')
pdffile.saveState()
# A4サイズ
pdffile.setPageSize((21.0*cm, 29.7*cm))
# フォント登録
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
pdffile.setFont('HeiseiKakuGo-W5', 10)


# kintoneレコード取得
def get_kintone(url, api_token):
    headers = {"X-Cybozu-API-Token": api_token}
    resp = requests.get(url, headers=headers)
    return resp.json()
# 最高温度・湿度の計算
def cal_maximum(list):
    daily_max_dict = {
        "temp_maxvalue": list[0]['temp']['value'],
        "temp_maxtime": list[0]['time']['value'],
        "humi_maxvalue": list[0]['humi']['value'],
        "humi_maxtime": list[0]['time']['value']
    }
    for item in list:
        if item['temp']['value']>daily_max_dict['temp_maxvalue']:
            daily_max_dict["temp_maxvalue"] = item['temp']['value']
            daily_max_dict["temp_maxtime"] = item['time']['value']
        if item['humi']['value']>daily_max_dict['humi_maxvalue']:
            daily_max_dict["humi_maxvalue"] = item['humi']['value']
            daily_max_dict["humi_maxtime"] = item['time']['value']
    return daily_max_dict
# 最低温度・湿度の計算
def cal_minimum(list):
    daily_min_dict = {
        "temp_minvalue": list[0]['temp']['value'],
        "temp_mintime": list[0]['time']['value'],
        "humi_minvalue": list[0]['humi']['value'],
        "humi_mintime": list[0]['time']['value']
    }
    for item in list:
        if item['temp']['value']<daily_min_dict['temp_minvalue']:
            daily_min_dict["temp_minvalue"] = item['temp']['value']
            daily_min_dict["temp_mintime"] = item['time']['value']
        if item['humi']['value']<daily_min_dict['humi_minvalue']:
            daily_min_dict["humi_minvalue"] = item['humi']['value']
            daily_min_dict["humi_mintime"] = item['time']['value']
    return daily_min_dict
# 温度・湿度・時刻のリスト
def graph_records(list):
    temp = []
    humi = []
    time = []
    for item in list:
        temp.append(item['temp']['value'])
        humi.append(item['humi']['value'])
        time.append(item['time']['value'])
    return temp, humi, time
# グラフの設定、表示
def graph_plot(y1, y2, x, room):
    # 左図
    fig, (axL, axR) = plt.subplots(ncols=2, figsize=(6,1.5), dpi=200, sharex=True)
    axL.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    axL.plot(x, y1, linewidth=1)
    axL.tick_params(labelsize=6)
    axL.set_title(room, fontsize = 8)
    axL.set_xlabel('time', fontsize=8)
    axL.set_ylabel('temperature', fontsize = 8)
    axL.grid(True)
    # 右図
    axR.plot(x, y2, linewidth=1)
    axR.tick_params(labelsize=6)
    axR.set_xlabel('time', fontsize = 8)
    axR.set_ylabel('humidity', fontsize = 8)
    axR.grid(True)

if __name__ == "__main__":
    # get_kintone
    r = []
    max_list = []
    min_list = []
    for i, x in enumerate(roomnum):
        gettmp = get_kintone(URL[i], API_TOKEN)
        r.append(gettmp['records'])
        # cal_maximum, cal_minimum
        # 最大温度・湿度・時刻
        maxtmp = cal_maximum(r[i])
        max_list.append(maxtmp)
        # 最低温度・湿度・時刻
        mintmp = cal_minimum(r[i])
        min_list.append(mintmp)

    # pdf作成
    # 体裁部分
    y = str(yesterday.year)
    m = str(yesterday.month)
    d = str(yesterday.day)
    pdffile.drawString(1*cm, 28*cm, '株式会社　岩野　様')
    pdffile.drawString(1*cm, 27*cm, y+'年'+m+'月'+d+'日温度・湿度（時刻）状況')
    yy = str(today.year)
    mm = str(today.month)
    dd = str(today.day)
    pdffile.drawString(13*cm, 27*cm, '作成日：'+yy+'年'+mm+'月'+dd+'日')
    # 部屋１
    pdffile.drawString(1*cm, 26*cm, '部屋ID：１')
    value = max_list[0]['temp_maxvalue']
    time = max_list[0]['temp_maxtime']
    pdffile.drawString(6*cm, 26*cm, '最高温度(度)：'+value+'（'+time+'）')
    value = min_list[0]['temp_minvalue']
    time = min_list[0]['temp_mintime']
    pdffile.drawString(12*cm, 26*cm, '最低温度：'+value+'（'+time+'）')
    value = max_list[0]['humi_maxvalue']
    time = max_list[0]['humi_maxtime']
    pdffile.drawString(6*cm, 25.5*cm, '最高湿度(％)：'+value+'（'+time+'）')
    value = min_list[0]['humi_minvalue']
    time = min_list[0]['humi_mintime']
    pdffile.drawString(12*cm, 25.5*cm, '最低湿度：'+value+'（'+time+'）')
    # 部屋２
    pdffile.drawString(1*cm, 24.5*cm, '部屋ID：２')
    value = max_list[1]['temp_maxvalue']
    time = max_list[1]['temp_maxtime']
    pdffile.drawString(6*cm, 24.5*cm, '最高温度：'+value+'（'+time+'）')
    value = min_list[1]['temp_minvalue']
    time = min_list[1]['temp_mintime']
    pdffile.drawString(12*cm, 24.5*cm, '最低温度：'+value+'（'+time+'）')
    value = max_list[1]['humi_maxvalue']
    time = max_list[1]['humi_maxtime']
    pdffile.drawString(6*cm, 24*cm, '最高湿度：'+value+'（'+time+'）')
    value = min_list[1]['humi_minvalue']
    time = min_list[1]['humi_mintime']
    pdffile.drawString(12*cm, 24*cm, '最低湿度：'+value+'（'+time+'）')
    # 部屋３
    pdffile.drawString(1*cm, 23*cm, '部屋ID：３')
    value = max_list[2]['temp_maxvalue']
    time = max_list[2]['temp_maxtime']
    pdffile.drawString(6*cm, 23*cm, '最高温度：'+value+'（'+time+'）')
    value = min_list[2]['temp_minvalue']
    time = min_list[2]['temp_mintime']
    pdffile.drawString(12*cm, 23*cm, '最低温度：'+value+'（'+time+'）')
    value = max_list[2]['humi_maxvalue']
    time = max_list[2]['humi_maxtime']
    pdffile.drawString(6*cm, 22.5*cm, '最高湿度：'+value+'（'+time+'）')
    value = min_list[2]['humi_minvalue']
    time = min_list[2]['humi_mintime']
    pdffile.drawString(12*cm, 22.5*cm, '最低湿度：'+value+'（'+time+'）')
    pdffile.restoreState()

    # 時刻を文字列型からdatetime型に変換
    for i in r:
        for j in i:
            tmp = datetime.datetime.strptime(j['time']['value'], '%H:%M')
            j['time']['value'] = tmp.time()

    # グラフ生成
    # 部屋１    
    temp, humi, time = graph_records(r[0])
    temp = list(map(float, temp))
    humi = list(map(float, humi))
    graph_plot(temp, humi, time, 'room1')
    plt.savefig(reportdate+'_room1.png')
    pdffile.drawInlineImage(reportdate+'_room1.png', 0, 450, width=600, height=170)
    # 部屋２
    temp, humi, time = graph_records(r[1])
    temp = list(map(float, temp))
    humi = list(map(float, humi))    
    graph_plot(temp, humi, time, 'room2')
    plt.savefig(reportdate+'_room2.png')
    pdffile.drawInlineImage(reportdate+'_room2.png', 0, 260, width=600, height=170)
    # 部屋３
    temp, humi, time = graph_records(r[2])
    temp = list(map(float, temp))
    humi = list(map(float, humi))
    graph_plot(temp, humi, time, 'room3')
    plt.savefig(reportdate+'_room3.png')
    pdffile.drawInlineImage(reportdate+'_room3.png', 0, 70, width=600, height=170)

    # フッターの作成
    pdffile.rect(0, 0, 600, 40, fill=True)
    pdffile.setFillColorRGB(1, 1, 1)
    pdffile.drawString(0.5*cm, 0.5*cm, 'Copyright© 2019 GARAGELABO All Rights Reserved.')
    pdffile.drawInlineImage('GL_logo.png', 335, 6)



    pdffile.save()