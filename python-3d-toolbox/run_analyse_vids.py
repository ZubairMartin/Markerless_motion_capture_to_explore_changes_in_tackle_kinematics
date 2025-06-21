import deeplabcut as dlc

path = '/home/uct/Desktop/RugbyProject/Analyse_videos/Session8_Set2_tackle1-UCT-2019-11-27/videos/'
config = '/home/uct/Desktop/RugbyProject/Analyse_videos/Session8_Set2_tackle1-UCT-2019-11-27/config.yaml'

array = []
'''
videos134 = [

    'GP{0}_Tackle2_session9_set1.MP4'.format(i),
    'GP{0}_Tackle2_session12_set1.MP4'.format(i),
    'GP{0}_Tackle2_session12_set2.MP4'.format(i),
    'GP{0}_Tackle3_session12_set1.MP4'.format(i),
    'GP{0}_Tackle3_session13_set1.MP4'.format(i),
    'GP{0}_Tackle4_session8_set2.MP4'.format(i),
    'GP{0}_Tackle4_session8_set3.MP4'.format(i),
    'GP{0}_Tackle4_session9_set1.MP4'.format(i),
    'GP{0}_Tackle4_session13_set1.MP4'.format(i),
    'GP{0}_Tackle5_session7_set1.MP4'.format(i),
    'GP{0}_Tackle5_session8_set3.MP4'.format(i),
    'GP{0}_Tackle5_session9_set2.MP4'.format(i),
    'GP{0}_Tackle6_session7_set1.MP4'.format(i),
    'GP{0}_Tackle6_session8_set2.MP4'.format(i),
    'GP{0}_Tackle6_session9_set2.MP4'.format(i),
    'GP{0}_Tackle6_session12_set2.MP4'.format(i)
]

videos34 = [

    'GP{0}_Tackle2_session2_set11.MP4'.format(i),
    'GP{0}_Tackle4_session2_set11.MP4'.format(i),
    'GP{0}_Tackle5_session2_set3.MP4'.format(i),
    'GP{0}_Tackle3_session2_set3.MP4'.format(i),
    'GP{0}_Tackle4_session2_set3.MP4'.format(i)
]
'''
for i in range(1,2):

    array.append('GP{0}_Tackle2_session9_set1.MP4'.format(i))
    array.append('GP{0}_Tackle2_session12_set1.MP4'.format(i))
    array.append('GP{0}_Tackle2_session12_set2.MP4'.format(i))
    array.append('GP{0}_Tackle3_session12_set1.MP4'.format(i))
    array.append('GP{0}_Tackle3_session13_set1.MP4'.format(i))
    array.append('GP{0}_Tackle4_session8_set2.MP4'.format(i))
    array.append('GP{0}_Tackle4_session8_set3.MP4'.format(i))
    array.append('GP{0}_Tackle4_session9_set1.MP4'.format(i))
    array.append('GP{0}_Tackle4_session13_set1.MP4'.format(i))
    array.append('GP{0}_Tackle5_session7_set1.MP4'.format(i))
    array.append('GP{0}_Tackle5_session8_set3.MP4'.format(i))
    array.append('GP{0}_Tackle5_session9_set2.MP4'.format(i))
    array.append('GP{0}_Tackle6_session7_set1.MP4'.format(i))
    array.append('GP{0}_Tackle6_session8_set2.MP4'.format(i))
    array.append('GP{0}_Tackle6_session9_set2.MP4'.format(i))
    array.append('GP{0}_Tackle6_session12_set2.MP4'.format(i))

for ik in range(3,5):

    array.append('GP{0}_Tackle2_session9_set1.MP4'.format(ik))
    array.append('GP{0}_Tackle2_session12_set1.MP4'.format(ik))
    array.append('GP{0}_Tackle2_session12_set2.MP4'.format(ik))
    array.append('GP{0}_Tackle3_session12_set1.MP4'.format(ik))
    array.append('GP{0}_Tackle3_session13_set1.MP4'.format(ik))
    array.append('GP{0}_Tackle4_session8_set2.MP4'.format(ik))
    array.append('GP{0}_Tackle4_session8_set3.MP4'.format(ik))
    array.append('GP{0}_Tackle4_session9_set1.MP4'.format(ik))
    array.append('GP{0}_Tackle4_session13_set1.MP4'.format(ik))
    array.append('GP{0}_Tackle5_session7_set1.MP4'.format(ik))
    array.append('GP{0}_Tackle5_session8_set3.MP4'.format(ik))
    array.append('GP{0}_Tackle5_session9_set2.MP4'.format(ik))
    array.append('GP{0}_Tackle6_session7_set1.MP4'.format(ik))
    array.append('GP{0}_Tackle6_session8_set2.MP4'.format(ik))
    array.append('GP{0}_Tackle6_session9_set2.MP4'.format(ik))
    array.append('GP{0}_Tackle6_session12_set2.MP4'.format(ik))

    array.append('GP{0}_Tackle2_session2_set11.MP4'.format(ik))
    array.append('GP{0}_Tackle4_session2_set11.MP4'.format(ik))
    array.append('GP{0}_Tackle5_session2_set3.MP4'.format(ik))
    array.append('GP{0}_Tackle3_session2_set3.MP4'.format(ik))
    array.append('GP{0}_Tackle4_session2_set3.MP4'.format(ik))

for j in range (len(array)):
    
    dlc.analyze_videos(config,[path+array[j]],save_as_csv=True)
    dlc.create_labeled_videos(config,[path+'new_'+array[j]],draw_skeleton=True)