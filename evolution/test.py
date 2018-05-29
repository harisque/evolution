#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib2
import time
import urllib
import json
import hashlib
import base64


def main():
    f = open("IMAGE_PATH", 'rb')
    file_content = f.read()
    base64_image = base64.b64encode(file_content)
    body = urllib.urlencode({'image': base64_image})

    url = 'http://webapi.xfyun.cn/v1/service/v1/ocr/handwriting'
    api_key = 'bab96523e2ecfc4443fd5d8810523066'
    param = {"language": "a", "location": "true"}

    x_appid = '5b0b692b'
    x_param = base64.b64encode(json.dumps(param).replace(' ', ''))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5(api_key + str(x_time) + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib2.Request(url, body, x_header)
    result = urllib2.urlopen(req)
    result = result.read()
    print result
    return


if __name__ == '__main__':
    main() 