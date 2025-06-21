import csv
import combine134

def delay():
    for i in range(10):
        for j in range (10):
            pass
done = []

compled =  ['Tackle6_Session6_Set1', 'Tackle1_Session12_Set1','Tackle1_Session6_Set1', 'Tackle3_Session6_Set1','Tackle5_Session13_Set1', 'Tackle6_Session13_Set1','Tackle1_Session3_Set1', 'Tackle6_Session4_Set2', 'Tackle5_Session9_Set1', 'Tackle2_Session10_Set3','Tackle2_Session6_Set1','Tackle4_Session4_Set2','Tackle4_Session12_Set1', 'Tackle5_Session12_Set1', 'Tackle3_Session12_Set2', 'Tackle4_Session12_Set2', 'Tackle5_Session12_Set2', 'Tackle1_Session13_Set1','Tackle2_Session3_Set1', 'Tackle3_Session3_Set1', 'Tackle4_Session3_Set1', 'Tackle5_Session3_Set1', 'Tackle6_Session3_Set1', 'Tackle1_Session3_Set2', 'Tackle2_Session3_Set2', 'Tackle3_Session3_Set2', 'Tackle4_Session3_Set2', 'Tackle5_Session3_Set2', 'Tackle6_Session3_Set2', 'Tackle5_Session5_Set2', 'Tackle1_Session8_Set1', 'Tackle2_Session8_Set1', 'Tackle3_Session8_Set1', 'Tackle4_Session8_Set1', 'Tackle5_Session8_Set1', 'Tackle6_Session8_Set1', 'Tackle3_Session9_Set1', 'Tackle6_Session9_Set1', 'Tackle1_Session9_Set2', 'Tackle3_Session9_Set2', 'Tackle4_Session9_Set2', 'Tackle1_Session10_Set3', 'Tackle4_Session10_Set3', 'Tackle5_Session10_Set3', 'Tackle6_Session10_Set3']

with open('valid_errors.csv') as csv_file: 
    csv_reader = list(csv.reader(csv_file, delimiter=','))
    print(csv_reader[0])
    print(len(csv_reader))

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

