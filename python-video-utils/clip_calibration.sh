#!/usr/bin/bash
source ~/anaconda3/etc/profile.d/conda.sh
conda activate video_tools

python clip_video.py "/home/uct/Analyse_videos/final_analysis_set/P30_P37_calibration/GP1_P30_baseline_2_calibration.MP4" "/home/uct/Analyse_videos/final_analysis_set/calibration_trim/GP1_P30_baseline_2_calibration_updated.MP4" 0 -1 10
python clip_video.py "/home/uct/Analyse_videos/final_analysis_set/P30_P37_calibration/GP4_P30_baseline_2_calibration.MP4" "/home/uct/Analyse_videos/final_analysis_set/calibration_trim/GP4_P30_baseline_2_calibration_updated.MP4" 0 -1 10
python clip_video.py "/home/uct/Analyse_videos/final_analysis_set/P30_P37_calibration/GP3_P30_baseline_2_calibration.MP4" "/home/uct/Analyse_videos/final_analysis_set/calibration_trim/GP3_P30_baseline_2_calibration_updated.MP4" 0 -1 10
python clip_video.py "/home/uct/Analyse_videos/final_analysis_set/P2_P29_calibration/GP1_P28_baseline_1_calibration.MP4" "/home/uct/Analyse_videos/final_analysis_set/calibration_trim/GP1_P28_baseline_1_calibration_updated.MP4" 0 -1 13
python clip_video.py "/home/uct/Analyse_videos/final_analysis_set/P2_P29_calibration/GP3_P28_baseline_1_calibration.MP4" "/home/uct/Analyse_videos/final_analysis_set/calibration_trim/GP3_P28_baseline_1_calibration_updated.MP4" 0 -1 13
python clip_video.py "/home/uct/Analyse_videos/final_analysis_set/P2_P29_calibration/GP4_P28_baseline_1_calibration.MP4" "/home/uct/Analyse_videos/final_analysis_set/calibration_trim/GP4_P28_baseline_1_calibration_updated.MP4" 0 -1 13
