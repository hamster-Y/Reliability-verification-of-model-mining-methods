import pm4py
import os
import re
from pm4py.objects.log.obj import EventLog
from pm4py.objects.log.importer.xes import importer as xes_importer
import pandas as pd
#该文件中的方法可以得到增量子日志L1,L2,...,Ln
variant_dir = "F:/402/模型挖掘算法可靠性评价方法/结果/Synthetic log6/variants_from_df"
output_dir = "F:/402/模型挖掘算法可靠性评价方法/结果/Synthetic log6/cumulative_logs"
os.makedirs(output_dir, exist_ok=True)
def safe_eventlog_to_df(log):
    rows = []
    for trace in log:
        case_id = trace.attributes.get("concept:name", None)
        for event in trace:
            row = {"case_id": case_id}
            for k, v in event.items():
                row[k] = v
            rows.append(row)
    return pd.DataFrame(rows)
files = os.listdir(variant_dir)
xes_files = [f for f in files if f.lower().endswith(".xes")]

def extract_index(filename):
    m = re.match(r"variant_(\d+)_", filename)
    return int(m.group(1)) if m else 999999

xes_files = sorted(xes_files, key=extract_index)

cumulative_log = EventLog()

for idx, filename in enumerate(xes_files, start=1):
    file_path = os.path.join(variant_dir, filename)

    # ---- 安全读取 ----
    # var_log = pm4py.read_xes(file_path)
    var_log = xes_importer.apply(file_path)
    # 强制转换，避免结构错误
    # df = pm4py.convert_to_dataframe(var_log)
    df = safe_eventlog_to_df(var_log)
    if "time:timestamp" in df.columns:
        df["time:timestamp"] = pd.to_datetime(df["time:timestamp"], errors="coerce")
    df = df.rename(columns={"case_id": "case:concept:name"})
    var_log = pm4py.convert_to_event_log(df)

    print(f"{filename}: {len(var_log)} traces")

    # 防止混入字符串
    for trace in var_log:
        if not hasattr(trace, "attributes"):
            raise ValueError(f"错误：在 {filename} 里发现非 trace 对象：{trace}")
        cumulative_log.append(trace)

    # 输出 Lx
    out = os.path.join(output_dir, f"L{idx}.xes")
    pm4py.write_xes(cumulative_log, out)
    print(f"✔ 导出 L{idx}: 总轨迹数 = {len(cumulative_log)}")

print("完成")
