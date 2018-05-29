#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import urllib3
import urllib3.exceptions as catch
import time
import urllib
import json
import hashlib
import base64
import getpass


class Requester():
    def __init__(self,requestURL,passcode,request_header,body):
        self.proxies_ips = [
            "10.24.129.241:8080",
            "10.24.163.218:8080"
        ]
        self.body = body
        self.login = os.getenv('username')
        self.passcode = passcode
        self.url = requestURL
        self.proxy_auth = '%(login)s:%(password)s' %{'login':self.login,'password':self.passcode}
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
        self.proxy_header = urllib3.make_headers(proxy_basic_auth=self.proxy_auth)
        self.request_header = request_header
        self.scheme = 'https' if self.url[:5]=='https' else 'http'
    def request(self,method):
        for ip in self.proxies_ips:
            proxy_str = '%(scheme)s://%(ip)s' %{"scheme":self.scheme,"ip":ip}
            proxy = urllib3.ProxyManager(proxy_str,timeout=10,proxy_headers=self.proxy_header,headers=self.request_header)
            try:
                r = proxy.request(method,self.url,fields=self.body)
                return r.data
            except catch.MaxRetryError as e:
                print(e)
            except catch.ProxyError as e:
                print(e)


def main():
    passcode = getpass.getpass("Passcode: ")
    image_path = os.path.join(os.getcwd(),'multi.jpg')
    f = open(image_path, 'rb')
    file_content = f.read()
    base64_image = base64.b64encode(file_content)
    #body = urllib.urlencode({'image': base64_image})
    body = {'image': base64_image}
    url = 'http://webapi.xfyun.cn/v1/service/v1/ocr/general'
    api_key = 'bab96523e2ecfc4443fd5d8810523066'
    param = {"language": "cn|en", "location": "false"}

    x_appid = '5b0b692b'
    x_param = base64.b64encode(json.dumps(param).replace(' ', ''))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5(api_key + str(x_time) + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    result = Requester(url,passcode,x_header,body).request('POST').decode('utf-8')
    #result = Requester.urlopen(req)
    #result = result.read()
    print result
    return

if __name__ == '__main__':
    main()