'''
Create 3D reconstruction video and csv file
Need to run code in 3d-toolbox
'''

def main(h5_dir,project_dir,folder,tackle):

    import cameratoolbox as ctb
    import utils

    dlc_filepaths = h5_dir # all camera h5 file paths of video (directories)
    points_2d_df = utils.create_dlc_points_2d_file(dlc_filepaths)
    points_2d_df = points_2d_df[points_2d_df['likelihood']>0.9]
    ctb.points_2d_df_to_3d(project_dir, points_2d_df, output_3d_point_df_filepath=folder+'3D_reconstruction.csv', output_video_filepath=folder+'3D_reconstruction_'+tackle+'.mp4')

if __name__ == "__main__":
    main()