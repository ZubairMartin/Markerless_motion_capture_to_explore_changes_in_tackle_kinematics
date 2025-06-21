'''
##################################################################################################################
directory = '/home/uct/Desktop/RugbyProject/Spreadsheet/' # Directory of folder to place files
folder = '/home/uct/Desktop/RugbyProject/Spreadsheet/'# Directory of folder with all the data
project_dir = '/home/uct/Desktop/RugbyProject/CameraCalibration/Projects/Session12_Set2_c' # of camera calibration
actual_to_truncate_frame = [92,182] # Actual frame in which the tackle starts and ends
mass = 87.7 # mass of tackler
temp = 'Tackle6_session12_set2'
spreadsheetname = 'spreadsheet_'+temp
a = 'GP1_{0}DLC_resnet101_Session8_Set2_tackle1Nov27shuffle1_200000.h5'.format(temp)
b = 'GP3_{0}DLC_resnet101_Session8_Set2_tackle1Nov27shuffle1_200000.h5'.format(temp)
c = 'GP4_{0}DLC_resnet101_Session8_Set2_tackle1Nov27shuffle1_200000.h5'.format(temp)
h5_dir = [directory+'{0}'.format(a),directory+'{0}'.format(b),directory+'{0}'.format(c)] # place h5 directories in the folder
##################################################################################################################
'''
#temp = name of tackle
#mass = tackler mass
#T_start = frame at which tackle starts
#T_end = frame at whoch tackle ends (bag touch ground)
#folder = Directory of folder with all the data
#directory = Directory of folder to place files
#project_dir = directrory of camera calibration project
#GP_used = gopros that were used [134] [13] [14] [34]


def main(temp,mass,T_start,T_end,folder,directory,project_dir,GP_used,player_number,tackle_numb,session):

    #########################################################################################
    spreadsheetname = 'spreadsheet_'+temp
    a = 'GP1_{0}DLC_resnet101_Session8_Set2_tackle1Nov27shuffle1_500000.h5'.format(temp)
    b = 'GP3_{0}DLC_resnet101_Session8_Set2_tackle1Nov27shuffle1_500000.h5'.format(temp)
    c = 'GP4_{0}DLC_resnet101_Session8_Set2_tackle1Nov27shuffle1_500000.h5'.format(temp)

    if GP_used==134:
        h5_dir = [directory+'{0}'.format(a),directory+'{0}'.format(b),directory+'{0}'.format(c)] # place h5 directories in the folder
        print(h5_dir)
    elif GP_used==13:
        h5_dir = [directory+'{0}'.format(a),directory+'{0}'.format(b)] # place h5 directories in the folder
        print(h5_dir)
    elif GP_used==14:
        h5_dir = [directory+'{0}'.format(a),directory+'{0}'.format(c)] # place h5 directories in the folder
        print(h5_dir)
    elif GP_used==34:
        h5_dir = [directory+'{0}'.format(b),directory+'{0}'.format(c)] # place h5 directories in the folder
        print(h5_dir)
    else:
        print('error no GP are indicated')
    actual_to_truncate_frame = [T_start,T_end] # Actual frame in which the tackle starts and ends
    #########################################################################################


    # Step 1: Median Filter

    print('Running median filter ...')

    import Median_Filter_outliers
    
    for i in range(len(h5_dir)):
        Median_Filter_outliers.main(h5_dir[i])

    # Step 2: 3D Reconstruction plotting points with 0.9 liklihood

    print('Median filter completed')
    print('')
    print('Running 3D reconstruction ...')
    
    import reconstruction
    reconstruction.main(h5_dir,project_dir,folder,temp)

    def delay():
        for i in range(10):
            for j in range (10):
                pass

    delay()

    # Step 3: Select_Data
    print('3D reconstruction completed')
    print('')
    print('Selecting and seperating data...')
    import Select_Data
    Select_Data.main(folder+'3D_reconstruction.csv',folder)

    # Step 4: Average Filter
    print('Data selection completed')
    print('')
    print('Running filter to average points ...')
    import filter_data_average
    filter_data_average.main(folder,folder)

    # Step 5: Implement velocity
    print('Data filter completed')
    print('')
    print('Finding velocity ...')
    import velocity
    velocity.main(folder,folder)

    # Step 6: Shift points to middle camera's frame
    print('Velocity per instance completed')
    print('')
    print('Rotating points from world frame to middle camera frame (GP3) ...')
    import worldtocam_frame
    worldtocam_frame.main(folder,folder,project_dir)
    #
    # Step 7: Generate splined data
    print('Rotation completed')
    print('')
    print('Generating spline through data points ...')
    import cubic_spline_new_file_interpolated
    cubic_spline_new_file_interpolated.main(folder,folder)

    # Not used as actual frames are used
    
    # Step 8: Find the end and start of a tackle
    print('Spline completed')
    print('')
    print('Estimating where start and end frame of tackle ...')
    import EndandStart
    Est_frame = EndandStart.main(folder,actual_to_truncate_frame[0],actual_to_truncate_frame[1])
    
    
    # Step 9: Create excel spreadsheet
    print('Estimate completed')
    print('')
    print('Generating spreadsheet...')
    import SpreadSheet
    SpreadSheet.main(location=folder,folder=folder,name=spreadsheetname, bag_mass = 42.1,tackler_mass=mass,Start_frame_est=Est_frame[0],End_frame_est=Est_frame[1],Start_frame=actual_to_truncate_frame[0],End_frame=actual_to_truncate_frame[1],temp=temp,player_number=player_number,tackle_numb = tackle_numb, session = session)
    #SpreadSheet.main(location=folder,folder=folder,name=spreadsheetname, bag_mass = 40,tackler_mass=mass,Start_frame_est=0,End_frame_est=0,Start_frame=actual_to_truncate_frame[0],End_frame=actual_to_truncate_frame[1],temp=temp,player_number=player_number)
    print('spreadsheet completed')

    # Will delete all unneeded files after spreasheet is generated
    import os 
  
    for file in os.listdir(directory): 
        if file.endswith('.csv'):
            os.remove(directory+file)
            print('The file {0} was removed'.format(file))

# temp = "Tackle1_Session13_Set1"
# mass = 83.55
# T_start = 184
# T_end = 170
# folder = "/home/uct/Analyse_videos/sort/valid_output/labelled_videos/"
# directory = "/home/uct/Analyse_videos/sort/valid_output/labelled_videos/"
# project_dir = "/home/uct/Analyse_videos/sort/valid_camera_calib/Session13_set1"
# GP_used = 134
# player_number="P15_B1"

# main(temp,mass,T_start,T_end,folder,directory,project_dir,GP_used,player_number)

if __name__ == "__main__":
    main()
    
