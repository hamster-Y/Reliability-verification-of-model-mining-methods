import pandas as pd
import numpy as np

# ==========================
# 参数
# ==========================
alpha = beta = gamma = delta = 0.25
lambda1, lambda2, lambda3 = 0.5, 0.3, 0.2

# ==========================
# 读取数据（无表头）
# ==========================
df = pd.read_excel("noise_data.xlsx", header=None)

# ==========================
# 判断有效值
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
log_NRI_list = []

for i in range(0, len(df), 3):

    row5 = df.iloc[i]
    row10 = df.iloc[i+1]
    row15 = df.iloc[i+2]

    SR5, MQ5, Stab5, Conv5, IRI5 = compute_metrics(row5)
    SR10, MQ10, Stab10, Conv10, IRI10 = compute_metrics(row10)
    SR15, MQ15, Stab15, Conv15, IRI15 = compute_metrics(row15)

    # ======================
    # Robust
    # ======================
    Robust = (IRI5 + IRI10 + IRI15) / 3

    # ======================
    # Amp（你的规则）
    # ======================
    if IRI5 == 0:
        Amp = 1
    else:
        Amp = (IRI5 - IRI15) / IRI5

    # ======================
    # 噪声稳定性
    # ======================
    Var = ((IRI5 - Robust)**2 + (IRI10 - Robust)**2 + (IRI15 - Robust)**2) / 3
    Stab_noise = 1 - Var

    # ======================
    # NRI
    # ======================
    NRI = 0.4*Robust + 0.4*(1 - Amp) + 0.2*Stab_noise

    log_NRI_list.append(NRI)

    # 写入三行（共享同一个NRI）
    results.extend([
        [SR5, MQ5, Stab5, Conv5, IRI5, Robust, Amp, Var, Stab_noise, NRI],
        [SR10, MQ10, Stab10, Conv10, IRI10, Robust, Amp, Var, Stab_noise, NRI],
        [SR15, MQ15, Stab15, Conv15, IRI15, Robust, Amp, Var, Stab_noise, NRI]
    ])

# ==========================
# 跨日志指标
# ==========================
nri_array = np.array(log_NRI_list)

mean_nri = np.mean(nri_array)
var_nri = np.mean((nri_array - mean_nri)**2)
nri_min = np.min(nri_array)

CR = lambda1*mean_nri - lambda2*var_nri + lambda3*nri_min

# ==========================
# 写回Excel
# ==========================
# ==========================
# 写回Excel（修正版）
# ==========================
start_col = 11

# ⭐ 先扩展列
required_cols = start_col + 14
if df.shape[1] < required_cols:
    for _ in range(required_cols - df.shape[1]):
        df[df.shape[1]] = np.nan

# 写入单日志指标
for i in range(len(df)):
    SR, MQ, Stab, Conv, IRI, Robust, Amp, Var, Stab_noise, NRI = results[i]

    df.iloc[i, start_col:start_col+10] = [
        SR, MQ, Stab, Conv,
        IRI,
        Robust, Amp, Var, Stab_noise,
        NRI
    ]

# 写跨日志指标
for i in range(len(df)):
    df.iloc[i, start_col+10:start_col+14] = [
        mean_nri, var_nri, nri_min, CR
    ]
# ==========================
# 保存
# ==========================
df.to_excel("noise_results.xlsx", index=False, header=False)

print("✅ 计算完成！")