import pm4py
import pandas as pd
import os
import re
#该文件中的方法可以得到单个轨迹变体的集合，如<a,b,c>2，包括<a,b,c>变体及其非变体集合
# 读取日志文件
log = pm4py.read_xes("F:/402/模型挖掘算法可靠性评价方法/结果/Synthetic log6/Synthetic log 6.xes")

# 转为 DataFrame
df = pm4py.convert_to_dataframe(log)

# 按 case 聚合事件顺序，得到每个 variant
df_sorted = df.sort_values(["case:concept:name", "time:timestamp"]) if "time:timestamp" in df.columns else df
case_variants = (
    df_sorted.groupby("case:concept:name")["concept:name"]
    .apply(tuple)
    .to_dict()
)

# 获取所有唯一 variant
variant_to_cases = {}
for case_id, variant in case_variants.items():
    variant_to_cases.setdefault(variant, []).append(case_id)

print(f"共发现 {len(variant_to_cases)} 种变体")

# 输出目录
output_dir = "F:/402/模型挖掘算法可靠性评价方法/结果/Synthetic log6/variants_from_df"
os.makedirs(output_dir, exist_ok=True)

# 将每个 variant 的轨迹提取为 EventLog 并导出
for idx, (variant, case_ids) in enumerate(variant_to_cases.items(), 1):
    # 过滤出属于该 variant 的所有事件
    variant_df = df[df["case:concept:name"].isin(case_ids)]

    # 转回 EventLog
    sub_log = pm4py.convert_to_event_log(variant_df)

    # 清理文件名
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', "-".join(variant))
    safe_name = safe_name[:100]  # 防止太长
    output_path = os.path.join(output_dir, f"variant_{idx}_{safe_name}.xes")

    # 导出
    pm4py.write_xes(sub_log, output_path)
    print(f"✅ 导出变体 {idx}: {variant} -> {len(case_ids)} 个轨迹")

print("全部变体导出完成。")

