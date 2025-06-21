import cameratoolbox as ctb
import time

import os 


  
proj = []

for file in os.listdir('/home/uct/Desktop/RugbyProject/CameraCalibration/VideosToCalibrate/VTC/'): 
    proj.append(file)
    print(file)

for i in range (len(proj)):
    project_dir = '/home/uct/Desktop/RugbyProject/CameraCalibration/Projects/'+proj[i]
    ctb.find_corners(project_dir,(8,6),0.04)
    time.sleep(10)
    ctb.calibrate_extrinsics(project_dir,output_video_filepath='/home/uct/Desktop/RugbyProject/CameraCalibration/VideosToCalibrate/'+proj[i]+'.mp4')
    time.sleep(10)
