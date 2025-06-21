#!/usr/bin/bash
source ~/anaconda3/etc/profile.d/conda.sh
conda activate video_tools

python clip_video.py ~/Desktop/RugbyProject/Session13_original/GP1/GH012337.MP4 ~/Desktop/RugbyProject/TrimmedVideos/Session13/set2/GP1_calibration.MP4 6491 9568
python clip_video.py ~/Desktop/RugbyProject/Session13_original/GP3/GH010073.MP4 ~/Desktop/RugbyProject/TrimmedVideos/Session13/set2/GP3_calibration.MP4 5063 8140
python clip_video.py ~/Desktop/RugbyProject/Session13_original/GP4/GH010052.MP4 ~/Desktop/RugbyProject/TrimmedVideos/Session13/set2/GP4_calibration.MP4 3706 6783