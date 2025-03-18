import matplotlib.pyplot as plt
import numpy as np

# 新增字体配置解决中文显示问题
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 使用黑体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题


def vaughan_sey(epsilon):
    """
    Vaughan secondary electron emission yield (SEY) model.

    Parameters:
    epsilon : float or array-like
        The normalized energy parameter.

    Returns:
    sey : float or array-like
        The secondary electron emission yield.
    """
    if isinstance(epsilon, (int, float)):
        if epsilon <= 3:
            return (epsilon * np.exp(1 - epsilon)) ** 0.56
        elif 3 < epsilon <= 3.6:
            return (epsilon * np.exp(1 - epsilon)) ** 0.25
        else:
            return 1.125 / epsilon**0.35
    else:
        sey = np.zeros_like(epsilon)
        sey[epsilon <= 1] = (
            epsilon[epsilon <= 1] * np.exp(1 - epsilon[epsilon <= 1])
        ) ** 0.56
        sey[(1 < epsilon) & (epsilon <= 3.6)] = (
            epsilon[(1 < epsilon) & (epsilon <= 3.6)]
            * np.exp(1 - epsilon[(1 < epsilon) & (epsilon <= 3.6)])
        ) ** 0.25
        sey[epsilon > 3.6] = 1.125 / epsilon[epsilon > 3.6] ** 0.35
        return sey


# Generate data points
epsilon_values = np.linspace(1, 5, 400)
sey_values = vaughan_sey(epsilon_values)

# Plot the SEY curve
plt.figure(figsize=(6, 6))
plt.plot(epsilon_values, sey_values, label="SEY vs Primary electron energy")

# Add reference lines
plt.axhline(y=1.0, color="gray", linestyle="--")
plt.axvline(x=np.argmax(sey_values), color="gray", linestyle="--")

# Set labels and title
plt.xlabel("Primary electron energy")
plt.ylabel("SEY")
plt.title("图 2.3 金属材料典型的二次电子发射特性曲线")

# Add annotations
max_index = np.argmax(sey_values)
plt.annotate(
    "E_max",
    xy=(epsilon_values[max_index], sey_values[max_index]),
    xytext=(epsilon_values[max_index] + 0.5, sey_values[max_index]),
    arrowprops=dict(facecolor="black", shrink=0.05),
)

# Show legend
plt.legend()

# Show plot
plt.show()
