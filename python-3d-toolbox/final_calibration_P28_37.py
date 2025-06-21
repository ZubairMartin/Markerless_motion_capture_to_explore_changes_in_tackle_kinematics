import cameratoolbox as ctb
import time

import os 


  
proj = [

"P28_baseline_1",
"P28_baseline_2",
"P29_baseline_1",
"P29_baseline_2",
"P30_baseline_1",
"P30_baseline_2",
"P31_baseline_1",
"P31_baseline_2",
"P32_baseline_1",
"P32_baseline_2",
"P33_baseline_1",
"P33_baseline_2",
"P34_baseline_1",
"P34_baseline_2",
"P35_baseline_1",
"P35_baseline_2",
"P36_baseline_1",
"P36_baseline_2",
"P37_baseline_1",
"P37_baseline_2"

]

orientation = [

'upright',
'sideways',
'upright',
'sideways',
'upright',
'upright',
'sideways',
'sideways',
'sideways',
'sideways',
'sideways',
'upright',
'upright',
'upright',
'sideways',
'sideways',
'sideways',
'sideways',
'sideways',
'sideways'
]

for i in range (len(proj)):
	project_dir = '/home/uct/Analyse_videos/CameraCalibration/Projects/final_calibration_videos/'+proj[i]
	time.sleep(10)
	if orientation[i]=='sideways':
		ctb.find_corners(project_dir,(8,6),0.04)
	else:
		ctb.find_corners(project_dir,(6,8),0.04)
	time.sleep(10)
	ctb.calibrate_extrinsics(project_dir,output_video_filepath='/home/uct/Analyse_videos/CameraCalibration/final_videos_to_calibrate/'+proj[i]+'.MP4')
	time.sleep(10)
