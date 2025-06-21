#!/usr/bin/bash
source ~/anaconda3/etc/profile.d/conda.sh
conda activate video_tools

python clip_video.py "/media/uct/Bubbles/MSc Testing/Go Pros/P2/Go Pro 1/P2_baseline_2.MP4" "/home/uct/P2_baseline_2_updated.MP4" 0 -1 2

python clip_video.py "/media/uct/Bubbles/MSc Testing/Go Pros/P26/Go Pro 1/P26_baseline_1.MP4" "/home/uct/P26_baseline_1_updated.MP4" 0 -1 2

python clip_video.py "/media/uct/Bubbles/MSc Testing/Go Pros/P26/Go Pro 1/P26_baseline_2.MP4" "/home/uct/P26_baseline_2_updated.MP4" 0 -1 2

python clip_video.py "/media/uct/Bubbles/MSc Testing/Go Pros/P27/Go Pro 1/P27_baseline_1.MP4" "/home/uct/P27_baseline_1_updated.MP4" 0 -1 2

python clip_video.py "/media/uct/Bubbles/MSc Testing/Go Pros/P27/Go Pro 1/P27_baseline_2.MP4" "/home/uct/P27_baseline_2_updated.MP4" 0 -1 2

