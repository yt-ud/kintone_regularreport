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
import matplotlib.pyplot as plt


# レポート日
reportdate = datetime.date.today() - datetime.timedelta(days=1)
reportdate = str(reportdate)

# pdf生成
pdffile = canvas.Canvas('./' + reportdate + '.pdf')
pdffile.saveState()
# A4サイズ
pdffile.setPageSize((21.0*cm, 29.7*cm))
# フォント登録
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
pdffile.setFont('HeiseiKakuGo-W5', 12)

# kintoneのクエリストリング＆APIトークン
URL = "https://garagelabo.cybozu.com/k/guest/5/v1/records.json?app=17&query=date%20%3D%20%22" + reportdate + "%22"
API_TOKEN = "AIk30Q18ivSZNA97oW3PdCSnbPUdtVNtnXpGFZmp"


# kintoneレコード取得
def get_kintone(url, api_token):
    headers = {"X-Cybozu-API-Token": api_token}
    resp = requests.get(url, headers=headers)
    return resp.json()

# 取得レコードをroom_idごとに（リスト）
def room_list(list):
    room1 = []
    room2 = []
    room3 = []
    for item in list:
        if item['room_id']['value']=='1':
            room1.append(item)            
        elif item['room_id']['value']=='2':
            room2.append(item)
        elif item['room_id']['value']=='3':
            room3.append(item)
    return room1, room2, room3

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

# 温度・湿度のグラフ表示
def graph_records(list):
    temp = []
    time = []
    for item in list:
        temp.append(item['temp']['value'])
        time.append(item['time']['value'])

    return temp, time



if __name__ == "__main__":
    # get_kintone
    t = get_kintone(URL, API_TOKEN)
    r = t['records']
    # room_list
    room1, room2, room3 = room_list(r)
    # cal_maximum, cal_minimum
    daily_list_max = []
    daily_list_min = []
    tmp = cal_maximum(room1)
    daily_list_max.append(tmp)
    tmp = cal_minimum(room1)
    daily_list_min.append(tmp)
    tmp = cal_maximum(room2)
    daily_list_max.append(tmp)
    tmp = cal_minimum(room2)
    daily_list_min.append(tmp)
    tmp = cal_maximum(room3)
    daily_list_max.append(tmp)
    tmp = cal_minimum(room3)
    daily_list_min.append(tmp)
    # pdfに書き込み
    # 部屋１
    pdffile.drawString(1*cm, 28*cm, '部屋ID：１')
    value = daily_list_max[0]['temp_maxvalue']
    time = daily_list_max[0]['temp_maxtime']
    pdffile.drawString(2*cm, 27*cm, '最高温度(度)：'+value+'（'+time+'）')
    value = daily_list_min[0]['temp_minvalue']
    time = daily_list_min[0]['temp_mintime']
    pdffile.drawString(10*cm, 27*cm, '最低温度：'+value+'（'+time+'）')
    value = daily_list_max[0]['humi_maxvalue']
    time = daily_list_max[0]['humi_maxtime']
    pdffile.drawString(2*cm, 26*cm, '最高湿度(％)：'+value+'（'+time+'）')
    value = daily_list_min[0]['humi_minvalue']
    time = daily_list_min[0]['humi_mintime']
    pdffile.drawString(10*cm, 26*cm, '最低湿度：'+value+'（'+time+'）')
    # 部屋２
    pdffile.drawString(1*cm, 25*cm, '部屋ID：２')
    value = daily_list_max[1]['temp_maxvalue']
    time = daily_list_max[1]['temp_maxtime']
    pdffile.drawString(2*cm, 24*cm, '最高温度：'+value+'（'+time+'）')
    value = daily_list_min[1]['temp_minvalue']
    time = daily_list_min[1]['temp_mintime']
    pdffile.drawString(10*cm, 24*cm, '最低温度：'+value+'（'+time+'）')
    value = daily_list_max[1]['humi_maxvalue']
    time = daily_list_max[1]['humi_maxtime']
    pdffile.drawString(2*cm, 23*cm, '最高湿度：'+value+'（'+time+'）')
    value = daily_list_min[1]['humi_minvalue']
    time = daily_list_min[1]['humi_mintime']
    pdffile.drawString(10*cm, 23*cm, '最低湿度：'+value+'（'+time+'）')
    # 部屋３
    pdffile.drawString(1*cm, 22*cm, '部屋ID：３')
    value = daily_list_max[2]['temp_maxvalue']
    time = daily_list_max[2]['temp_maxtime']
    pdffile.drawString(2*cm, 21*cm, '最高温度：'+value+'（'+time+'）')
    value = daily_list_min[2]['temp_minvalue']
    time = daily_list_min[2]['temp_mintime']
    pdffile.drawString(10*cm, 21*cm, '最低温度：'+value+'（'+time+'）')
    value = daily_list_max[2]['humi_maxvalue']
    time = daily_list_max[2]['humi_maxtime']
    pdffile.drawString(2*cm, 20*cm, '最高湿度：'+value+'（'+time+'）')
    value = daily_list_min[2]['humi_minvalue']
    time = daily_list_min[2]['humi_mintime']
    pdffile.drawString(10*cm, 20*cm, '最低湿度：'+value+'（'+time+'）')




    x, y = graph_records(room1)
    print(len(r))



    pdffile.restoreState()
    pdffile.save()
    