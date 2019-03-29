import requests

URL = "https://garagelabo.cybozu.com/k/guest/5/v1/records.json?app=17&query=date%20%3D%20TODAY()"
API_TOKEN = "AIk30Q18ivSZNA97oW3PdCSnbPUdtVNtnXpGFZmp"

def get_kintone(url, api_token):
    # get record of today
    headers = {"X-Cybozu-API-Token": api_token}
    resp = requests.get(url, headers=headers)
    
    with open('resp.txt', 'w') as f:
        f.write(resp.text)

    return type(resp.text)


if __name__ == "__main__":
    RESP = get_kintone(URL, API_TOKEN)

#    print(RESP.text)
    print(RESP)