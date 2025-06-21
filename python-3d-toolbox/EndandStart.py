'''
Find start and end of tackle using Truncate_vid_in_line.py
'''
#Option1: Draw a vector from top to botton find angle with respect to y axis

'''
Description:
Must be in python-3d-toolbox file in order to run code
0. Find start of tackle using perpendicular distance of sholder and middle of bag
1. Finds angle between y-axis and middle-bottom line
2. indicate which csv frame to start from (latest)
3. Finds when end of tackle is reached: use last few frames and height
4. Generate new csv file -> start = bag aligned, end = bag has zero velocity and angle = 270 deg
'''
def main(original_file_folder,start,end):

    #import deeplabcut as dlc
    import pandas as pd
    import numpy as np
    import csv
    import math
    import statistics

    #############################################################################    
    labels = ['middle','bottom','shoulder1'] #top,bottom or top,middle - can be changed
    end_frames = 5 # Last number of frames to average position to end of tackle
    percentage = 10 # height above average
    threshold1 = 0.3 #0.21
    threshold2 = 0.34
    actual_to_truncate_frame = [start,end]
    #############################################################################

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

        bot_vector = [bottom_x[q],bottom_y[q],bottom_z[q]]
        relative_position2 = np.array(shoulder1_vector) - np.array(bot_vector) # In cam1 frame
        r = relative_position2[0]*math.cos(angle*(math.pi/180))-(relative_position2[1]*math.sin(angle*(math.pi/180)))

        #print('')
        #print('row1_middle: ',row1)
        #print('frame: ',top_frame[q])
        #print('r_bottom: ',r)
        #print('')

        
        if (row1<threshold1 and r<threshold2):
            to_truncate_frame[0]=top_frame[q]
            print('Bag on contact at frame: {0} with a middle displacement of: {1} meters'.format(top_frame[q],row1))
            break
        
    ################################################################################################################################################2

    '''
    Detect end of tackle [check velocity and angle]
    '''
    ################################################################################################################################################1

    print('')
    print('End of tackle section')

    df2 = [pd.read_csv(original_file_folder+'top_splined.csv'),pd.read_csv(original_file_folder+'bottom_splined.csv'), pd.read_csv(original_file_folder+'middle_splined.csv'), pd.read_csv(original_file_folder+'upper quartile_splined.csv'), pd.read_csv(original_file_folder+'lower quartile_splined.csv')]

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

    max_frame = max(top_vel_frame[0],bot_vel_frame[0],mid_vel_frame[0],uq_vel_frame[0],lq_vel_frame[0])

    def truncatearray(array_vel=[],array_frame=[],array_pos=-1,max_frame=0):

        start = array_frame.index(max_frame)
        if (array_pos ==-1):
            #print('start: ',start)
            #print('frame: ',array_frame)
            #print('array_vel: ',array_vel)
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

    min_len = min(len(top_vel_frame),len(bot_vel_frame),len(mid_vel_frame),len(uq_vel_frame),len(lq_vel_frame)) # length of column


    # Using last number of frames to detect the end of a tackle

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

    counter = []
    for c in range(min_len):

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

            print('frame at which tackle ends occurs at: {0} at which the point below position is: {1} meters'.format(top_vel_frame[c],counter))
            
            to_truncate_frame[1]=(top_vel_frame[c])
            break



    print('estimated tackle period, frame: ',to_truncate_frame)
    print('actual tackle period, frame: ',actual_to_truncate_frame)
    ################################################################################################################################################2
    return to_truncate_frame

if __name__ == "__main__":
    main()

