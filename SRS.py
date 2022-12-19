# encoding:utf-8
import base64
import json
import requests 
import pyaudio
import wave
from urllib.request import urlopen
from urllib.request import Request

client_id = 'Pc4FvxRBCTfdKI9z527URR5D'
client_secret = 'aQ3lHzlAd1EUQAUOo1rYNIypKNBOY4uE'

#Python实现录音
def get_audio(sec):
    #创建对象
    p = pyaudio.PyAudio()
    #创建流：采样位，声道数，采样频率，input= True，缓冲区
    stream = p.open(format=pyaudio.paInt16,channels=1,rate = 16000,input = True,frames_per_buffer=1024)
    #创建式打开音频文件
    wf = wave.open('switch.wav','wb')
    #设置音频文件的属性:采样位，声道数，采样频率
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setnchannels(1)
    wf.setframerate(16000)
    for w in range(int(16000*sec/1024)):
        data = stream.read(1024)
        wf.writeframes(data)
    #停止并关闭流
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()
    return 'switch.wav'

def get_words():
    #获取Access Token
    url_token = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+ client_id + '&client_secret='+client_secret
    #向网址进行请求
    response = requests.post(url = url_token)
    #将结果放入result中
    result = response.json()
    #获得token
    token = result['access_token']

    #设置网址
    host = 'http://vop.baidu.com/server_api'
    #音频文件存储位置,即识别的音频文件
    file = '.\switch.wav'
    #将文件转码为base64
    data = open(file,'rb').read()
    base_data = base64.b64encode(data).decode('utf-8')
    length = len(data)

    params={
        "format":"wav",
        "rate":16000,
        "dev_pid":1537,
        "channel":1,
        "token":token,
        "cuid":"231312baidu_workshop",
        "len":length,
        "speech":base_data
    }
    #将数据转为json结构
    data = json.dumps(params,sort_keys = False)
    #响应，并获取结果
    response = Request(host,data.encode('utf-8'))
    result = urlopen(response)
    result = result.read().decode('utf-8')
    str = eval(result)["result"][0]
    return str