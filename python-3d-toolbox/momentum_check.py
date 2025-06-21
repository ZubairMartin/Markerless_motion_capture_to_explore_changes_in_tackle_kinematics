'''
Check if momentum equation works when finding the final velocity
'''

import xlsxwriter
import string
import itertools
import deeplabcut as dlc
import pandas as pd
import numpy as np
import csv
import math

Start_frame = # Actual frame in which tackle starts 
End_frame = # Actual frame in which tackle ends
location = '/home/uct/Desktop/'
labels = ['ankle1','knee1','hip1','wrist1','shoulder1','elbow1','ankle2','knee2','hip2','wrist2','shoulder2','elbow2','chin','forehead','top','bottom','middle','upper quartile','lower quartile']


def truncate(df_to_use,item,start_frame,end_frame):
    var = []
    len_of_df = len(df['{0}'.format(item)])
    
    for t in range(len_of_df):
        var.append(df.iloc[t]['{0}'.format(item)])

    start_index = var.index(start_frame)
    end_index = var.index(end_frame)

    #return start_index,end_index,var[start_index:end_index+1]
    return var[start_index:end_index+1]

df = []
for k in range (len(labels)):
    df.append(pd.read_csv(folder+'{0}_splined.csv'.format(labels[k])))


velocity_shoulder1 = truncate(df[4],'x_vel',Start_frame,End_frame)
velocity_hip1 = truncate(df[2],'x_vel',Start_frame,End_frame)
velocity_middle = truncate(df[16],'x_vel',Start_frame,End_frame)
velocity_lower = truncate(df[18],'x_vel',Start_frame,End_frame)