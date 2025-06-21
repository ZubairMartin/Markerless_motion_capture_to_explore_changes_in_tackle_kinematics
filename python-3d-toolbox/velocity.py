# Generate new csv file including velocity after filtered

def main(original_file_path,new_file_path_folder):

    #import deeplabcut as dlc
    import pandas as pd
    import numpy as np
    import csv
    import matplotlib.pyplot as plt

    #############################################################################    
    labels = ['ankle1','knee1','hip1','wrist1','shoulder1','elbow1','ankle2','knee2','hip2','wrist2','shoulder2','elbow2','chin','forehead','top','bottom','middle','upper quartile','lower quartile']
    #############################################################################

    for k in range (len(labels)):

        # Read filtered CSV (of one body part)
        df = pd.read_csv(original_file_path+labels[k]+'_filtered.csv')

        new_file_path = new_file_path_folder+labels[k]+'_velocity.csv'

        # Create a new csv file
        with open(new_file_path, 'wb') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        # Include headings of the new csv file
        headings =['index', 'frame', 'label' ,'x', 'y', 'z', 'point_index','time(sec)','x_velocity','y_velocity','z_velocity']
        with open(r'{0}'.format(new_file_path), 'a') as f:
            writer = csv.writer(f)
            writer.writerow(headings) 

        # Array that is used to append to csv file
        array = []

        point_index=len(df['point_index'])
        index=0
        frame1=0
        frame2=0
        fps = 119
        frames = 244
        time1=0
        time2=0
        x1=0
        x2=0
        y1=0
        y2=0
        z1=0
        z2=0

        for i in range (point_index):
            
            # Clear array every new frame
            frame2 = df.iloc[i][1]
            if (frame1==frame2):
                frame1=frame2 #not needed
            else:
                del array
                array = []
                frame1=frame2

            if (df.iloc[i][2]==labels[k]):
                array.append(index)         # current index  
                array.append(df.iloc[i][1]) # frame  
                array.append(df.iloc[i][2]) # label [ankle1]
                array.append(df.iloc[i][3]) # x
                array.append(df.iloc[i][4]) # y
                array.append(df.iloc[i][5]) # z
                array.append(df.iloc[i][6]) # point index
                array.append(df.iloc[i][1]*(1/fps)) #time
                time2 = df.iloc[i][1]*(1/fps)
                x2 = df.iloc[i][3]
                y2 = df.iloc[i][4]
                z2 = df.iloc[i][5]

                # Velocity
                if (index==0):
                    time1=time2
                    x1=x2
                    y1=y2
                    z1=z2
                    
                else:
                    array.append((x2-x1)/(time2-time1)) # velocity_x
                    array.append((y2-y1)/(time2-time1)) # velocity_y
                    array.append((z2-z1)/(time2-time1)) # velocity_z
                    time1=time2

                #print(array)
                index = index+1

                #writes array to new csv file
                with open(r'{0}'.format(new_file_path), 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(array)

            
            else: 
                continue
                #do nothing
    
if __name__ == "__main__":
    main()


