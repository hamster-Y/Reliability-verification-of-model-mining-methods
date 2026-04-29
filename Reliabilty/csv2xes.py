import pm4py
import pandas as pd
dataframe = pd.read_csv("F:/402/模型挖掘算法可靠性评价方法/结果/Synthetic log6/15%/Synthetic log 6_with_15anomalies.csv", sep=',')
# dataframe = pandas.read()
dataframe = pm4py.format_dataframe(dataframe, case_id='Case', activity_key='Activity', timestamp_key='Timestamp')
log = pm4py.convert_to_event_log(dataframe)
pm4py.write_xes(log, "F:/402/模型挖掘算法可靠性评价方法/结果/Synthetic log6/15%/Synthetic log 6_with_15anomalies.xes", case_id_key='case:concept:name')
# log2=pm4py.read_xes("F:/402/模型挖掘算法可靠性评价方法/结果/Synthetic log1/Synthetic log 1.xes")
# log=pm4py.read_xes("F:/402/模型挖掘算法可靠性评价方法/结果/Synthetic log1/5%/Synthetic log 105_with_anomalies.xes")
# a,b,c=pm4py.discover_petri_net_inductive(log)
# aligned_traces = pm4py.fitness_alignments(log, a,b,c)
# print(aligned_traces)
# pm4py.view_petri_net(a,b,c)