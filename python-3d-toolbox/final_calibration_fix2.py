import cameratoolbox as ctb
import time

import os 

#"P2_baseline_1",
#"P2_baseline_2",
#'upright',
#'sideways',


proj = [

"P26_baseline_1"

]



orientation = [
'sideways'
]

for i in range (len(proj)):
	project_dir = '/home/uct/Analyse_videos/CameraCalibration_fix/Projects/'+proj[i]
	time.sleep(10)
	if orientation[i]=='sideways':
		ctb.find_corners(project_dir,(8,6),0.04)
	else:
		ctb.find_corners(project_dir,(6,8),0.04)
	time.sleep(10)
	ctb.calibrate_extrinsics(project_dir,output_video_filepath='/home/uct/Analyse_videos/CameraCalibration_fix/final_videos_to_calibrate/'+proj[i]+'.MP4')
	time.sleep(10)
