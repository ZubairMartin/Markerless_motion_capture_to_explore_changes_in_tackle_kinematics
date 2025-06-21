#!/usr/bin/bash
source ~/anaconda3/etc/profile.d/conda.sh
conda activate video_tools

python clip_video.py calibration/GP4_calibration_updated.MP4 calibration/1.MP4 8 20
python clip_video.py calibration/GP4_calibration_updated.MP4 calibration/2.MP4 36 70
python clip_video.py calibration/GP4_calibration_updated.MP4 calibration/3.MP4 89 105
python clip_video.py calibration/GP4_calibration_updated.MP4 calibration/4.MP4 116 172
python clip_video.py calibration/GP4_calibration_updated.MP4 calibration/5.MP4 178 182
python clip_video.py calibration/GP4_calibration_updated.MP4 calibration/6.MP4 191 195
python clip_video.py calibration/GP4_calibration_updated.MP4 calibration/7.MP4 208 220
python clip_video.py calibration/GP4_calibration_updated.MP4 calibration/8.MP4 232 241
python clip_video.py calibration/GP4_calibration_updated.MP4 calibration/9.MP4 257 267
python clip_video.py calibration/GP4_calibration_updated.MP4 calibration/10.MP4 303 334

