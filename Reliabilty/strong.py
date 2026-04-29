import pandas as pd
import numpy as np

# ==========================
# 参数设置
# ==========================
alpha = beta = gamma = delta = 0.25
lambda1, lambda2, lambda3 = 0.5, 0.3, 0.2

# ==========================
# 读取Excel
# ==========================
file_path = "data.xlsx"   # 修改为你的文件路径
df = pd.read_excel(file_path, header=None)

# ==========================
# 工具函数
# ==========================
def is_valid(x):
    """判断是否为有效数值"""
    try:
        return not pd.isna(float(x))
    except:
        return False

def compute_metrics(row_values):
    """计算单日志指标"""
    q = []
    valid_idx = []

    # 提取有效数据
    for i, val in enumerate(row_values):
        if is_valid(val):
            q.append(float(val))
            valid_idx.append(i)

    n = 10
    k = len(q)

    # --------------------------
    # SR
    # --------------------------
    SR = k / n

    # --------------------------
    # MQ
    # --------------------------
    MQ = np.mean(q) if k > 0 else 0

    # --------------------------
    # Stability
    # --------------------------
    if k > 1:
        diffs = [abs(q[i] - q[i-1]) for i in range(1, k)]
        Stab = 1 - np.mean(diffs)
    else:
        Stab = 0

    # --------------------------
    # Convergence
    # --------------------------
    if k > 1:
        q_final = q[-1]
        conv_vals = [abs(v - q_final) for v in q]
        Conv = 1 - np.mean(conv_vals)
    else:
        Conv = 0

    # --------------------------
    # IRI
    # --------------------------
    IRI = alpha*SR + beta*Stab + gamma*Conv + delta*MQ

    return SR, MQ, Stab, Conv, IRI


# ==========================
# 主计算
# ==========================
results = []
alg_IRI_dict = {"AM": [], "HM": [], "IM": [], "IMi": []}

alg_names = ["AM", "HM", "IM", "IMi"]

for i in range(len(df)):
    row = df.iloc[i, :10]  # 前10列是数据

    SR, MQ, Stab, Conv, IRI = compute_metrics(row)

    results.append([SR, MQ, Stab, Conv, IRI])

    # 按算法存储
    alg = alg_names[i % 4]
    alg_IRI_dict[alg].append(IRI)

# ==========================
# 跨日志指标
# ==========================
cross_metrics = {}

for alg in alg_names:
    iri_list = np.array(alg_IRI_dict[alg])

    mean_iri = np.mean(iri_list)
    var_iri = np.mean((iri_list - mean_iri)**2)
    iri_min = np.min(iri_list)

    CR = lambda1*mean_iri - lambda2*var_iri + lambda3*iri_min

    cross_metrics[alg] = (mean_iri, var_iri, iri_min, CR)

# ==========================
# 写回Excel
# ==========================
start_col = 11  # 第12列（从0开始）

required_cols = start_col + 9
if df.shape[1] < required_cols:
    for _ in range(required_cols - df.shape[1]):
        df[df.shape[1]] = np.nan

for i in range(len(df)):
    alg = alg_names[i % 4]

    SR, MQ, Stab, Conv, IRI = results[i]
    mean_iri, var_iri, iri_min, CR = cross_metrics[alg]

    df.iloc[i, start_col:start_col+9] = [
        SR, MQ, Stab, Conv,
        IRI,        # 单日志IRI
        mean_iri,   # 跨日志IRI
        var_iri,
        iri_min,
        CR
    ]

# ==========================
# 保存结果
# ==========================
output_path = "output.xlsx"
df.to_excel(output_path, index=False, header=False)

print("计算完成，结果已保存到:", output_path)