import PySimpleGUI as sg
import voice
import threading
#定义ui界面
def ui():
    #设置主题
    sg.theme("Dark Brown")
    #设置布局
    layout = [
                [sg.Text("=====欢迎使用声控灯系统=====",size=(64,1),justification='center'),
                sg.Button(key="-stop-",image_filename=("close-little.png"),border_width=0,image_subsample=7,
                button_color=(sg.theme_background_color()))],
                [sg.Text("操作指南：")],
                [sg.Text("点击打开声控系统后大声说出语音指令即可控灯，点击关闭声控系统，可以结束程序运行")],
                [sg.Text("语音指令中含有开灯字样可以开启电灯，语音指令中含有关灯字样可以关闭电灯，")],
                [sg.Text("同时系统实现了延时开关灯，目前支持以秒为单位延时开关,例说出“1秒后关灯”，电灯将在1秒后关闭")],
                [sg.Text("说出指令“结束运行”也可以关闭声控系统")],
                [sg.Text("----------------------------------------------",size=(100,1),justification='center')],
                [sg.Button("打开声控系统",size=(100,1),)],
                [sg.Button("关闭声控系统",size=(100,1))],
                [sg.Text("----------------------------------------------",size=(100,1),justification='center')],
                [sg.Text("声控系统反馈提示：")],
                [sg.Output(size=(500,280))]
            ]
    windows = sg.Window("基于声控的电灯开关系统", layout,size=(580,500))
    while True:
        event, values = windows.read()
        if  event is None or event == "-stop-": #当按下×时，触发事件结束程序
            break
        elif event == '关闭声控系统': #按下“关闭声控系统”按钮时向start()传入False来关闭声控系统
            print("声控系统已关闭")
            voice.start(False)
        elif event == "打开声控系统": #按下“打开声控系统”按钮时建立子线程调用start(True)，开启声控系统
            print("欢迎使用本套声控系统")
            threading.Thread(target=voice.start,args=(True,),daemon=True).start()
    windows.close()
if __name__ == '__main__':
    ui()