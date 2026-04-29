import pm4py
import pandas as pd
log=pm4py.read_xes("F:/402/模型挖掘算法可靠性评价方法/结果/Synthetic log6/Synthetic log 6.xes")
# 读取 XES
# log = pm4py.read_xes("input.xes")

# 转成 DataFrame
df = pm4py.convert_to_dataframe(log)

# 保存为 CSV
# df = df.drop(columns=["event_startTime"])
df = df.drop(columns=["startTime"])
df=df.drop(columns=["org:resource"])
# 转时间
df["time:timestamp"] = pd.to_datetime(df["time:timestamp"])
df["resource"] = "NONE"
# 转回字符串（保留毫秒）
# 去时区 + 保留到秒
df["time:timestamp"] = (
    df["time:timestamp"]
    .dt.tz_localize(None)
    .dt.strftime("%Y-%m-%d %H:%M:%S")
)

# 保存
df.to_csv("F:/402/模型挖掘算法可靠性评价方法/结果/Synthetic log6/Synthetic log 6.csv", index=False, encoding="utf-8-sig")

print("处理完成")
