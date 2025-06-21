'''
Must be in python-3d-toolbox file in order to run code
world frame to camera frame
'''
def main(original_file_path,new_file_path_folder,project_dir):

    import cameratoolbox as ctb
    import cv2
    import numpy as np
    import pandas as pd
    import csv
    import scipy

    #############################################################################    
    labels = ['ankle1','knee1','hip1','wrist1','shoulder1','elbow1','ankle2','knee2','hip2','wrist2','shoulder2','elbow2','chin','forehead','top','bottom','middle','upper quartile','lower quartile']
    #############################################################################

    cameras = ctb.load_cameras(project_dir)
    cam_middle = cameras[1] # select camera

    #Create 3x3 matrix
    rotation_matrix = cv2.Rodrigues(cam_middle.R)[0] #rot_mat, _ = cv2.Rodrigues(cam0.R)

    translation_vector = cam_middle.T
    #rotation_matrix_invert = np.linalg.inv(rotation_matrix)

    print('rotation_matrix: ',rotation_matrix)
    print('translation_vector: ',translation_vector)

    for k in range (len(labels)):

        # Path of csv file to be filtered (place unfiltered csv file)
        df = pd.read_csv(original_file_path+labels[k]+'_velocity.csv')

        new_file_path = new_file_path_folder+labels[k]+'_new_frame.csv'

        # Create a new csv file
        with open(new_file_path, 'wb') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        # Include headings of the new csv file
        headings =['index', 'frame', 'label' ,'x_new', 'y_new', 'z_new', 'point_index','time(sec)','x_velocity_new','y_velocity_new','z_velocity_new']
        with open(r'{0}'.format(new_file_path), 'a') as f:
            writer = csv.writer(f)
            writer.writerow(headings) 

        array = []
        index=0
        for i in range(len(df['point_index'])):

            if (df.iloc[i][2]==labels[k]):
                array.append(index)         # current index  
                array.append(df.iloc[i][1]) # frame  
                array.append(df.iloc[i][2]) # label [ankle1]

                # world frame to camera frame
                x = df.iloc[i][3]
                y = df.iloc[i][4]
                z = df.iloc[i][5]
                world_frame_coordinates_vector = [[x],[y],[z]] #[[-0.5],[5],[0.5]] 
                #print('world_frame_coordinates_vector: ',world_frame_coordinates_vector)

                RX = [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*world_frame_coordinates_vector) for X_row in rotation_matrix]]
                for x in range(3):
                    Xc = RX[0][x]+translation_vector[x][0]
                    array.append(Xc)
                    #print("Xc: ",Xc)

                array.append(df.iloc[i][6]) # point index
                array.append(df.iloc[i][7]) # time
                
                with open(r'{0}'.format(new_file_path), 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(array)
                
                index=index+1
                del array
                array = []
            
            else:
                del array
                array = []
                continue      

if __name__ == "__main__":
    main()