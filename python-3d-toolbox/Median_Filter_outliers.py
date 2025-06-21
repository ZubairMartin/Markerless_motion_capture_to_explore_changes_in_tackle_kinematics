# Median Filter using GP1 Tackle 1
'''
replace h5 file of the video being filtered
'''
def main(h5_dir):

  import pandas as pd
  import numpy as np
  import statistics

  #Print statements are commented out cause they made everything slooooow 

  #Read hdf file
  #h5_path = '/content/drive/My Drive/Cheetah/Dusty/JamesFlick1CAM7DeepCut_resnet50_CheetahApr2shuffle1_1030000.h5'
  h5_path = h5_dir
  df = pd.read_hdf(h5_path)
  #print(df.keys())
 
  #Initialise array of bodyparts, lure should be removed in future

  parts = np.array(['ankle1', 'knee1', 'hip1', 'hip2', 'knee2', 'ankle2', 'wrist1', 'elbow1', 'shoulder1',
  'shoulder2', 'elbow2', 'wrist2', 'chin', 'forehead', 'top', 'upper quartile','middle','lower quartile','bottom'])

  '''
  parts = np.array(['ankle1', 'knee1', 'hip1', 'hip2', 'knee2', 'ankle2', 'wrist1', 'elbow1', 'shoulder1',
  'shoulder2', 'elbow2', 'wrist2', 'chin', 'forehead'])
  '''
  #Loop for number of frames analyzed
  # for index in range(len(df[('DeepCut_resnet50_CheetahApr2shuffle1_1030000',parts[0],'x')])):
  for index in range(len(df[('DLC_resnet101_Session8_Set2_tackle1Nov27shuffle1_500000',parts[0],'x')])):
    x_list = []
    y_list = []
    for i in range(len(parts)):
      #print(parts[i], 'x-value:', df[('DeepCut_resnet50_CheetahApr2shuffle1_1030000',parts[i],'x')][index])
      #x_list.append(df[('DeepCut_resnet50_CheetahApr2shuffle1_1030000',parts[i],'x')][index])
      x_list.append(df[('DLC_resnet101_Session8_Set2_tackle1Nov27shuffle1_500000',parts[i],'x')][index])


      #print(parts[i], 'y-value:', df[('DeepCut_resnet50_CheetahApr2shuffle1_1030000',parts[i],'y')][index])
      #y_list.append(df[('DeepCut_resnet50_CheetahApr2shuffle1_1030000',parts[i],'y')][index])
      y_list.append(df[('DLC_resnet101_Session8_Set2_tackle1Nov27shuffle1_500000',parts[i],'y')][index])

    #Find the median for x and y, modelling the cheetah as a rectangle
    x_median = statistics.median(x_list)
    y_median = statistics.median(y_list)
    #print('X median: ', x_median, 'Y median: ',y_median)

    #Set the limits outside of which a point is considered an outlier
    x_bound = 500
    y_bound = 500
    
    #Change the likelihood of outliers to 0
    for j in range(len(parts)):
      if np.absolute(x_list[j]-x_median)>x_bound or np.absolute(y_list[j]-y_median)>y_bound:
        #print(parts[j], x_list[j], y_list[j], ' is an outlier!')
        
        #Edit the key with the correct snapshot
        df[('DLC_resnet101_Session8_Set2_tackle1Nov27shuffle1_500000',parts[j],'likelihood')][index] = 0
    
  #df1 = pd.DataFrame.from_dict(df,orient='columns')
  #print(df)

  #Write to hdf
  df.to_hdf(h5_path,key='df_with_missing',mode='w',format='table')  

if __name__ == "__main__":
    main()
