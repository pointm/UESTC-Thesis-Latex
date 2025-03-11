import math


def calculate_lambda_c(a, b, s, d):
    """
    计算双脊波导截止波长λ_c
    参数单位：毫米(mm)
    返回单位：毫米(mm)
    """
    # 计算主要项
    term1 = 1 + (4 / math.pi) * (1 + 0.2 * math.sqrt(b / (a - s))) * (
        b / (a - s)
    ) * math.log(1 / math.sin(math.pi * d / (2 * b)))

    term2 = (2.45 + 0.2 * (s / a)) * (s * b / (d * (a - s)))

    # 计算整个分母项
    denominator = term1 + term2

    # 计算a/lambda_c比值
    a_over_lambda_c = a / (2 * (a - s)) * math.sqrt(1 / denominator)

    # 计算实际lambda_c
    lambda_c = a / a_over_lambda_c

    return lambda_c


# 新增频率换算函数
def calculate_frequency(lambda_c_mm):
    """将毫米为单位的波长转换为GHz为单位的频率"""
    c = 3e8  # 光速，单位：米/秒
    lambda_c_m = lambda_c_mm / 1000  # 毫米转米
    return c / lambda_c_m / 1e9  # 转换为GHz


# 示例参数（单位：mm）
a = 20
b = 10
s = 4
d = 5

# 新增参数校验
print("\n参数校验结果:")
d_b_ratio = d / b
b_a_ratio = b / a
s_a_ratio = s / a

print(
    f"(1) d/b = {d_b_ratio:.3f} ({'满足' if 0.01 <= d_b_ratio <= 1 else '不满足'}) 0.01 ≤ {d_b_ratio:.3f} ≤ 1"
)
print(
    f"(2) b/a = {b_a_ratio:.3f} ({'满足' if 0 <= b_a_ratio <= 1 else '不满足'}) 0 ≤ {b_a_ratio:.3f} ≤ 1"
)
print(
    f"(3) s/a = {s_a_ratio:.3f} ({'满足' if 0 <= s_a_ratio <= 0.45 else '不满足'}) 0 ≤ {s_a_ratio:.3f} ≤ 0.45"
)

# 在输出部分添加频率计算
result = calculate_lambda_c(a, b, s, d)
print(f"\n计算得到的截止波长λ_c为: {result:.2f} mm")
print(f"对应的截止频率f_c为: {calculate_frequency(result):.2f} GHz")  # 新增输出行
