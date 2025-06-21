'''
Magnitude vectors of point on person and bag should continue to decrease
'''
import deeplabcut as dlc
import cv2
import numpy as np
import pandas as pd
import csv
import scipy
import math

#############################################################################    
original_file_path = '/home/uct/Desktop/Testing/data_testing2/Tackle5_session13_set2/'
new_file_path_folder = '/home/uct/Desktop/Testing/data_testing2/Tackle5_session13_set2/'
labels = ['middle', 'shoulder1'] # can be changed but must be in the format of ['moving right(bag)','moving left (body part)']
vel_lim = 6 #set assumed/approximated relative velocity at impact [cannot be less than 6]
pos_lim = 0.6
fps = 119
#############################################################################

#df = [pd.read_csv(original_file_path+labels[0]+'_tackle.csv'),pd.read_csv(original_file_path+labels[1]+'_tackle.csv')]
df = [pd.read_csv(original_file_path+labels[0]+'_splined.csv'),pd.read_csv(original_file_path+labels[1]+'_splined.csv')]

df_start_index = [0,0] # df_start_index = [approach to right,approach to left] 

max_iterations = 0  # Find the max number of times you can iterate after frame is found

flag = False

# Gets starting frame of original video
highest_start_frame = df[0].iloc[0][1]

if (df[1].iloc[0][1]>highest_start_frame):
        highest_start_frame = df[1].iloc[0][1]
        flag = True

if (flag == False):
    
    print ('False: {0} is the latest frame at frame: {1}'.format(labels[0],highest_start_frame))

    df_start_index[0]= 0
    
    df_len = len(df[1]['frame'])

    #print('number of rows in bottom.csv file: ',df_len)
    
    for k in range (df_len):
        if (highest_start_frame == df[1].iloc[k][1]): # Check when frames are equal
            df_start_index[1]=df[1].iloc[k][0]        # append the index of the csv file to offset 
            break
        else: continue

    if(len(df[0]['frame'])<=len(df[1]['frame'][df_start_index[1]:])):
        max_iterations = len(df[0]['frame'])
    else:
         max_iterations = len(df[1]['frame'][df_start_index[1]:])


elif (flag == True):

    print ('True: {0} is the latest frame at frame: {1}'.format(labels[1],highest_start_frame))

    df_start_index[1]=0
    
    df_len = len(df[0]['frame'])

    #print('number of rows in top.csv file: ',df_len)
    
    for k in range (df_len):
        if (highest_start_frame == df[0].iloc[k][1]):
            df_start_index[0]=df[0].iloc[k][0]
            break
        else: continue

    if(len(df[1]['frame'])<=len(df[0]['frame'][df_start_index[1]:])):
        max_iterations = len(df[1]['frame'])
    else:
         max_iterations = len(df[0]['frame'][df_start_index[1]:])

print('df_start_index: ',df_start_index)
print('{0}: {1}'.format(labels[0],df[0].iloc[df_start_index[0]][1]))
print('{0}: {1}'.format(labels[1],df[1].iloc[df_start_index[1]][1]))
#print('check: ',len(df[1]['frame'][df_start_index[1]:]))

rel_vel = []
rel_pos = []
frame = []
time =[]
x_acc = [] # of the bag

for i in range(max_iterations):
    
    x_vel_right = df[0].iloc[i+df_start_index[0]][8]
    y_vel_right = df[0].iloc[i+df_start_index[0]][9]
    z_vel_right = df[0].iloc[i+df_start_index[0]][10]  

    x_vel_left = df[1].iloc[i+df_start_index[1]][8]
    y_vel_left = df[1].iloc[i+df_start_index[1]][9]
    z_vel_left = df[1].iloc[i+df_start_index[1]][10]
    
    x_pos_right = df[0].iloc[i+df_start_index[0]][3]
    y_pos_right = df[0].iloc[i+df_start_index[0]][4]
    z_pos_right = df[0].iloc[i+df_start_index[0]][5]  

    x_pos_left = df[1].iloc[i+df_start_index[1]][3]
    y_pos_left = df[1].iloc[i+df_start_index[1]][4]
    z_pos_left = df[1].iloc[i+df_start_index[1]][5]
    
    relative_velocity_vector = [[x_vel_left-x_vel_right],[y_vel_left-y_vel_right],[z_vel_left-z_vel_right]] #V_left_right
    relative_position_vector = [[x_pos_left-x_pos_right],[y_pos_left-y_pos_right],[z_pos_left-z_pos_right]] #V_left_right

    relative_velocity_mag = math.sqrt((relative_velocity_vector[0][0]*relative_velocity_vector[0][0])+(relative_velocity_vector[1][0]*relative_velocity_vector[1][0])+(relative_velocity_vector[2][0]*relative_velocity_vector[2][0]))

    relative_position_mag = math.sqrt((relative_position_vector[0][0]*relative_position_vector[0][0])+(relative_position_vector[1][0]*relative_position_vector[1][0])+(relative_position_vector[2][0]*relative_position_vector[2][0]))


    rel_vel.append(relative_velocity_mag)
    rel_pos.append(relative_position_mag)
    frame.append(df[0].iloc[i+df_start_index[0]][1])
    time.append(df[0].iloc[i+df_start_index[0]][7])
    x_acc.append(df[0].iloc[i+df_start_index[0]][11])

    #print('relative_velocity vector: ',relative_velocity_vector)
    print('relative_velocity_mag: ',relative_velocity_mag)
    #print('relative_position_vector: ',relative_position_vector)
    print('relative_position_mag: ',relative_position_mag)
    print('frame: ',df[0].iloc[i+df_start_index[0]][1])
    print('frame_check: ',df[1].iloc[i+df_start_index[1]][1])
    print(' ')

def turningpoints(xx):
    N=[]
    
    for p in range(1,len(xx)-1):
        
        if(xx[p]=='nan'):
            continue
      
        else:
            #print('')
            if ((xx[p-1] < xx[p] and xx[p+1] < xx[p]) or (xx[p-1] > xx[p] and xx[p+1] > xx[p])):
                #print('True')
                N.append(time[p])
    return N


tp = turningpoints(x_acc)
frame_at_tp = []

for q in range(len(tp)): frame_at_tp.append(fps*tp[q])
#print('tp_frame: ',frame_at_tp)

for s in range(len(tp)): frame_at_tp[s] = int(frame_at_tp[s])
print('tp_frame: ',frame_at_tp)

for j in range(len(rel_vel)):

    if(rel_vel[j]<=vel_lim and (frame[j] in frame_at_tp) and (rel_pos[j]<=pos_lim)):#if(rel_vel[j]<=vel_lim and (frame[j] in frame_at_tp) and (rel_pos[j]<=pos_lim)):
        print('Relative velocity value: ',rel_vel[j])
        print('Tackle occurs at frame: ',frame[j])
        print('Tackle occurs after edit at frame: ',frame[j]-2)
        break