import csv
import combine134
from os import listdir
from os.path import isfile, join
import pandas as pd

onlyfiles = [f for f in listdir("/home/uct/Analyse_videos/sort/final_valid/valid") if isfile(join("/home/uct/Analyse_videos/sort/final_valid/valid", f))]
xlsx = []


for i in range(len(onlyfiles)):
	if ".xlsx" in onlyfiles[i]:
		xlsx.append(onlyfiles[i])
	else: pass
	
print(xlsx)

df = pd.read_excel (r'/home/uct/Analyse_videos/sort/final_valid/valid/'+xlsx[0]) #place "r" before the path string to address special character, such as '\'. Don't forget to put the file name at the end of the path + '.xlsx'
print (df['Video'].values[0])


import xlsxwriter

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Expenses01.xlsx')
worksheet = workbook.add_worksheet()

# Some data we want to write to the worksheet.
expenses = (
    ['Rent', 1000],
    ['Gas',   100],
    ['Food',  300],
    ['Gym',    50],
)

# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

# Iterate over the data and write it out row by row.
for item, cost in (expenses):
    worksheet.write(row, col,     item)
    worksheet.write(row, col + 1, cost)
    row += 1

# Write a total using a formula.
worksheet.write(row, 0, 'Total')
worksheet.write(row, 1, '=SUM(B1:B4)')

workbook.close()



# Video	Tackler	Session	Tackle Number	Start Frame Est	End Frame Est	Start Frame Act	End Frame Act	Mass_of_bag[kg]	Mass_of_tackler[kg]	Vi_middle_bag[m/s]	Vf_middle_bag[m/s]	Vi_lower_bag[m/s]	Vf_lower_bag[m/s]	Vi_shoulder1[m/s]	Vf_shoulder1[m/s]	Vi_hip1[m/s]	Vf_hip1[m/s]	Relative_pos_shoudler1_middle[m]	Relative_pos_shoudler1_bottom[m]	Relative_pos_shoudler1_top[m]	Relative_pos_elbow1_top[m]	Relative_pos_wrist1_top[m]	Bag_Energy_x_impact_middle[J]	Bag_Energy_x_impact_lower[J]	Bag_Force_x_impact_middle[N]	Bag_Force_x_impact_lower[N]	Tackler_Energy_x_impact_left_hip[J]	Tackler_Force_x_impact_left_shoulder[N]	Power_of_tackler_x_left_shoulder[W]	Momentum_bag_lower_before_impact[kgm/s]	Momentum_left_hip_before_impact[kgm/s]	Momentum_baghip_before_impact(calculated)	Velocity_after_impact_calculated	Velocity_after_impact_actual	Distance_x_calculated[m]	x_distance_travelled[m]	Contact_time[s]	Ai_left_shoulder


'''


df = pd.read_excel("/home/uct/Analyse_videos/sort/final_valid/valid/"+xlsx[0]) # can also index sheet by name or fetch all sheets
mylist = df['column name'].tolist()
print(mylist)


with open("/home/uct/Analyse_videos/sort/final_valid/valid/"+xlsx[0]) as csv_file: 
    csv_reader = list(csv.reader(csv_file, delimiter=','))
    print(csv_reader[0])
    print(len(csv_reader))
'''    
'''
for i in range (len(csv_reader)):
    
    if i>0 and (csv_reader[i][0] not in compled):

        temp = csv_reader[i][0]
        mass = float(csv_reader[i][3].replace(",","."))
        T_start = int(csv_reader[i][6])
        T_end = int(csv_reader[i][7])
        folder = "/home/uct/Analyse_videos/sort/final_valid/valid/"
        directory = "/home/uct/Analyse_videos/sort/final_valid/valid/"
        project_dir = "/home/uct/Analyse_videos/sort/valid_camera_calib/"+csv_reader[i][4]
        GP_used = int(csv_reader[i][2])
        player_number = csv_reader[i][1]
        print()
        print("Generating spreadsheet for {0} ...".format(temp))
        print()
        combine134.main(temp,mass,T_start,T_end,folder,directory,project_dir,GP_used,player_number)
        done.append(temp)
        print("#############################################################")
        print("Files that are completed = ",done)
        print("#############################################################")
        delay()
'''
