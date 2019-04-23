import requests
import json

URL = "https://garagelabo.cybozu.com:443"
APP_ID = "43"
API_TOKEN = "wLluORI6jnG2HBIqN2JrOkJqQR8mQIZrJQphqDwQ"
KNT_PASS = "eS51ZWRhOmFwb2xsbzE5Njk="


class KINTONE:
    def UploadToKintone(self, url, knt_pass,path,filename):
        tmp = open(path + filename, 'rb')
        files={'file':(filename,tmp,'pdf')}
#        files={'file':(filename,tmp,'png')}
        headers = {"X-Cybozu-Authorization": knt_pass , 'X-Requested-With': 'XMLHttpRequest'} 
        resp=requests.post(url+"/k/v1/file.json",files=files,headers=headers)

        return resp 

    def PostToKintone(self,url,appId,apiToken,filekey):
        record = {
            "daily_report":{'type':"FILE","value" :[{'fileKey':filekey}]}
            #他のフィールドにデータを挿入する場合は','で区切る
        }
        data = {'app':appId,'record':record}
        headers = {"X-Cybozu-API-Token": apiToken, "Content-Type" : "application/json"}
        resp=requests.post(url+'/k/v1/record.json',json=data,headers=headers)

        return resp

if __name__ == '__main__':
    # ファイル保存パス
    Path='/Users/yutaueda/Developments/Work/Garagelabo/Codes/Python/Iwano/kintone_regularreport/kintone_regularreport/'
    # ファイル名
    FileName='2019-04-21.pdf'


    knt=KINTONE()
    resp=knt.UploadToKintone(URL, KNT_PASS,Path,FileName)

    txt=json.loads(resp.text)
    FileKey=txt['fileKey']
    resp=knt.PostToKintone(URL, APP_ID, API_TOKEN,FileKey)
    print(resp.text)