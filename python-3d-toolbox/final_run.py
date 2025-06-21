import combine134 as cb
import csv
"""
directory = '/home/uct/Analyse_videos/test/' # Directory of folder to place files
folder = '/home/uct/Analyse_videos/test/'# Directory of folder with all the data
project_dir = '/home/uct/Analyse_videos/CameraCalibration/Projects/final_calibration_videos/P34_baseline_2' # of camera calibration
mass = 100.55 # mass of tackler
temp = 'P34_baseline_2_tackle_1'
spreadsheetname = 'spreadsheet_'+temp
T_start = 74
T_end = 160
GP_used = 134
player_number= 34

cb.main(temp,mass,T_start,T_end,folder,directory,project_dir,GP_used,player_number,tackle_numb,session)
"""

file = open("P2_P29.csv", "r")

csv_reader = csv.reader(file)

lists_from_csv = []

for row in csv_reader:

    lists_from_csv.append(row)


for i in range (len(lists_from_csv)):
    if i>0:
        directory = lists_from_csv[i][8] # Directory of folder to place files
        folder = lists_from_csv[i][8] # Directory of folder with all the data
        project_dir = lists_from_csv[i][7] # of camera calibration
        mass = float(lists_from_csv[i][3]) # mass of tackler
        temp = lists_from_csv[i][2]
        spreadsheetname = 'spreadsheet_'+temp
        T_start = int(lists_from_csv[i][0])
        T_end = int(lists_from_csv[i][1])
        GP_used = int(lists_from_csv[i][6])
        player_number = int(lists_from_csv[i][4])
        tackle_numb = int(lists_from_csv[i][5])
        session = 1

        cb.main(temp,mass,T_start,T_end,folder,directory,project_dir,GP_used,player_number,tackle_numb,session)



#print(lists_from_csv[1][5])

