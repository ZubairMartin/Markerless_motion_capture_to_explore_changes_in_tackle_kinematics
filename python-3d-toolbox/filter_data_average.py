# done using liams csv file
# need to filter each body part

def main(original_file_path,new_file_path_folder):

    import pandas as pd
    import numpy as np
    import csv
    import matplotlib.pyplot as plt
    import scipy
    from scipy import signal

    #############################################################################    
    labels = ['ankle1','knee1','hip1','wrist1','shoulder1','elbow1','ankle2','knee2','hip2','wrist2','shoulder2','elbow2','chin','forehead','top','bottom','middle','upper quartile','lower quartile']
    #############################################################################
    for k in range (len(labels)): 

        point_index = []
        index = []
        label = []
        frames = []
        x_unfiltered = []
        y_unfiltered = []
        z_unfiltered = []
        time=[]

        # Path of csv file to be filtered (place unfiltered csv file)
        df = pd.read_csv(original_file_path+labels[k]+'.csv')

        new_file_path = new_file_path_folder+labels[k]+'_filtered.csv'

        # Create a new csv file
        with open(new_file_path, 'wb') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        # Include headings of the new csv file
        headings =['index', 'frame', 'label' ,'x', 'y', 'z', 'point_index','time(sec)']
        with open(r'{0}'.format(new_file_path), 'a') as f:
            writer = csv.writer(f)
            writer.writerow(headings) 

        index_len=len(df['index'])
        print('{0} = index_len = {1}'.format(labels[k],index_len))

        for i in range(index_len):
            index.append(df.iloc[i][0])
            frames.append(df.iloc[i][1])
            label.append (df.iloc[i][2])
            x_unfiltered.append(df.iloc[i][3])
            y_unfiltered.append(df.iloc[i][4])
            z_unfiltered.append(df.iloc[i][5])
            point_index.append(df.iloc[i][6])
            time.append(df.loc[i][7])

        x_filtered = scipy.signal.medfilt(volume = x_unfiltered)
        y_filtered = scipy.signal.medfilt(volume = y_unfiltered)
        z_filtered = scipy.signal.medfilt(volume = z_unfiltered)

        array = []

        for i in range (len(index)):
            array.append(i)
            array.append(frames[i])
            array.append(label[i])
            array.append(x_filtered[i])
            array.append(y_filtered[i])
            array.append(z_filtered[i])
            array.append(point_index[i])
            array.append(time[i])

            # Directory of new csv file (filtered)
            with open(r'{0}'.format(new_file_path), 'a') as f:
                writer = csv.writer(f)
                writer.writerow(array)
            
            # clear array for next row
            del array
            array = []

if __name__ == "__main__":
    main()