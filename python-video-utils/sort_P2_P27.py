import os 

valid = os.listdir('/home/uct/Analyse_videos/Session8_Set2_tackle1-UCT-2019-11-27/all_final_vids/P2_P27_old/valid_old')
invalid = os.listdir('/home/uct/Analyse_videos/Session8_Set2_tackle1-UCT-2019-11-27/all_final_vids/P2_P27_old/invalid_old')

va = []
ia = []

for v in valid:
	va.append('/home/uct/Analyse_videos/Session8_Set2_tackle1-UCT-2019-11-27/all_final_vids/P2_P27_old/valid_old/'+v+' /home/uct/Analyse_videos/Session8_Set2_tackle1-UCT-2019-11-27/all_final_vids/P2_P27/valid/'+v+' 0 -1 2')
	
for i in invalid:
	ia.append('/home/uct/Analyse_videos/Session8_Set2_tackle1-UCT-2019-11-27/all_final_vids/P2_P27_old/invalid_old/'+i+' /home/uct/Analyse_videos/Session8_Set2_tackle1-UCT-2019-11-27/all_final_vids/P2_P27/invalid/'+i+' 0 -1 2')
	
arr = va + ia

for j in arr:
	print('python clip_video.py '+j)
	print()
