# 广东财经大学人机交互期末作业

该项目是利用佛山微风科技的MODBUS-485继电器模块与百度语音识别实现的一套基于声控的电灯控制系统，该套系统基于python开发设计，其中用到的界面设计也是用python开发的。

该项目为用户语音输入，程序判断语音输入的指令中是否含有开灯关灯字样来控制485模块中继电器的开合从而控制电灯的开关，同时还实现了以秒为单位的延迟开关指令。

## 注意事项

需要安装serial和modbus_tk

pip install serial

pip install modbus_tk

还需下载继电器对应的驱动

下载连接--http://www.wch.cn/products/CH340.html

