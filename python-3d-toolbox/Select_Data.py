# Select plots of body parts of interest and append them to a new csv file [xyz vs frame]

def main(original_file_path,new_file_path_folder):

    import sys
    import pandas as pd
    import numpy as np
    import csv
    import matplotlib.pyplot as plt

    #############################################################################    
    labels = ['ankle1','knee1','hip1','wrist1','shoulder1','elbow1','ankle2','knee2','hip2','wrist2','shoulder2','elbow2','chin','forehead','top','bottom','middle','upper quartile','lower quartile']
    #############################################################################

    for k in range(len(labels)): # For each body part

        new_file_path = new_file_path_folder+labels[k]+'.csv'
        #print(new_file_path)

        # Read original CSV
        df = pd.read_csv(original_file_path)
        #print(df.head(10))

        # Create a new csv file
        with open(new_file_path, 'wb') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        # Include headings of the new csv file
        headings =['index', 'frame', 'label' ,'x', 'y', 'z', 'point_index','time(sec)']
        with open(r'{0}'.format(new_file_path), 'a') as f:
            writer = csv.writer(f)
            writer.writerow(headings) 

        # Array that is used to append to csv file
        array = []

        point_index=len(df['point_index'])
        index=0
        frame1=0
        frame2=0
        fps = 119 # indicate frames per second of original video to obtain seconds

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
                array.append(df.iloc[i][1]*(1/fps))
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


####################################################################################################################
