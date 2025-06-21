# Implement cubic spline interpolation
# Plots velocity and acceleration of given position

def main(original_file_path,new_file_path_folder):

    from scipy.interpolate import CubicSpline
    import matplotlib.pyplot as plt
    import numpy as np
    #import deeplabcut as dlc
    import pandas as pd
    import csv
    import matplotlib.pyplot as plt
    from scipy import interpolate
    from scipy import signal

    ############################################################################# 
    labels = ['ankle1','knee1','hip1','wrist1','shoulder1','elbow1','ankle2','knee2','hip2','wrist2','shoulder2','elbow2','chin','forehead','top','bottom','middle','upper quartile','lower quartile']
    ############################################################################# 

    for zp in range (len(labels)):

        df = pd.read_csv(original_file_path+labels[zp]+'_new_frame.csv')

        new_file_path = new_file_path_folder+labels[zp]+'_splined.csv'

        # Create a new csv file
        with open(new_file_path, 'wb') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        # Include headings of the new csv file
        headings =['index', 'frame', 'label' ,'x_pos', 'y_pos', 'z_pos', 'point_index','time(sec)','x_vel','y_vel','z_vel','x_acc','y_acc','z_acc']
        with open(r'{0}'.format(new_file_path), 'a') as f:
            writer = csv.writer(f)
            writer.writerow(headings) 
        
        # create an arrays to be fed into CubicSpline function 
        array_x = []
        array_y = []
        array_z = []
        time = []
        frame = []

        index_len=len(df['index'])
        index=0

        # interpolate position, can change indices for velocity interpolation
        for i in range(index_len):
            array_x.append(df.iloc[i][3])
            array_y.append(df.iloc[i][4])
            array_z.append(df.iloc[i][5])
            time.append(df.iloc[i][7])
            frame.append(df.iloc[i][1])

        t_temp = np.array(time)
        f = np.array(frame)
        x = np.array(array_x)
        y = np.array(array_y)
        z = np.array(array_z)

        if (len(x)<12): # too few points to interpolate
            print(labels[zp]+' array is too short, require more points to interpolate')
            continue

        b, a = signal.butter(3, 0.05)

        if (len(x)>12 and len(y)>12 and len(z)>12):
            cx = signal.filtfilt(b, a, x)
            cy = signal.filtfilt(b, a, y)
            cz = signal.filtfilt(b, a, z)
        else: continue

        xx = CubicSpline(t_temp, cx)
        yy = CubicSpline(t_temp, cy)
        zz = CubicSpline(t_temp, cz)

    
        #print('t_temp[0]: ',t_temp[0])
        #print('t_temp[-1]',t_temp[-1])
        #print('index_len: ',index_len)

        t = np.linspace(t_temp[0],t_temp[-1],(frame[-1]-frame[0])+1)
        #print('t_len: ',len(t))
        

        x_interpolated = xx(t)
        y_interpolated = yy(t)
        z_interpolated = zz(t)

        '''
        Derivative of spline (velocity)
        '''

        vel_x =[]
        vel_y =[]
        vel_z =[]

        for i in range (len(xx(t))):
            if (i==0):
                continue
            else:
                vel_x.append((xx(t)[i]-xx(t)[i-1])/(t[i]-t[i-1]))
                vel_y.append((yy(t)[i]-yy(t)[i-1])/(t[i]-t[i-1]))
                vel_z.append((zz(t)[i]-zz(t)[i-1])/(t[i]-t[i-1]))

        #Derivative of derivative of spline (acceleration)
        acc_x =[]
        acc_y =[]
        acc_z =[]

        for j in range (len(xx(t))-1):
            if (j==0):
                continue
            else:
                acc_x.append((vel_x[j]-vel_x[j-1])/(t[j]-t[j-1]))
                acc_y.append((vel_y[j]-vel_y[j-1])/(t[j]-t[j-1]))
                acc_z.append((vel_z[j]-vel_z[j-1])/(t[j]-t[j-1]))

        array = []
        start_frame = df.iloc[0][1]
        for y in range (len(x_interpolated)):
            #print(labels[zp],': ',y)
            array.append(y)         # current index 
            array.append(start_frame+y) # frame 
            array.append(labels[zp]) # label 
            array.append(x_interpolated[y]) # x
            array.append(y_interpolated[y]) # y
            array.append(z_interpolated[y]) # z
            array.append('ToBe_solved') # point index
            array.append(t[y])
            
            if (y > 0):
                array.append(vel_x[y-1])
                array.append(vel_y[y-1])
                array.append(vel_z[y-1])
            if (y>1):
                array.append(acc_x[y-2])
                array.append(acc_y[y-2])
                array.append(acc_z[y-2])
            
            #writes array to new csv file
            with open(r'{0}'.format(new_file_path), 'a') as f:
                writer = csv.writer(f)
                writer.writerow(array)
                #print(array)
                index = index+1

            del array
            array = []




        '''
        def turningpoints(x):
        N=[]
        for i in range(1, len(x)-1):
            if ((x[i-1] < x[i] and x[i+1] < x[i]) or (x[i-1] > x[i] and x[i+1] > x[i])):
                N.append(t[2:][i])
        return N

        print('turningpoints: ',turningpoints(acc_x))


        plt.plot(t[2:], acc_x, label="x_acceleration")
        plt.plot(t[2:], acc_y, label="y_acceleration")
        plt.plot(t[2:], acc_z, label="z_acceleration")
        '''

if __name__ == "__main__":
    main()
