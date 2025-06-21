#Option1: Draw a vector from top to botton find angle with respect to y axis

'''
Description:
Must be in python-3d-toolbox file in order to run code
1. Finds angle between y-axis and top-bottom line
2. indicate which csv frame to start from (latest)
3. Finds when end of tackle is reached: use angle and velocity
4. Generate new csv file -> start = bag aligned, end = bag has zero velocity and angle = 270 deg
'''
import deeplabcut as dlc
import pandas as pd
import numpy as np
import csv
import math
import statistics

#############################################################################    
original_file_folder = '/home/uct/Desktop/Testing/data_testing2/session8set2tackle1_b/'
new_truncated_file_path_folder = '/home/uct/Desktop/Testing/data_testing2/session8set2tackle1_b/'
labels = ['middle','bottom','shoulder1'] #top,bottom or top,middle
angle_range = [15,359] # lowest<,>highest -> note angle is between 0-360 deg for alignment
vel_threshold = 0.9 # velocity value to be considered the end of a tackle [m/s]
number_of_points_to_track_vel = 3 # number of points to be below vel_threshold to be considered not a tackle
angle_range_end_of_tackle = [285,270] # lowest<,>=highest -> note angle is between 0-360 deg for end of tackle
labels_new = ['ankle1','knee1','hip1','wrist1','shoulder1','elbow1','ankle2','knee2','hip2','wrist2','shoulder2','elbow2','chin','forehead','top','bottom','middle','upper quartile','lower quartile']
end_frames = 5 # Last number of frames to average position to end of tackle
percentage = 10
threshold1 = 0.3 #0.21
threshold2 = 0.34
#############################################################################

#############################################################################1
'''
to_truncate = [0,0]
to_truncate_frame =[0,0]
df = [pd.read_csv(original_file_folder+'{0}_splined.csv'.format(labels[0])),pd.read_csv(original_file_folder+'{0}_splined.csv'.format(labels[1]))]

df_start_index = [0,0] # df_start_index = [top_offset,bottom_offset] 

flag = False

# Gets starting frame of original video
highest_start_frame = df[0].iloc[0][1]

if (df[1].iloc[0][1]>highest_start_frame):
        highest_start_frame = df[1].iloc[0][1]
        flag = True

if (flag == False):
    
    print ('False: top is the latest frame at frame: ',highest_start_frame)

    df_start_index[0]= 0
    
    df_len = len(df[1]['frame'])

    #print('number of rows in bottom.csv file: ',df_len)
    
    for k in range (df_len):
        if (highest_start_frame == df[1].iloc[k][1]): # Check when frames are equal
            df_start_index[1]=df[1].iloc[k][0]        # append the index of the csv file to offset 
            break
        else: continue

elif (flag == True):

    print ('True: bottom is the latest frame at frame: ', highest_start_frame)

    df_start_index[1]=0
    
    df_len = len(df[0]['frame'])

    #print('number of rows in top.csv file: ',df_len)
    
    for k in range (df_len):
        if (highest_start_frame == df[0].iloc[k][1]):
            df_start_index[0]=df[0].iloc[k][0]
            break
        else: continue

print('df_start_index: ',df_start_index) 
print('frame at which top is with offset: ',df[0].iloc[df_start_index[0]][1])

# finding the vectors

top_frames =[]
bottom_frames = []
# Note: top and bottom frames should be equal

top_x = []
top_y = []
top_z = []
bottom_x = []
bottom_y = []
bottom_z = []

for m in range(df_len):
    
    #print('m: ',m)
    
    #False: df_len = len(bottom - which is the longest) 
    #True: df_len = len(top - which is the longest)
    

    if (flag == False):

        #print('1 ##########################################')

        if (m<len(df[0]['frame'])): # enter while number number of rows in smaller < number of rows in larger
            top_x.append(df[0].iloc[m][3]) # x_pos
            top_y.append(df[0].iloc[m][4]) # y_pos
            top_frames.append(df[0].iloc[m][1]) # frames
            #print('frame: ',df[0].iloc[m][1])
            #print('y_top: ',df[0].iloc[m][4])
            #print('x_top: ',df[0].iloc[m][3])
            top_z.append(df[0].iloc[m][5]) # z_pos
            

        if(df[1].iloc[m][1]>=highest_start_frame): # start after frames are equal
            bottom_x.append(df[1].iloc[m][3])
            bottom_y.append(df[1].iloc[m][4])
            bottom_frames.append(df[1].iloc[m][1]) # frames
            #print('original frame: ',df[1].iloc[m][1])
            #print('with offset frame: ',df[1].iloc[m+df_start_index[1]][1])
            #print('y_bot: ',df[1].iloc[m][4])
            #print('x_bot: ',df[1].iloc[m][3])
            bottom_z.append(df[1].iloc[m][5])
            
        else: continue

    elif (flag == True):

        #print('2 ##########################################')


        if (m<len(df[1]['frame'])):
            bottom_x.append(df[1].iloc[m][3]) # x_pos
            bottom_y.append(df[1].iloc[m][4]) # y_pos
            bottom_frames.append(df[1].iloc[m][1]) # frames
            #print('y_bot: ',df[1].iloc[m][4])
            #print('x_bot: ',df[1].iloc[m][3])
            #print('frame: ',df[1].iloc[m][1])
            bottom_z.append(df[1].iloc[m][5]) # z_pos
            

        if(df[0].iloc[m][1]>=highest_start_frame):
            top_x.append(df[0].iloc[m][3])
            top_y.append(df[0].iloc[m][4])
            top_frames.append(df[0].iloc[m][1])
            #print('original frame: ',df[0].iloc[m][1])
            #print('with offset frame: ',df[0].iloc[m+df_start_index[0]][1])
            #print('y_top: ',df[0].iloc[m][4])
            #print('x_top: ',df[0].iloc[m][3])
            top_z.append(df[0].iloc[m][5])
        
        else: continue
'''
'''
Detecting start of tackle using angle alignment
'''
'''
# Vector
if (len(top_x)>len(bottom_x)):
    cycle = len(bottom_x)
else:
    cycle = len(top_x)

# cycle - number of times to do angle calculation
angle = []
frames = []

for n in range (cycle):
    x_vect = top_x[n]-bottom_x[n]
    y_vect = top_y[n]-bottom_y[n]
    z_vect = top_z[n]-bottom_z[n]

    v0 = [x_vect,y_vect,z_vect] # vector

    mag =  math.sqrt((x_vect*x_vect)+(y_vect*y_vect)+(z_vect*z_vect)) #magintude
   
    angle_wrt_yaxis = math.atan2(x_vect,y_vect)*(180/math.pi)
    angle.append(180-angle_wrt_yaxis)
    #print('angle_wrt_yaxis: ',180-angle_wrt_yaxis)
    
    # Indicate which frame to look at
    if (flag == False):
        #print('frame_top: ',top_frames[n])
        frames.append(top_frames[n])
    elif (flag == True):
        #print('frame_bot: ',bottom_frames[n])
        frames.append(bottom_frames[n])

for b in range (len(angle)):
    if (angle[b]<angle_range[0] or angle[b]>angle_range[1]):
        print('Bag aligned at frame: {0} with an angle of: {1}'.format(frames[b],angle[b]))
        to_truncate_frame[0]=(frames[b])
        break # remove break if you require more points
        
'''
#############################################################################2
'''
Detecting start of tackle using perpendicular distance between line of bag and shoulder 
'''
################################################################################################################################################1

to_truncate_frame =[0,0]
df = [pd.read_csv(original_file_folder+'{0}_splined.csv'.format(labels[0])),pd.read_csv(original_file_folder+'{0}_splined.csv'.format(labels[1])),pd.read_csv(original_file_folder+'{0}_splined.csv'.format(labels[2]))]
df_start_index = [0,0,0] # df_start_index = [top_offset,bottom_offset,shoulder1] 

top_frame = []
top_x = []
top_y = []
top_z = []

bottom_frame = []
bottom_x=[]
bottom_y=[]
bottom_z=[]

shoudler1_frame =[]
shoudler1_x=[]
shoudler1_y=[]
shoudler1_z=[]

frames = []
x_distance = []

def fillarray(frame,x,y,z,df_used): # Append velocity and frames to array

    len_of_df = len(df_used['frame'])
    
    for t in range(len_of_df):
        
        frame.append(df_used.iloc[t][1])
        x.append(df_used.iloc[t][3])
        y.append(df_used.iloc[t][4])
        z.append(df_used.iloc[t][5])
        
fillarray(top_frame,top_x,top_y,top_z,df[0])
fillarray(bottom_frame,bottom_x,bottom_y,bottom_z,df[1])
fillarray(shoudler1_frame,shoudler1_x,shoudler1_y,shoudler1_z,df[2])

start_frame = max(top_frame[0],shoudler1_frame[0],bottom_frame[0])

def shortenarray(frame,x,y,z,start_frame):
    start_index = frame.index(start_frame)
    df_start_index.append(start_index)
    return frame[start_index:],x[start_index:],y[start_index:],z[start_index:]

top_frame,top_x,top_y,top_z = shortenarray(top_frame,top_x,top_y,top_z,start_frame)
bottom_frame,bottom_x,bottom_y,bottom_z = shortenarray(bottom_frame,bottom_x,bottom_y,bottom_z,start_frame)
shoudler1_frame,shoudler1_x,shoudler1_y,shoudler1_z = shortenarray(shoudler1_frame,shoudler1_x,shoudler1_y,shoudler1_z,start_frame)

cycle = min(len(top_frame),len(bottom_frame),len(shoudler1_frame))

for q in range (cycle):

    frames.append(top_frame[q])
    shoulder1_vector = [shoudler1_x[q],shoudler1_y[q],shoudler1_z[q]]
    top_vector = [top_x[q],top_y[q],top_z[q]]

    relative_position = np.array(shoulder1_vector) - np.array(top_vector) # In cam1 frame

    
    
    # Find angle wrt y axis
    x_vect = top_x[q]-bottom_x[q]
    y_vect = top_y[q]-bottom_y[q]
    z_vect = top_z[q]-bottom_z[q]
    mag =  math.sqrt((x_vect*x_vect)+(y_vect*y_vect)+(z_vect*z_vect)) #magintude
    angle_wrt_yaxis = math.atan2(x_vect,y_vect)*(180/math.pi)
    angle = 180-angle_wrt_yaxis
    
    # Find the rotation matrix wrt the y axis - note math.trig = radians

    row1 = relative_position[0]*math.cos(angle*(math.pi/180))-(relative_position[1]*math.sin(angle*(math.pi/180)))
    row2 = relative_position[0]*math.sin(angle*(math.pi/180))+(relative_position[1]*math.cos(angle*(math.pi/180)))

    x_distance.append(row1)
    '''
    R = np.array([[math.cos(angle),0,math.sin(angle)],[0,1,0],[-math.sin(angle),0,math.cos(angle)]])
    relative_position_bag = camera.rotate([relative_position], R) 
    '''
    bot_vector = [bottom_x[q],bottom_y[q],bottom_z[q]]
    relative_position2 = np.array(shoulder1_vector) - np.array(bot_vector) # In cam1 frame
    r = relative_position2[0]*math.cos(angle*(math.pi/180))-(relative_position2[1]*math.sin(angle*(math.pi/180)))

    print('')
    print('row1_middle: ',row1)
    print('frame: ',top_frame[q])
    print('r_bottom: ',r)
    print('')

    
    if (row1<threshold1 and r<threshold2):
        to_truncate_frame[0]=top_frame[q]
        print('Bag on contact at frame: {0} with a middle displacement of: {1}'.format(top_frame[q],row1))
        break
    
################################################################################################################################################2


'''
Detect end of tackle [check velocity and angle]
'''
print('')
print('End of tackle section')

df2 = [pd.read_csv(original_file_folder+'top_splined.csv'),pd.read_csv(original_file_folder+'bottom_splined.csv'), pd.read_csv(original_file_folder+'middle_splined.csv'), pd.read_csv(original_file_folder+'upper quartile_splined.csv'), pd.read_csv(original_file_folder+'lower quartile_splined.csv')]

#####################################################################1
'''
df4 = pd.read_csv(original_file_folder+'ankle1_splined.csv')
ankle1_y_pos = []
ankle1_vel_frame =[]
df4_len = len(df4['frame'])
for length in range(df4_len):
    ankle1_vel_frame.append(df4.iloc[length][1])
    ankle1_y_pos.append(df4.iloc[length][4])

df5 = pd.read_csv(original_file_folder+'ankle2_splined.csv')
ankle2_y_pos = []
ankle2_vel_frame =[]
df5_len = len(df5['frame'])
for length in range(df5_len):
    ankle2_vel_frame.append(df5.iloc[length][1])
    ankle2_y_pos.append(df5.iloc[length][4])

df6 = pd.read_csv(original_file_folder+'knee1_splined.csv')
knee1_y_pos = []
knee1_vel_frame =[]
df6_len = len(df6['frame'])
for length in range(df6_len):
    knee1_vel_frame.append(df6.iloc[length][1])
    knee1_y_pos.append(df6.iloc[length][4])
'''
#####################################################################2

top_vel = []
top_y_pos = []
top_vel_frame =[]

bot_vel = []
bot_y_pos = []
bot_vel_frame =[]

mid_vel = []
mid_y_pos = []
mid_vel_frame =[]

uq_vel = []
uq_y_pos = []
uq_vel_frame =[]

lq_vel = []
lq_y_pos = []
lq_vel_frame =[]

def appendtoarray(array_vel,array_frame,array_y_pos,df_to_use): # Append velocity and frames to array

    len_of_df = len(df_to_use['frame'])
    
    for t in range(len_of_df):
        
        array_frame.append(df_to_use.iloc[t][1])
        array_y_pos.append(df_to_use.iloc[t][4])
        mag = math.sqrt((df_to_use.iloc[t][8]*df_to_use.iloc[t][8])+(df_to_use.iloc[t][9]*df_to_use.iloc[t][9])+(df_to_use.iloc[t][10]*df_to_use.iloc[t][10]))
        array_vel.append(mag)

appendtoarray(top_vel,top_vel_frame,top_y_pos,df2[0])
appendtoarray(bot_vel,bot_vel_frame,bot_y_pos,df2[1])
appendtoarray(mid_vel,mid_vel_frame,mid_y_pos,df2[2])
appendtoarray(uq_vel,uq_vel_frame,uq_y_pos,df2[3])
appendtoarray(lq_vel,lq_vel_frame,lq_y_pos,df2[4])

#####################################################################1

#max_frame = max(top_vel_frame[0],bot_vel_frame[0],mid_vel_frame[0],uq_vel_frame[0],lq_vel_frame[0],ankle1_vel_frame[0],ankle2_vel_frame[0],knee1_vel_frame[0])
max_frame = max(top_vel_frame[0],bot_vel_frame[0],mid_vel_frame[0],uq_vel_frame[0],lq_vel_frame[0])
#####################################################################2

def truncatearray(array_vel=[],array_frame=[],array_pos=-1,max_frame=0):

    start = array_frame.index(max_frame)
    if (array_pos ==-1):
        print('start: ',start)
        print('frame: ',array_frame)
        print('array_vel: ',array_vel)
        return array_vel[start:],array_frame[start:]
    else:
        return array_vel[start:],array_frame[start:],array_pos[start:]

# Below arrays are truncated

# Truncate velocity and position
top_vel,top_vel_frame, top_y_pos= truncatearray(top_vel,top_vel_frame,top_y_pos,max_frame)
bot_vel,bot_vel_frame, bot_y_pos= truncatearray(bot_vel,bot_vel_frame,bot_y_pos,max_frame)
mid_vel,mid_vel_frame, mid_y_pos = truncatearray(mid_vel,mid_vel_frame,mid_y_pos,max_frame)
uq_vel,uq_vel_frame, uq_y_pos = truncatearray(uq_vel,uq_vel_frame,uq_y_pos,max_frame)
lq_vel,lq_vel_frame, lq_y_pos = truncatearray(lq_vel,lq_vel_frame,lq_y_pos,max_frame)

# Truncate angle
#tr_angle,tr_frame = truncatearray(angle,frames,max_frame=max_frame)
'''
#####################################################################1
# Truncate ankles and knee
ankle1_y_pos,ankle1_vel_frame = truncatearray(ankle1_y_pos,ankle1_vel_frame,max_frame=max_frame)
ankle2_y_pos,ankle2_vel_frame = truncatearray(ankle2_y_pos,ankle2_vel_frame,max_frame=max_frame)
knee1_y_pos,knee1_vel_frame = truncatearray(knee1_y_pos,knee1_vel_frame,max_frame=max_frame)
#####################################################################2
'''
min_len = min(len(top_vel_frame),len(bot_vel_frame),len(mid_vel_frame),len(uq_vel_frame),len(lq_vel_frame)) # length of column

#####################################################################1
'''
# if =1 remove condition
ankle1_condition = 0
ankle2_condition = 0
knee1_condition = 0

if (min_len>len(ankle1_vel_frame)): ankle1_condition = 1
if (min_len>len(ankle2_vel_frame)): ankle2_condition = 1
if (min_len>len(knee1_vel_frame)): knee1_condition = 1
'''
#####################################################################2


# Uncomment if end of tackle depends on angle and velocity
'''
####################################################################################################################1
end_of_tackle_frame = []
counter=[]
for c in range(min_len):

    del counter
    counter = [] # number of parts to be considered ground

    if(top_vel[c]<= vel_threshold):
        counter.append('top')

    if(bot_vel[c]<= vel_threshold):
        counter.append('bot')

    if(mid_vel[c]<= vel_threshold):
        counter.append('mid')

    if(uq_vel[c]<= vel_threshold):
        counter.append('uq')

    if(lq_vel[c]<= vel_threshold):
        counter.append('lq')

    if (len(counter)>=number_of_points_to_track_vel and tr_angle[c]<angle_range_end_of_tackle[0] and tr_angle[c]>=angle_range_end_of_tackle[1]):
        
        
        #for ii in counter:

            #if (ii == 'top'):print('top_vel[c]: ',top_vel[c])
            #if (ii == 'bot'):print('bot_vel[c]: ',bot_vel[c])
            #if (ii == 'mid'):print('mid_vel[c]: ',mid_vel[c])
            #if (ii == 'uq'):print('uq_vel[c]: ',uq_vel[c])
            #if (ii == 'lq'):print('lq_vel[c]: ',lq_vel[c])
        

        print('frame at which tackle ends occurs at: {0} at which the angle is: {1}'.format(top_vel_frame[c],tr_angle[c]))
        
        end_of_tackle_frame.append(top_vel_frame[c])
        to_truncate_frame.append(top_vel_frame[c])
        break # remove break if you require more points
####################################################################################################################2
'''


# Using last number of frames to detect the end of a tackle

####################################################################################################################1

def lastframes(y_pos,iterations,min_len):

    positions = []

    for i in range(iterations,0,-1):
        positions.append(y_pos[min_len-i])
    return positions

# last y position values
p_top = lastframes(top_y_pos,end_frames,min_len) 
p_bot = lastframes(bot_y_pos,end_frames,min_len)  
p_mid = lastframes(mid_y_pos,end_frames,min_len)
p_uq = lastframes(uq_y_pos,end_frames,min_len)
p_lq = lastframes(lq_y_pos,end_frames,min_len)

y_top = statistics.mean(p_top)
y_bot = statistics.mean(p_bot)
y_mid = statistics.mean(p_mid)
y_uq = statistics.mean(p_uq)
y_lq = statistics.mean(p_lq)

y_top_max = y_top-abs(y_top*percentage/100)
y_bot_max = y_bot-abs(y_bot*percentage/100)
y_mid_max = y_mid-abs(y_mid*percentage/100)
y_uq_max = y_uq -abs(y_uq*percentage/100)
y_lq_max = y_lq-abs(y_lq*percentage/100)
'''
print('')
print('y_top: ',y_top)
print('y_bot: ',y_bot)
print('y_mid: ',y_mid)
print('y_uq: ',y_uq)
print('y_lq: ',y_lq)
'''
print('')

counter = []
for c in range(min_len):

    '''
    print('')
    print('y_top_max: ',y_top_max)
    print('y_bot_max: ',y_bot_max)
    print('y_mid_max: ',y_mid_max)
    print('y_uq_max: ',y_uq_max)
    print('y_lq_max: ',y_lq_max)
    print('')
    print('top_y_pos[c]: ',top_y_pos[c])
    print('bot_y_pos[c]: ',bot_y_pos[c])
    print('mid_y_pos[c]: ',mid_y_pos[c])
    print('uq_y_pos[c]: ',uq_y_pos[c])
    print('lq_y_pos[c]: ',lq_y_pos[c])
    print('top_vel_frame[c]: ',top_vel_frame[c])
    print('')
    '''
    del counter
    counter = []
    
    if(top_y_pos[c]>= y_top_max or top_y_pos[c]>= y_bot_max or top_y_pos[c]>= y_mid_max or top_y_pos[c]>= y_uq_max or top_y_pos[c]>= y_lq_max):
        counter.append('top')

    if(bot_y_pos[c]>= y_bot_max or bot_y_pos[c]>= y_top_max or bot_y_pos[c]>= y_mid_max or bot_y_pos[c]>= y_uq_max or bot_y_pos[c]>= y_lq_max):
        counter.append('bot')

    if(mid_y_pos[c]>= y_mid_max or mid_y_pos[c]>= y_top_max or mid_y_pos[c]>= y_bot_max or mid_y_pos[c]>= y_uq_max or mid_y_pos[c]>= y_lq_max):
        counter.append('mid')

    if(uq_y_pos[c]>= y_uq_max or uq_y_pos[c]>= y_top_max or uq_y_pos[c]>= y_bot_max or uq_y_pos[c]>= y_mid_max or uq_y_pos[c]>= y_lq_max):
        counter.append('uq')

    if(lq_y_pos[c]>= y_lq_max or lq_y_pos[c]>= y_top_max or lq_y_pos[c]>= y_bot_max or lq_y_pos[c]>= y_uq_max or lq_y_pos[c]>= y_mid_max):
        counter.append('lq')

    if (len(counter)>0):

        print('frame at which tackle ends occurs at: {0} at which the point below position is: {1}'.format(top_vel_frame[c],counter))
        
        to_truncate_frame[1]=(top_vel_frame[c])
        break

'''
#Finds the min displacement 
###################################################################################a
end_tac_index = frames.index(to_truncate_frame[1])
min_val_temp = np.array(x_distance[:(end_tac_index+1)])
min_val = min(abs(min_val_temp))
min_val_index = x_distance.index(min_val)
to_truncate_frame[0]=frames[min_val_index]
print('Bag on contact at frame: {0} with an displacement of: {1}'.format(frames[min_val_index],x_distance[min_val_index]))
###################################################################################b
'''

print('to_truncate frame: ',to_truncate_frame)
####################################################################################################################2



# Using ankle and bag position to detect the end of a tackle
'''
####################################################################################################################1

counter = []
for c in range(min_len):

    del counter
    counter = []

    if(((top_y_pos[c]>= ankle1_y_pos[c]) or (top_y_pos[c]>= ankle2_y_pos[c])) and top_y_pos[c]>=knee1_y_pos[c]) :
        counter.append('top')

    if(((bot_y_pos[c]>= ankle1_y_pos[c]) or (bot_y_pos[c]>= ankle2_y_pos[c]) )and bot_y_pos[c]>=knee1_y_pos[c]):
        counter.append('bot')

    if(((mid_y_pos[c]>= ankle1_y_pos[c]) or (mid_y_pos[c]>= ankle2_y_pos[c])) and mid_y_pos[c]>=knee1_y_pos[c]):
        counter.append('mid')

    if(((uq_y_pos[c]>= ankle1_y_pos[c]) or (uq_y_pos[c]>= ankle2_y_pos[c]) )and uq_y_pos[c]>=knee1_y_pos[c]):
        counter.append('uq')

    if(((lq_y_pos[c]>= ankle1_y_pos[c]) or (lq_y_pos[c]>= ankle2_y_pos[c])) and lq_y_pos[c]>=knee1_y_pos[c]):
        counter.append('lq')

    if (len(counter)>0):

        print('frame at which tackle ends occurs at: {0} at which the point below position is: {1}'.format(top_vel_frame[c],counter))
        
        to_truncate_frame.append(top_vel_frame[c])
        break
    
print('to_truncate frame: ',to_truncate_frame)
####################################################################################################################
'''

# Using last number of frames to detect the end of a tackle, ankle and knee

####################################################################################################################
'''
def lastframes(y_pos,iterations,min_len):

    positions = []

    for i in range(iterations,0,-1):
        positions.append(y_pos[min_len-i])
    return positions


# last y position values
p_top = lastframes(top_y_pos,end_frames,min_len) 
p_bot = lastframes(bot_y_pos,end_frames,min_len)  
p_mid = lastframes(mid_y_pos,end_frames,min_len)
p_uq = lastframes(uq_y_pos,end_frames,min_len)
p_lq = lastframes(lq_y_pos,end_frames,min_len)

y_top = statistics.mean(p_top)
y_bot = statistics.mean(p_bot)
y_mid = statistics.mean(p_mid)
y_uq = statistics.mean(p_uq)
y_lq = statistics.mean(p_lq)


counter = []
for c in range(min_len):

    del counter
    counter = []

    if(top_y_pos[c]>= y_top or top_y_pos[c]>= y_bot or top_y_pos[c]>= y_mid or top_y_pos[c]>= y_uq or top_y_pos[c]>= y_lq or ((top_y_pos[c]>= ankle1_y_pos[c]) or (top_y_pos[c]>= ankle2_y_pos[c])) and top_y_pos[c]>=knee1_y_pos[c]):
        counter.append('top')

    if(bot_y_pos[c]>= y_bot or bot_y_pos[c]>= y_top or bot_y_pos[c]>= y_mid or bot_y_pos[c]>= y_uq or bot_y_pos[c]>= y_lq or ((bot_y_pos[c]>= ankle1_y_pos[c]) or (bot_y_pos[c]>= ankle2_y_pos[c]) )and bot_y_pos[c]>=knee1_y_pos[c]):
        counter.append('bot')

    if(mid_y_pos[c]>= y_mid or mid_y_pos[c]>= y_top or mid_y_pos[c]>= y_bot or mid_y_pos[c]>= y_uq or mid_y_pos[c]>= y_lq or ((mid_y_pos[c]>= ankle1_y_pos[c]) or (mid_y_pos[c]>= ankle2_y_pos[c])) and mid_y_pos[c]>=knee1_y_pos[c]):
        counter.append('mid')

    if(uq_y_pos[c]>= y_uq or uq_y_pos[c]>= y_top or uq_y_pos[c]>= y_bot or uq_y_pos[c]>= y_mid or uq_y_pos[c]>= y_lq or ((uq_y_pos[c]>= ankle1_y_pos[c]) or (uq_y_pos[c]>= ankle2_y_pos[c])) and uq_y_pos[c]>=knee1_y_pos[c]):
        counter.append('uq')

    if(lq_y_pos[c]>= y_lq or lq_y_pos[c]>= y_top or lq_y_pos[c]>= y_bot or lq_y_pos[c]>= y_uq or lq_y_pos[c]>= y_mid or ((lq_y_pos[c]>= ankle1_y_pos[c]) or (lq_y_pos[c]>= ankle2_y_pos[c])) and lq_y_pos[c]>=knee1_y_pos[c]):
        counter.append('lq')

    if (len(counter)>0):

        print('frame at which tackle ends occurs at: {0} at which the point below position is: {1}'.format(top_vel_frame[c],counter))
        
        to_truncate_frame.append(top_vel_frame[c])
        break
    
print('to_truncate frame: ',to_truncate_frame)
'''
####################################################################################################################


'''
Truncate video using to_truncate
'''
####################################################################################################################1
'''
for zp in range (len(labels_new)):

    df3 = pd.read_csv(original_file_folder+labels_new[zp]+'_splined.csv')

    new_file_path = new_truncated_file_path_folder+labels_new[zp]+'_tackle.csv'

    # Create a new csv file
    with open(new_file_path, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    # Include headings of the new csv file
    headings =['index', 'frame', 'label' ,'x_pos', 'y_pos', 'z_pos', 'point_index','time(sec)','x_vel','y_vel','z_vel','x_acc','y_acc','z_acc']
    with open(r'{0}'.format(new_file_path), 'a') as f:
        writer = csv.writer(f)
        writer.writerow(headings) 

    array = []
    
    max_length_of_csv = len(df3['index'])

    flag2 = False

    for check in range (max_length_of_csv):
        if(df3.iloc[check][1]==to_truncate_frame[0]):
            to_truncate[0] = df3.iloc[check][0]

        if(df3.iloc[check][1]==to_truncate_frame[1]):
            to_truncate[1] = df3.iloc[check][0]
            flag2 = True

    if (flag2==False):
        print((labels_new[zp])+' that does not have a frame range of: ',to_truncate_frame) 
        if(max_length_of_csv==0):
            to_truncate[1] =0
        else:
            to_truncate[1] = df3.iloc[max_length_of_csv-1][0]


    for y in range (to_truncate[0],to_truncate[1]+1):
        print('frame: ',df3.iloc[y][1])
        array.append(y-to_truncate[0])         # current index 
        array.append(df3.iloc[y][1]) # frame 
        array.append(labels_new[zp]) # label
        array.append(df3.iloc[y][3]) # x
        array.append(df3.iloc[y][4]) # y
        array.append(df3.iloc[y][5]) # z
        array.append(df3.iloc[y][6]) # point index
        array.append(df3.iloc[y][7]) # time
        array.append(df3.iloc[y][8]) # x_vel
        array.append(df3.iloc[y][9]) # y_vel
        array.append(df3.iloc[y][10]) # z_vel
        array.append(df3.iloc[y][11]) # x_acc
        array.append(df3.iloc[y][12]) # y_acc
        array.append(df3.iloc[y][13]) # z_acc
      
        
        #writes array to new csv file
        with open(r'{0}'.format(new_file_path), 'a') as f:
            writer = csv.writer(f)
            writer.writerow(array)

        del array
        array = []
'''
####################################################################################################################2