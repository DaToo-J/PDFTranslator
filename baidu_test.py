# coding=utf-8

import hashlib
from urllib import parse
import random
import requests
import urllib3
from configuration import userAppid,userSecretKey
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def English_to_Chinese(text):
    appid = userAppid #你的appid
    secretKey = userSecretKey #你的密钥

    # --------------------------------------------
    httpClient = None
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    q = text
    fromLang = 'en'
    toLang = 'zh'
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode(encoding='utf-8'))
    sign = m1.hexdigest()
    url = url + '?appid=' + appid + '&q=' + \
        parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + \
        '&salt=' + str(salt) + '&sign=' + sign
    # --------------------------------------------
    headers = {
        'Connection': 'close',
    }
    r = requests.get(url, headers=headers)

    result_after = []
    if r.status_code == 200:
        result = eval(r.content)
        for i in result['trans_result']:
            result_after.append(i['dst'])
        return result_after
    else:
        return None
        
if __name__ == '__main__':
    pass

