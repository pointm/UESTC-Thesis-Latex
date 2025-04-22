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

# 预设配置字典
configs = {
    "XDRW2RW": {
        "chaptername": "chapter3",
        "s2p_file": "X脊波导与矩形波导过渡.s2p",
        "denserperiod": "6-11ghz",
        "x_minor_step": 1e9,
        "y_minor_step": 5,
        "figsize": (8, 5.5),
    },
}

# 通过修改这里切换配置 ↓
config_selector = "XDRW2RW"  # 可选 'window' 或 'waveguide'
selected_config = configs[config_selector]

# 加载TOUCHSTONE数据
sparadata = rf.Network(
    os.path.join(
        script_dir, selected_config["chaptername"], selected_config["s2p_file"]
    )
)
denserperiod = selected_config["denserperiod"]  # 加粗的频域范围

# 创建画布和主Y轴
fig, axis_y1 = plt.subplots(figsize=selected_config["figsize"])

# 绘制S12曲线（左轴）
# sparadata.plot_s_db(m=1, n=0, lw=2, color="b", label=None)
sparadata.plot_s_db(m=0, n=1, lw=2, color="b", label=None)
axis_y1.spines["left"].set_color("b")
axis_y1.spines["left"].set_linewidth(3)
# axis_y1.set_ylabel(r"$\mathrm{S_{21}}$/dB", color="b", fontsize=label_size)
axis_y1.set_ylabel(r"$\mathrm{S_{12}}$/dB", color="b", fontsize=label_size)
axis_y1.tick_params(
    axis="y",
    color="b",
    labelcolor="b",
    width=2,
    length=6,
    labelsize=axis_size,  # 新增：设置左轴刻度标签大小
)

# 设置X轴标签和刻度
axis_y1.set_xlabel("频率/GHz", fontsize=label_size)  # 添加字体大小
axis_y1.tick_params(axis="x", labelsize=axis_size)  # 新增X轴刻度字体设置

# 创建次Y轴绘制S22曲线
axis_y2 = axis_y1.twinx()

# sparadata.plot_s_db(m=0, n=0, lw=2, color="r", label=None)
sparadata.plot_s_db(m=1, n=1, lw=2, color="r", label=None)

axis_y2.spines["right"].set_color("r")
axis_y2.spines["right"].set_linewidth(3)
# axis_y2.set_ylabel(r"$\mathrm{S_{11}}$ /dB", color="r", fontsize=label_size)
axis_y2.set_ylabel(r"$\mathrm{S_{22}}$ /dB", color="r", fontsize=label_size)
axis_y2.tick_params(
    axis="y",
    color="r",
    labelcolor="r",
    width=2,
    length=6,
    labelsize=axis_size,  # 新增：设置右轴刻度标签大小
)

# 设置坐标轴标签和标题
plt.xlabel("频率/ GHz", fontsize=label_size)


# 设置图例
lines = axis_y1.get_lines() + axis_y2.get_lines()
# labels = [
#     r"$\mathrm{S_{21}}$",  # 手动指定S21标签
#     r"$\mathrm{S_{11}}$",  # 手动指定S11标签
# ]
labels = [
    r"$\mathrm{S_{12}}$",  # 手动指定S12标签
    r"$\mathrm{S_{22}}$",  # 手动指定S22标签
]
plt.legend(
    lines,
    labels,  # 使用自定义标签列表
    frameon=False,
    fontsize=legend_size,
    bbox_to_anchor=(0.4, 0.5),
)

# 显示图表
plt.show()
