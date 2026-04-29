# import pm4py
# import os
# import re
# import pandas as pd
#挖掘增量模型
# # ----------------------------
# # 输入日志文件夹
# # ----------------------------
# log_dir = "F:/YanJiaXin/模型挖掘算法可靠性评价方法/cumulative_logs"
#
# # ----------------------------
# # 输出：评估结果表、模型文件夹
# # ----------------------------
# output_excel = "F:/YanJiaXin/模型挖掘算法可靠性评价方法/evaluation_results.xlsx"
# model_dir = "F:/YanJiaXin/模型挖掘算法可靠性评价方法/models"
# os.makedirs(model_dir, exist_ok=True)
#
# # ----------------------------
# # 获取所有 Lk.xes，并按编号排序
# # ----------------------------
# files = [f for f in os.listdir(log_dir) if f.lower().endswith(".xes")]
#
# def extract_index(name):
#     m = re.match(r"L(\d+)\.xes", name)
#     return int(m.group(1)) if m else 999999
#
# files = sorted(files, key=extract_index)
#
# print("发现增量日志：")
# for f in files:
#     print("  -", f)
#
# # ----------------------------
# # 存储指标结果
# # ----------------------------
# metrics = ["fitness", "precision", "f_measure"]
# results = {m: [] for m in metrics}
# results["log_id"] = []
#
# # ----------------------------
# # 主循环：挖掘模型、评估、保存
# # ----------------------------
# for filename in files:
#     log_id = filename.replace(".xes", "")
#     file_path = os.path.join(log_dir, filename)
#
#     print(f"\n===== 处理 {filename} =====")
#     log = pm4py.read_xes(file_path)
#
#     # ---- 挖掘模型：Inductive Miner ----
#     net, im, fm = pm4py.discover_petri_net_inductive(log)
#
#     # ---- 保存模型 PNG ----
#     # png_path = os.path.join(model_dir, f"{log_id}.png")
#     # pm4py.save_vis_petri_net(net, im, fm, png_path)
#
#     # ---- 保存模型 PNML ----
#     pnml_path = os.path.join(model_dir, f"{log_id}.pnml")
#     pm4py.write_pnml(net, im, fm, pnml_path)
#
#     # print(f"模型已保存：{png_path}")
#     print(f"模型已保存：{pnml_path}")
#
#     # ---- 计算 fitness ----
#     fitness = pm4py.fitness_alignments(log, net, im, fm)["log_fitness"]
#
#     # ---- 计算 precision ----
#     precision = pm4py.precision_alignments(log, net, im, fm)
#
#     # ---- F-measure ----
#     if fitness + precision == 0:
#         f_measure = 0
#     else:
#         f_measure = 2 * fitness * precision / (fitness + precision)
#
#     # ---- 保存到结果中 ----
#     results["log_id"].append(log_id)
#     results["fitness"].append(fitness)
#     results["precision"].append(precision)
#     results["f_measure"].append(f_measure)
#
#     print(f"fitness  = {fitness:.4f}")
#     print(f"precision = {precision:.4f}")
#     print(f"F-measure = {f_measure:.4f}")
#
# # ----------------------------
# # 写入 Excel：第一列为指标，第一行是 L1/L2/L3...
# # ----------------------------
# df = pd.DataFrame(results)
# df = df.set_index("log_id").T
# df.to_excel(output_excel, index=True)
#
# print("\n========= 全部完成 =========")
# print("评估结果写入：", output_excel)
# print("模型保存在：", model_dir)
import pm4py
import os
import re
import pandas as pd

# ======================================================
# 固定对比日志（唯一的基准日志）
# ======================================================
# target_log_path = r"F:/402/模型挖掘算法可靠性评价方法/结果/Synthetic log4/Synthetic log 4.xes"
# target_log = pm4py.read_xes(target_log_path)
# print("基准日志加载完成：", target_log_path)

# ======================================================
# 输入增量日志文件夹
# ======================================================
log_dir = r"F:/402/模型挖掘算法可靠性评价方法/结果/Synthetic log6/cumulative_logs"

# ======================================================
# 输出路径
# ======================================================
output_excel = r"F:/402/模型挖掘算法可靠性评价方法/结果/Synthetic log5/10%/evaluation_results_single_reference_IM.xlsx"
model_dir = r"F:/402/模型挖掘算法可靠性评价方法/结果/Synthetic log6/models_single_reference_IMi"
os.makedirs(model_dir, exist_ok=True)

# ======================================================
# 获取所有 Lk.xes，并按编号排序
# ======================================================
files = [f for f in os.listdir(log_dir) if f.lower().endswith(".xes")]

def extract_index(name):
    m = re.match(r"L(\d+)\.xes", name)
    return int(m.group(1)) if m else 999999

files = sorted(files, key=extract_index)

print("发现增量日志：", len(files))
for f in files:
    print("  -", f)

num_logs = len(files)

# ======================================================
# 按你给的规则选取日志进行评估
# ======================================================
selected_logs = []

if num_logs < 10:
    # 规则 1：数量 < 10 → 全部读取
    selected_logs = files
else:
    # 规则 2：数量 >= 10 → 均分 10 份
    step = num_logs // 10

    # 前 9 份取每份最后一个日志
    for i in range(9):
        idx = (i + 1) * step - 1
        selected_logs.append(files[idx])

    # 第 10 份 → 文件夹编号最大日志
    selected_logs.append(files[-1])

print("\n最终参与挖掘的日志：")
for f in selected_logs:
    print("  →", f)

# ======================================================
# 评估结果
# ======================================================
metrics = ["fitness", "precision", "f_measure"]
results = {m: [] for m in metrics}
results["log_id"] = []

# ======================================================
# 主循环：挖掘模型、评估、保存
# ======================================================
for filename in selected_logs:
    log_id = filename.replace(".xes", "")
    file_path = os.path.join(log_dir, filename)

    print(f"\n===== 处理 {filename} =====")
    log = pm4py.read_xes(file_path)
    # df = pm4py.convert_to_dataframe(pm4py.read_xes(file_path))
    #
    # # print(df.dtypes)
    # # print(df.head())
    #
    # # 3. 强制转换时间戳为 datetime
    # df['time:timestamp'] = pd.to_datetime(df['time:timestamp'], errors='coerce')
    # if df['time:timestamp'].isna().any():
    #     print("WARNING: Some timestamps failed to convert. Rows:")
    #     print(df[df['time:timestamp'].isna()].head())
    # log = pm4py.convert_to_event_log(df)
    # 挖掘模型
    net, im, fm = pm4py.discover_petri_net_inductive(log,noise_threshold=0.2)

    # 保存模型
    pnml_path = os.path.join(model_dir, f"{log_id}.pnml")
    pm4py.write_pnml(net, im, fm, pnml_path)
    print(f"模型已保存：{pnml_path}")
    # sound=pm4py.check_soundness(net, im, fm)
    # if sound ==True:
    # 使用固定 target_log 评估模型

#     try:
#         fitness = pm4py.fitness_alignments(target_log, net, im, fm)["log_fitness"]
#         precision = pm4py.precision_alignments(target_log, net, im, fm)
#         f_measure = 2 * fitness * precision / (fitness + precision)
#     except Exception as e:
#         print(f"错误: {e}. 将 fitness 和 precision 设为 '-'")
#         fitness = "-"
#         precision = "-"
#         f_measure = "-"
#     # else:
#     #     fitness='-'
#     #     precision = '-'
#     #     f_measure ='-'
#         # f_measure = 0 if fitness == precision == '-' else 2 * fitness * precision / (fitness + precision)
#     results["log_id"].append(log_id)
#     results["fitness"].append(fitness)
#     results["precision"].append(precision)
#     results["f_measure"].append(f_measure)
#
#     # print(f"[基准日志] fitness  = {fitness:.4f}")
#     # print(f"[基准日志] precision = {precision:.4f}")
#     # print(f"[基准日志] F-measure = {f_measure:.4f}")
#
# # ======================================================
# # 写出 Excel
# # ======================================================
# df = pd.DataFrame(results)
# df = df.set_index("log_id").T
# df.to_excel(output_excel, index=True)

print("\n========= 全部完成 =========")
print("评估结果写入：", output_excel)
print("模型保存在：", model_dir)

