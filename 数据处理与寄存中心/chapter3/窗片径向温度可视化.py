import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


filepath = os.path.dirname(
    os.path.abspath(__file__)
)  # 获取当前py文件所在文件夹路径，字体已经安装好啦
filename = "窗片径向温度分布.txt"
filepath = os.path.join(filepath, filename)

S11 = np.loadtxt(filepath, delimiter="\t", skiprows=1, unpack=True)

plt.rcParams["font.size"] = 18
mpl.rc(
    "font", family="Consolas"
)  # 设置绘图全局字体这种办法比直接使用fontproperties方便一些，因为它全局设置不需要再更改
plt.figure(figsize=(10, 6))

plt.plot(S11[0], S11[1], label="$S_{11}$")
plt.xlabel("Frequency/GHz")
plt.ylabel("S Parameters/dB")
plt.legend()
plt.grid()
plt.show()
pass
