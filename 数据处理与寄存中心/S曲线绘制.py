import skrf as rf
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# 图片预处理部分
plt.style.use("fast")  # 调用配色方案
# 设置字体的最优方案，中文为宋体，英文为Times New Roman
plt.rcParams["font.family"] = (
    "Times New Roman, SimSun"  # 设置字体族，中文为SimSun，英文为Times New Roman
)
plt.rcParams["mathtext.fontset"] = "stix"  # 设置数学公式字体为stix
# 设置字体的大小，
label_size = 18  # xy轴标签的大小
legend_size = 18  # 图例的大小
axis_size = 16  # 坐标轴刻度标签的大小
# 预设配置字典（修改部分）
configs = {
    "xwindow": {
        "chaptername": "chapter3",
        "s2p_file": "6-11GHz窗S曲线.s2p",
        "denserperiod": "6-11ghz",
        "x_minor_step": 1e9,
        "y_minor_step": 5,
        "figsize": (6, 5.5),
    },
    "Xwaveguide": {
        "chaptername": "chapter3",
        "s2p_file": "X波段脊波导验证.s2p",
        "denserperiod": "6-11ghz",
        "x_minor_step": 0.5e9,
        "y_minor_step": 10,
        "figsize": (6, 5.5),
    },
    "Xwindowshelled": {
        "chaptername": "chapter3",
        "s2p_file": "X加上铜壳后的S曲线.s2p",
        "denserperiod": "6-11ghz",
        "x_minor_step": 0.5e9,
        "y_minor_step": 5,
        "figsize": (6, 5.5),
    },
}

# 通过修改这里切换配置 ↓
config_selector = "Xwindowshelled"  # 可选 'window' 或 'waveguide'
selected_config = configs[config_selector]

# 加载TOUCHSTONE数据（修改部分）
sparadata = rf.Network(
    os.path.join(
        script_dir, selected_config["chaptername"], selected_config["s2p_file"]
    )
)

denserperiod = selected_config["denserperiod"]  # 加粗的频域范围

# 绘制 S11 参数
sparadata.s11.plot_s_db(label=r"$\mathrm{S_{11}}$", lw=2)

sparadata.s21.plot_s_db(label=r"$\mathrm{S_{21}}$", lw=2)
sparadata.s11[denserperiod].plot_s_db(
    lw=3, label="目标频段反射", color="red"
)  # 标出感兴趣的频段，表粗的线的宽度为3

# 设置坐标轴标签和标题
plt.xlabel("频率/ GHz", fontsize=label_size)
plt.ylabel("幅值/ dB", fontsize=label_size)

# 启用次要刻度
plt.minorticks_on()

# 自定义次要刻度位置
plt.tick_params(
    axis="both", which="minor", bottom=True, top=False, left=True, right=False
)

# 设置坐标轴刻度标签大小
plt.tick_params(axis="both", which="major", labelsize=axis_size)
plt.tick_params(axis="both", which="minor")

# 设置图例
plt.legend(frameon=False, fontsize=legend_size)

# 获取当前轴，准备设置子刻度
ax = plt.gca()
# 设置X/Y轴次要刻度（修改部分）
ax.xaxis.set_minor_locator(ticker.MultipleLocator(selected_config["x_minor_step"]))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(selected_config["y_minor_step"]))

plt.grid(which="both", linestyle="--", linewidth=0.5)
# 显示图表
plt.show()
