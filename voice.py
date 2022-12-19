import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import sys
import SRS
import time
import re
COM_PORT = "COM3" # USB-串口端口，需要在设备管理器中手动查看并修改
#由于语音识别返回的十及以下的数字为汉字，故建立以下键值对数组
num_list = {'一' : 1, '二' : 2, '三' : 3, '四' : 4, '五' : 5, '六' : 6, '七' : 7, '八' : 8, '九' : 9,'十':10}
#正则匹配的规则
str = "[一二三四五六七八九十]"
#该函数用于初始化模块，prot为端口号
def Init(PORT):
    try:
        # C2S03设备默认波特率9600、偶校验、停止位1
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT,baudrate=9600, bytesize=8, parity='E', stopbits=1))
        master.set_timeout(5.0)
        master.set_verbose(True)

        # 读输入寄存器
        # C2S03设备默认slave=2,指令为0x04, 起始地址=0, 输入寄存器个数2
        master.execute(2, cst.READ_INPUT_REGISTERS, 0, 2)

        # 读保持寄存器
        # C2S03设备默认slave=2,指令为0x03,起始地址=0, 保持寄存器个数1
        master.execute(2, cst.READ_HOLDING_REGISTERS, 0, 1)

        # 没有报错，返回1
        response_code = 1

    except Exception as exc:
        print(str(exc))
        # 报错，返回<0并输出错误
        response_code = -1
        master = None

    return response_code, master

def Switch(master, action):
    try:

        if "on" in action.lower():
            # 写单个线圈，状态常量为0xFF00，请求线圈接通,即output_value等于1
            # C2S03设备默认slave=2, 指令为0x05,线圈地址=0
            master.execute(2, cst.WRITE_SINGLE_COIL, 0, output_value=1)

        else:
            # 状态常量为0x0000，请求线圈断开,即output_value等于0
            master.execute(2, cst.WRITE_SINGLE_COIL, 0, output_value=0)

        # 没有报错，返回1
        response_code = 1

    except Exception as exc:
        print(str(exc))
        # 报错，返回<0并输出错误
        response_code = -1

    return response_code
def start(loop):
        # 检查串口继电器是否连接成功
        if loop == False:
            return ""
        response_code, master = Init(COM_PORT)
        if response_code > 0:
            print("串口继电器模块连接成功！")
        else:
            print("串口继电器模块连接失败，请排查原因！")
            exit()

        # 本次使用的语音识别系统为百度的语音识别系统，调用方式为调用百度提供的接口，调用时存在延迟，返回可能较慢
        while loop:
            print("=======================")
            print('您有3秒时间输入语音命令:')
            SRS.get_audio(3)  # 接收语音
            print('处理语音命令，可能较慢，请稍后')
            words = SRS.get_words() #返回语音识别结果到words
            print("你的命令是：" + words)
            #判断命令并执行相应的操作
            if "开" in words and "灯" in words: #开灯
                #延时开灯
                if "秒" in words:
                    if re.search(str,words) != None:
                        ans = re.search(str,words).group()
                        num = num_list.get(ans)
                        print("将在"+ans+"秒后打开电灯")
                        time.sleep(num)
                    else:
                        ans = re.search("\d",words).group()
                        print("将在"+ans+"秒后打开电灯")
                        time.sleep(int(ans))
                Switch(master, "on")
                if response_code > 0:
                    print("电灯开启成功！")
                else:
                    print("电灯开启失败，请检查USB串口连接！")
                    exit()
            if "关" in words and "灯" in words: #关灯
                #延时关灯
                if "秒" in words:
                    if re.search(str,words) != None:
                        ans = re.search(str,words).group()
                        num = num_list.get(ans)
                        print("将在"+ans+"秒后关闭电灯")
                        time.sleep(num)
                    else:
                        ans = re.search("\d",words).group()
                        print("将在"+ans+"秒后关闭电灯")
                        time.sleep(int(ans))
                Switch(master, "off")
                if response_code > 0:
                    print("电灯关闭成功！")
                else:
                    print("电灯关闭失败，请检查USB串口连接！")
                    exit()
            if "结束" in words and "运行" in words: #退出语音识别
                print("断开连接，欢迎下次使用")
                sys.exit()