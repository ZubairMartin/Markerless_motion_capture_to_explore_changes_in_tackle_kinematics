import os
import numpy as np
import pandas as pd
from pathlib import Path
import re
import time

def replace_dataset_backslash_with_forward(df):
    idx = list(df.index)
    for i in range(len(idx)):
        idx[i] = idx[i].replace("\\", "/")
    df.index = pd.Index(idx)

def get_collected_data_df(dir):
    h5_paths = [os.path.join(dir,f) for f in os.listdir(dir) if f.endswith(".h5") and f.startswith("CollectedData")]
    return pd.read_hdf(h5_paths[0])

def save(df, dir):
    df = df.sort_index()
    df.to_hdf(os.path.join(dir,'CollectedData_UCT.h5'), key='df_with_missing', mode='w')
    df.to_csv(os.path.join(dir,'CollectedData_UCT.csv'))
    print("Saved " + dir)


topdir = '/home/zubair/Session8_Set2_tackle1-UCT-2019-11-27/labeled-data/'
#topdir = '/labeled-data/'

folders = ['GP1_P33_baseline_2_tackle_5', 'GP4_Tackle2_session13_set1', 'GP1_tackle4_session4_set4', 'GP4_Tackle3_session8_set3', 'GP4_Tackle3_session2_set11', 'GP3_tackle4_session7_set1', 'GP4_P37_baseline_1_tackle_6', 'GP1_tackle2_session4_set3', 'GP4_Tackle6_session2_set3', 'GP1_Tackle6_session12_set1', 'GP4_Tackle1_set1_session9', 'GP1_P30_baseline_2_tackle_1', 'GP1_Tackle1_session12_set2', 'GP1_Tackle1_set1_session9', 'GP4_Tackle4_session3_set3', 'GP3_Tackle1_set1_session9', 'GP3_P34_baseline_1_tackle_2', 'GP3_Tackle3_session2_set11', 'GP4_Tackle6_session12_set1', 'GP4_P33_baseline_2_tackle_3', 'GP4_tackle2_session4_set3', 'GP1_tackle3_session3_set3', 'GP3_Tackle5_session13_set2', 'GP3_Tackle1_session2_set5', 'GP4_P34_baseline_1_tackle_1', 'GP3_Tackle3_session8_set3', 'GP1_P28_baseline_2_tackle_2', 'GP1_Tackle2_session12_set2', 'GP4_Tackle1_session5_set1', 'GP1_Tackle1_session3_set3', 'GP3_Tackle2_set2_session9', 'GP3_Tackle6_session2_set3', 'GP3_Tackle5_session3_set3', 'GP3_P35_baseline_2_tackle_5', 'GP3_P32_baseline_1_tackle_3', 'GP3_P33_baseline_2_tackle_2', 'GP4_P29_baseline_1_tackle_4', 'GP1_P37_baseline_2_tackle_1', 'GP4_P35_baseline_2_tackle_6', 'GP4_Tackle5_session13_set2', 'GP1_Tackle4_session3_set3', 'GP1_P35_baseline_1_tackle_1', 'GP3_P31_baseline_1_tackle_3', 'GP1_Tackle5_session3_set3', 'GP1_Tackle1', 'GP3_Tackle6_session5_set1', 'GP3_Tackle6_session12_set1', 'GP4_Tackle2_set2_session9', 'GP1_Tackle6_session12_set2', 'GP4_P28_baseline_2_tackle_2', 'GP1_P31_baseline_2_tackle_1', 'GP4_P31_baseline_1_tackle_5', 'GP4_Tackle1_session3_set3', 'GP4_P30_baseline_1_tackle_3', 'GP4_Tackle1_session2_set1', 'GP1_Tackle3_session7_set1', 'GP1_P34_baseline_1_tackle_1', 'GP4_tackle4_session4_set4', 'GP1_Tackle2_session13_set1', 'GP4_Tackle1', 'GP1_P29_baseline_2_tackle_5', 'GP4_Tackle1_session2_set5', 'GP4_Tackle1_session12_set2', 'GP4_Tackle3_session7_set1', 'GP3_Tackle1_session5_set1', 'GP3_P37_baseline_2_tackle_6', 'GP4_P32_baseline_2_tackle_6', 'GP3_P29_baseline_2_tackle_6', 'GP4_P36_baseline_2_tackle_6', 'GP4_Tackle6_session5_set1', 'GP4_Tackle5_session3_set3', 'GP4_Tackle2_session12_set2', 'GP3_Tackle3_session7_set1', 'GP3_Tackle1_session12_set2', 'GP3_Tackle1_session2_set1', 'GP1_Tackle6_session5_set1', 'GP3_Tackle2_session13_set1', 'GP1_P36_baseline_1_tackle_1', 'GP1_Tackle4_set4_session8', 'GP3_P36_baseline_2_tackle_4', 'GP3_Tackle4_set4_session8', 'GP1_Tackle1_session5_set1', 'GP3_P28_baseline_1_tackle_6', 'GP1_Tackle5_session13_set2', 'GP3_tackle3_session3_set3', 'GP1_Tackle3_session8_set3', 'GP3_Tackle1', 'GP4_tackle3_session3_set3', 'GP4_Tackle6_session12_set2', 'GP4_Tackle4_set4_session8', 'GP1_tackle4_session7_set1', 'GP4_tackle4_session7_set1', 'GP1_Tackle2_set2_session9', 'GP3_P30_baseline_1_tackle_3']

for folder in folders:
	dir =  topdir+folder+"/"
	print("Solving {0} ...".format(dir))
	df = get_collected_data_df(dir)
	replace_dataset_backslash_with_forward(df)
	save(df, dir)
	time.sleep(0.5)
