'''
Generate a excel spread sheet per tackle
'''

def main(location='~/Desktop/',folder='~/Desktop/',name='Spreadsheet', bag_mass = 42.1,tackler_mass=1,Start_frame_est=0,End_frame_est=0,Start_frame=0,End_frame=0,temp='notsure',player_number = 'P',tackle_numb = 'NA', session = 'NA'):

    import xlsxwriter
    import string
    import itertools
    #import deeplabcut as dlc
    import pandas as pd
    import numpy as np
    import csv
    import math

    ################################################################################################################################################
    #headings_to_use = ['Vid','Tackler','Session','Tackle Number','Start Frame Est','End Frame Est','Start Frame Act','End Frame Act','Contact Time','Power At Impact of bag','Bag Energy Before','Bag Energy After','Shoulder Energy Before','Shoulder Energy After','Longest Distance', 'Start Vel Bag', 'End Vel Bag','Start Vel Shoulder','End Vel Shoulder']
    # Need to fill: 'Vid','Tackler','Session','Tackle Number'
    headings_to_use = [
        'Video','Tackler','Session','Tackle Number',
        'Start Frame Est','End Frame Est','Start Frame Act','End Frame Act',
        'Mass_of_bag[kg]','Mass_of_tackler[kg]',
        'Vi_middle_bag[m/s]','Vf_middle_bag[m/s]','Vi_lower_bag[m/s]','Vf_lower_bag[m/s]',
        'Vi_shoulder1[m/s]','Vf_shoulder1[m/s]','Vi_hip1[m/s]','Vf_hip1[m/s]',
        'Relative_pos_shoudler1_middle[m]','Relative_pos_shoudler1_bottom[m]',
        'Relative_pos_shoudler1_top[m]','Relative_pos_elbow1_top[m]',
        'Relative_pos_wrist1_top[m]','Bag_Energy_x_impact_middle[J]',
        'Bag_Energy_x_impact_lower[J]','Bag_Force_x_impact_middle[N]','Bag_Force_x_impact_lower[N]',
        'Tackler_Energy_x_impact_left_hip[J]','Tackler_Force_x_impact_left_shoulder[N]',
        'Power_of_tackler_x_left_shoulder[W]','Momentum_bag_lower_before_impact[kgm/s]',
        'Momentum_left_hip_before_impact[kgm/s]','Momentum_baghip_before_impact(calculated)',
        'Velocity_after_impact_calculated', 'Velocity_after_impact_actual',
        'Distance_x_calculated[m]',   'x_distance_travelled[m]',
        'Contact_time[s]','Ai_left_shoulder']

    labels = ['ankle1','knee1','hip1','wrist1','shoulder1','elbow1','ankle2','knee2','hip2','wrist2','shoulder2','elbow2','chin','forehead','top','bottom','middle','upper quartile','lower quartile']
    fps = 119
    ################################################################################################################################################

    def excel_cols(): 
        n = 1 
        while True: 
            yield from (''.join(group) for group in itertools.product(string.ascii_uppercase, repeat=n)) 
            n += 1

    def createspreadsheet(worksheet,workbook): #Only use section to generate new excel sheet
        
        #worksheet.write(row, col, data)
        for i in range (len(headings_to_use)):
            
            #print(list(itertools.islice(excel_cols(),len(headings_to_use))))

            # Widen the first column to make the text clearer.
            worksheet.set_column('A:{0}'.format(list(itertools.islice(excel_cols(),len(headings_to_use)))[-1] ), 30) # (column to use,width of)

            # Add a bold format to use to highlight cells.
            bold = workbook.add_format({'bold': True})

            worksheet.write('{0}1'.format(list(itertools.islice(excel_cols(),i+1))[-1]), '{0}'.format(headings_to_use[i]), bold)  

        # Insert an image.
        worksheet.insert_image('B5', 'logo.png')

    # Limit array to start and end of tackle and returns indices of when takle start and end
    def truncate(df_to_use,item,start_frame,end_frame):
        var = []
        frame = []
        len_of_df = len(df_to_use['{0}'.format(item)])
        
        flag = True

        for t in range(len_of_df):
            var.append(df_to_use.iloc[t]['{0}'.format(item)])
            frame.append(df_to_use.iloc[t]['frame'])

        #print('Var: ',var)
        if start_frame in frame:
            start_index = frame.index(start_frame)
            
        if start_frame not in frame:
            start_index = frame[0]
            flag = False

        if end_frame in frame:
            end_index = frame.index(end_frame)

        if end_frame not in frame:
            end_index = frame[-1]
            flag = False

        

        '''
        a = frame.index(12) # get row number

        print(df['frame'][a]) # get value at row number
        '''

        #return start_index,end_index,var[start_index:end_index+1]
        if (flag == False):
            return var[start_index:end_index]
        else:
            return var[start_index:end_index+1]



    def kinetic_energy (mass,velocity):
        KE = 0.5*mass*(velocity*velocity)
        return KE

    def force(mass,acceleration):
        F = mass*acceleration
        return F

    # Find power before impact of bag
    def power(mass,velocity,acceleration):
        F = force(mass,acceleration)
        P = abs(F*velocity)
        return P

    def momentum(mass ,velocity):
        M = mass*velocity
        return M

    def relative_pos(angle,limb_x,limb_y,bag_x,bag_y):
        limb = [limb_x[0],limb_y[0]]
        bag = [bag_x[0],bag_y[0]]
        relative_position = np.array(limb) - np.array(bag) # In cam1 frame
                
        # Find the rotation matrix wrt the y axis - note math.trig = radians

        x_distance_between_bag_limb = relative_position[0]*math.cos(angle*(math.pi/180))-(relative_position[1]*math.sin(angle*(math.pi/180)))
        y_distance_between_bag_limb = relative_position[0]*math.sin(angle*(math.pi/180))+(relative_position[1]*math.cos(angle*(math.pi/180)))
        return y_distance_between_bag_limb

    def main2():
            
        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(location+name+'.xlsx')
        worksheet = workbook.add_worksheet()

        # Read csv files 
        df = []
        for k in range (len(labels)):
            df.append(pd.read_csv(folder+'{0}_splined.csv'.format(labels[k])))

        createspreadsheet(worksheet,workbook) # Create spreadsheet

        # All values are used in the x_direction  
        position_wrist1 = truncate(df[3],'x_pos',Start_frame,End_frame)
        position_elbow1 = truncate(df[5],'x_pos',Start_frame,End_frame)
        position_shoulder1 = truncate(df[4],'x_pos',Start_frame,End_frame)
        position_top = truncate(df[14],'x_pos',Start_frame,End_frame)
        position_middle = truncate(df[16],'x_pos',Start_frame,End_frame)
        position_bottom = truncate(df[15],'x_pos',Start_frame,End_frame)

        position_top_y = truncate(df[14],'y_pos',Start_frame,End_frame)
        position_bottom_y = truncate(df[15],'y_pos',Start_frame,End_frame)
        position_shoulder1_y = truncate(df[4],'y_pos',Start_frame,End_frame)
        position_middle_y = truncate(df[16],'y_pos',Start_frame,End_frame)
        position_elbow1_y = truncate(df[5],'y_pos',Start_frame,End_frame)
        position_wrist1_y = truncate(df[3],'y_pos',Start_frame,End_frame)


        velocity_shoulder1 = truncate(df[4],'x_vel',Start_frame,End_frame)
        print()
        print("Start_frame = ",Start_frame)
        print("End_frame = ",End_frame)
        print("velocity_shoulder1 = ",velocity_shoulder1)
        velocity_hip1 = truncate(df[2],'x_vel',Start_frame,End_frame)
        velocity_middle = truncate(df[16],'x_vel',Start_frame,End_frame)
        velocity_lower = truncate(df[18],'x_vel',Start_frame,End_frame)

        acceleration_middle = truncate(df[16],'x_acc',Start_frame,End_frame)
        acceleration_lower = truncate(df[18],'x_acc',Start_frame,End_frame)
        acceleration_shoulder1 = truncate(df[4],'x_acc',Start_frame,End_frame)

        #contact_time = truncate(df[0],'time(sec)',Start_frame,End_frame)

        #worksheet.write(row, col, data)

        # Video
        worksheet.write(1, 0, temp)

        # Tackler
        worksheet.write(1, 1, player_number)

        # Session
        # worksheet.write(1, 2, temp[temp.find('n')+1:temp.find('set')-1])
        worksheet.write(1, 2, session)

        # Tackle Number
        worksheet.write(1, 3, tackle_numb)

        # Start Frame Est
        worksheet.write(1, 4, Start_frame_est)

        # End Frame Est 
        worksheet.write(1, 5, End_frame_est)

        # Start Frame Act
        worksheet.write(1, 6, Start_frame)

        # End Frame Act
        worksheet.write(1, 7, End_frame)

        # Mass_of_bag
        worksheet.write(1, 8, bag_mass)

        # Mass_of_tackler
        worksheet.write(1, 9, tackler_mass)

        # Vi_middle_bag
        worksheet.write(1, 10, velocity_middle[0])

        # Vf_middle_bag
        worksheet.write(1, 11, velocity_middle[-1])

        # Vi_lower_bag
        worksheet.write(1, 12, velocity_lower[0])

        # Vf_lower_bag
        worksheet.write(1, 13, velocity_lower[-1])

        # Vi_shoulder1
        print(velocity_shoulder1[0])
        worksheet.write(1, 14, velocity_shoulder1[0])

        # Vf_shoulder1
        worksheet.write(1, 15, velocity_shoulder1[-1])

        # Vi_hip1
        worksheet.write(1, 16, velocity_hip1[0])

        # Vf_hip1
        worksheet.write(1, 17, velocity_hip1[-1])

        # Ai_left_shoulder
        worksheet.write(1, 38, acceleration_shoulder1[0])

        ####################################################################################################################################################
        # Find angle wrt y axis
        x_vect = position_top[0]-position_bottom[0]
        y_vect = position_top_y[0]-position_bottom_y[0]
        
        mag =  math.sqrt((x_vect*x_vect)+(y_vect*y_vect)) #magintude
        angle_wrt_yaxis = math.atan2(x_vect,y_vect)*(180/math.pi)
        angle = (180-angle_wrt_yaxis)
        ####################################################################################################################################################

        # Relative_pos_shoudler1_middle
        Relative_pos_shoudler1_middle = relative_pos(angle,position_shoulder1,position_shoulder1_y,position_middle,position_middle_y)
        worksheet.write(1, 18, Relative_pos_shoudler1_middle)

        # Relative_pos_shoudler1_bottom
        Relative_pos_shoudler1_bottom = relative_pos(angle,position_shoulder1,position_shoulder1_y,position_bottom,position_bottom_y)
        worksheet.write(1, 19, Relative_pos_shoudler1_bottom)

        # Relative_pos_shoudler1_top
        Relative_pos_shoudler1_top = relative_pos(angle,position_shoulder1,position_shoulder1_y,position_top,position_top_y)
        worksheet.write(1, 20, Relative_pos_shoudler1_top)

        # Relative_pos_elbow1_top
        Relative_pos_elbow1_top = relative_pos(angle,position_elbow1,position_elbow1_y,position_top,position_top_y)
        worksheet.write(1, 21, Relative_pos_elbow1_top)

        # Relative_pos_wrist1_top
        Relative_pos_wrist1_top = relative_pos(angle,position_wrist1,position_wrist1_y,position_top,position_top_y)
        worksheet.write(1, 22, Relative_pos_wrist1_top)

        # Bag_Energy_x_impact_middle
        Bag_Energy_x_impact_middle = kinetic_energy(bag_mass,velocity_middle[0])
        worksheet.write(1, 23, Bag_Energy_x_impact_middle)

        # Bag_Energy_x_impact_lower
        Bag_Energy_x_impact_lower = kinetic_energy(bag_mass,velocity_lower[0])
        worksheet.write(1, 24, Bag_Energy_x_impact_lower)

        # Bag_Force_x_impact_middle
        Bag_Force_x_impact_middle = force(bag_mass,acceleration_middle[0])
        worksheet.write(1, 25, Bag_Force_x_impact_middle)

        # Bag_Force_x_impact_lower 
        Bag_Force_x_impact_lower = force(bag_mass,acceleration_lower[0])
        worksheet.write(1, 26, Bag_Force_x_impact_lower)

        
        ####################################################################################################################################################
        # Tackler_Energy_x_impact_left_hip
        Tackler_Energy_x_impact_left_hip = kinetic_energy(tackler_mass,velocity_hip1[0])
        worksheet.write(1, 27, Tackler_Energy_x_impact_left_hip)

        # Tackler_Force_x_impact_left_shoulder 
        Tackler_Force_x_impact_left_shoulder = force(tackler_mass,acceleration_shoulder1[0])
        worksheet.write(1, 28, Tackler_Force_x_impact_left_shoulder)

        # Power_of_tackler_x_left_shoulder 
        Power_of_tackler_x_left_shoulder = power(tackler_mass,velocity_shoulder1[0],acceleration_shoulder1[0])
        worksheet.write(1, 29, Power_of_tackler_x_left_shoulder) 
        ####################################################################################################################################################
        
        
        '''
        Note: hip1 and lower quartile had same velocity after impact (on average)
        '''
        # Momentum_bag_lower_before_impact
        Momentum_bag_lower_before_impact = momentum(bag_mass,velocity_lower[0])
        worksheet.write(1,30,Momentum_bag_lower_before_impact)

        # Momentum_left_hip_before_impact
        Momentum_left_hip_before_impact = momentum(bag_mass,velocity_hip1[0])
        worksheet.write(1,31,Momentum_left_hip_before_impact)

        # Momentum_baghip_before_impact(calculated)
        Momentum_baghip_before_impact = Momentum_left_hip_before_impact +Momentum_bag_lower_before_impact
        worksheet.write(1,32,Momentum_baghip_before_impact)

        # Velocity_after_impact_calculated
        Velocity_after_impact_calculated = Momentum_baghip_before_impact/(bag_mass+tackler_mass)
        worksheet.write(1,33,Velocity_after_impact_calculated)

        # Velocity_after_impact_actual

        '''
        Find when lower acceleration of bag change direction
        '''
        value = min(acceleration_lower)
        index = acceleration_lower.index(value)
        index_to_use = index+1
        print()
        print((acceleration_lower))
        print(index_to_use)
        print(len(velocity_hip1))
        print()
        Velocity_after_impact_actual=velocity_hip1[index_to_use]
        worksheet.write(1, 34, Velocity_after_impact_actual)

        # Distance_x_calculated
        #Distance_x_calculated = (1/fps)*
        #velocity_hip1[-1]

        # x_distance_travelled
        total_distance = 0
        
        for c in range (index_to_use,len(velocity_hip1)):
            total_distance = total_distance + velocity_hip1[c]*(1/fps)

        worksheet.write(1, 36, total_distance)

        # Contact_time 37
        total_time = 0
        
        for c in range (index_to_use,len(velocity_hip1)):
            total_time = total_time + (1/fps)

        worksheet.write(1, 37, total_time)

        workbook.close()
    main2()

if __name__ == "__main__":
    main()
