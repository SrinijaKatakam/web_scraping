import pandas as pd
dfs = []
# reading csv files
data1 = pd.read_csv('final_1.csv')
dfs.append(data1)
data2 = pd.read_csv('crunchbasetask10.csv')
dfs.append(data2)
big_frame = pd.concat(dfs, ignore_index=True)
big_frame.to_csv('final_1.csv')