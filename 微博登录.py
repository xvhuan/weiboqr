import time
import requests
import re
import json
from PIL import Image
from io import BytesIO

#  --二维码获取
qrAllUrl = 'https://login.sina.com.cn/sso/qrcode/image?entry=weibo&size=180&callback=STK_' + str(int(time.time()))
qrJson = json.loads(re.findall(r'[(](.*?)[)]', requests.get(qrAllUrl).text)[0])["data"]
qrUrl = qrJson['image']
qrId = qrJson['qrid']
qrEcho = BytesIO(requests.get('https:' + qrUrl).content)
Image.open(qrEcho).show()
#  --扫码验证
qrCheckUrl = 'https://login.sina.com.cn/sso/qrcode/check?entry=sso&qrid=' + qrId + '&callback=STK_' + str(
    int(time.time()))
qrCheckResponse = ''
while 'succ' not in qrCheckResponse:
    qrCheckResponse = requests.get(qrCheckUrl).text
    time.sleep(2)
altUrl = json.loads(re.findall(r'[(](.*?)[)]', qrCheckResponse)[0])['data']['alt']
coreUrl = 'https://login.sina.com.cn/sso/login.php?entry=qrcodesso&returntype=TEXT&crossdomain=1' \
          '&cdult=3&domain=weibo.com&alt=' + altUrl + '&savestate=30&callback=STK_' + str(int(time.time()))
loginUrl = requests.get(coreUrl).headers
weiboCookies = dict(loginUrl)['Set-Cookie']
print('SUB=' + re.findall('SUB=(.*?);', weiboCookies)[0])  # 有用的cookie
