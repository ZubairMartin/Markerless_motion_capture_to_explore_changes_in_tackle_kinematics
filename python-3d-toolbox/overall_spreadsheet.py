"""
cd Desktop/python-3d-toolbox
conda activate dlc
python overall_spreadsheet.py

Note: 
    - Do spreadsheet in .xlsx then .ods the .csv
    - write mass in a fraction form
    - all video names should be in the format Tackle6_session12_set2
"""

#############################################################################  
dir_of_spreadsheet = '/home/uct/Desktop/python-3d-toolbox/recent18.csv'
#############################################################################  

import combine134
import deeplabcut as dlc
import sys
import pandas as pd
import numpy as np
import csv
import time

# reads data frame
df = pd.read_csv(dir_of_spreadsheet) 

length=len(df['tackle_name'])

for i in range(length):
    print('Running {0} spreadsheet'.format(df.iloc[i][0]))
    a = df.iloc[i][0] # tackle_name
    b = df.iloc[i][1] # dir_data_files
    c = df.iloc[i][2] # dir_destination
    d = df.iloc[i][3] # calib_project_dir
    e = eval(df.iloc[i][4]) # mass_of_player
    f = (df.iloc[i][5]) # start_tackle_frame
    g = (df.iloc[i][6]) # end_tackle_frame
    h = (df.iloc[i][7]) # GP_used
    j = (df.iloc[i][8]) # the tackler
    #combine134.main(temp='\''+a+'\'',mass=e,T_start=f,T_end=g,folder='\''+b+'\'',directory='\''+c+'\'',project_dir='\''+d+'\'',GP_used=h)
    combine134.main(temp=a[4:],mass=e,T_start=f,T_end=g,folder=b,directory=c,project_dir=d,GP_used=h,player_number=j)
    time.sleep(5) # 5 second delay
    print()

    