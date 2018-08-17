
# -*- coding: UTF-8 -*-
import os
import time
#import urllib
#import json
import hashlib
import base64
import getpass
import wave
import urllib3
import urllib3.exceptions as catch
import requests
import simplejson as json
from pyaudio import PyAudio, paInt16
from naoqi import ALProxy
frame_rate = 16000
channel = 1
bite = 2
record_time = 60
num_sample = 1600
tts = ALProxy("ALTextToSpeech", "192.168.2.7", 9559)

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
def save_wave_file(filename,data):
    wf = wave.open(filename,'wb')
    wf.setnchannels(channel)
    wf.setsampwidth(bite)
    wf.setframerate(frame_rate)
    wf.writeframes(b"".join(data))
    wf.close()
def my_record():
    pa = PyAudio()
    stream = pa.open(format=paInt16,channels=channel,rate=frame_rate,input=True,frames_per_buffer=num_sample)
    my_buf = []
    count = 0
    t1 = time.clock()
    try:
        while count < int(frame_rate/num_sample*record_time):
            string_audio_data = stream.read(num_sample,exception_on_overflow=False)
            if count == 0:
                print('start your show, press ctrl+c to stop')
            my_buf.append(string_audio_data)
            count+=1
        print('max time recording reached')
    except KeyboardInterrupt:
        print('\nrecording stopped')
    t2 = time.clock()
    length = t2-t1
    print(length)
    stream.stop_stream()
    stream.close()
    pa.terminate()

    save_wave_file('a.wav',my_buf)
    return 'a.wav'
def sc_main():
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
    print(result)
    return
def general_main():
    URL = "http://openapi.xfyun.cn/v2/aiui"
    APPID = "5aa8940e"
    API_KEY = "22f5227158494de7bafff4e38acba802"
    AUE = "raw"
    AUTH_ID = "efed1fb964694ce4be1f2d9fe01e1973"
    DATA_TYPE = "audio"
    SAMPLE_RATE = "16000"
    SCENE = "main"
    RESULT_LEVEL = "plain"
    LAT = "39.938838"
    LNG = "116.368624"
    #个性化参数，需转义
    PERS_PARAM = "{\\\"auth_id\\\":\\\"efed1fb964694ce4be1f2d9fe01e1973\\\"}"
    FILE_PATH = my_record()


    def buildHeader():
        curTime = str(int(time.time()))
        param = "{\"result_level\":\""+RESULT_LEVEL+"\",\"auth_id\":\""+AUTH_ID+"\",\"data_type\":\""+DATA_TYPE+"\",\"sample_rate\":\""+SAMPLE_RATE+"\",\"scene\":\""+SCENE+"\",\"aue\":\""+AUE+"\",\"lat\":\""+LAT+"\",\"lng\":\""+LNG+"\"}"
        #使用个性化参数时参数格式如下：
        #param = "{\"result_level\":\""+RESULT_LEVEL+"\",\"auth_id\":\""+AUTH_ID+"\",\"data_type\":\""+DATA_TYPE+"\",\"sample_rate\":\""+SAMPLE_RATE+"\",\"scene\":\""+SCENE+"\",\"lat\":\""+LAT+"\",\"lng\":\""+LNG+"\",\"pers_param\":\""+PERS_PARAM+"\"}"
        paramBase64 = base64.b64encode(param)

        m2 = hashlib.md5()
        m2.update(API_KEY + curTime + paramBase64)
        checkSum = m2.hexdigest()

        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': APPID,
            'X-CheckSum': checkSum,
        }
        return header

    def readFile(filePath):
        binfile = open(filePath, 'rb')
        data = binfile.read()
        return data

    r = requests.post(URL, headers=buildHeader(), data=readFile(FILE_PATH))
    x = json.loads(r.content,encoding='utf-8')
    for el in x['data']:
        if el['sub']=='nlp' and el['intent']!={}:
            if el['intent']['rc']==0:
                result = u"Your question: {0};\n Answer: {1}".format(el['intent']['text'],el['intent']['answer']['text'])
                answer = (0,el['intent']['answer']['text'])
            else:
                result = u"Your question: {0};\n Answer: NO ANSWER {1}".format(el['intent']['text'],el['intent']['rc'])
                answer = (1,'这个问题我还不会回答')
    #print(answer)
    tts.say(answer[1].encode('utf-8') if answer[0]==0 else answer[1])
    print(result)

if __name__ == '__main__':
    while True:
        if raw_input('press ENTER to start recording:: ')!="":
            break
        general_main()