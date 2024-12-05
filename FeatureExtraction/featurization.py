"""
This file contains all the functions neccessary to extract all the features 
Author: Dan Shudrenko, Kai Britt
Date: 12/4/2024
"""

#MY IMPORTS
import numpy as np

#MY FUNCTIONS
def get_power(current_event : int, data, event):
    """
    preforms fouier transform given 5 second interval given the last second of the interval in the format of 
    1x18 where [F3_t,F3_a,Fz_t,Fz_a,F4_t,F4_a,C3_t,C3_a,Cz_t,Cz_a,C4_t,C4_a,P3_t,P3_a,Pz_t,Pz_a,P4_t,P4_a]
    """

    skip = [6,7,11,12,13]
    output = []
    hz = 2048
    interval = 5 * hz
   
    ###THE FOLLOWING LINE OF CODE TAKE INTO ACCOUNT BAD BLOCKS########################
    last_second = event[current_event][0]
    #initializing not bad block points
    target_data = np.array([])
    #finding the start of the data
    start = last_second - interval 
    j = current_event - 1
    #going to the last event 5 seconds ago 
    while j >= 0 and event[j][3] >= start:
        j -= 1
    j += 1
    #checking all the bad blocks and respectively adjusting data
    for i in range(j, current_event + 1):
        #if it is a bad block 
        if event[i][1] == 700000: 
            #if the bad block begins later after start 
            if event[i][2] > start: 
                target_data = np.concatenate((target_data, data[start:event[i][2],:]))
            else: #if the bad block begins after start
                start = event[i][3]
    #checking if we need to close add anything
    if last_second+1 > start: 
        target_data = np.concatenate((target_data, data[start:last_second+1,:]))
    ###############################################################################
    theta = [4,8]
    alpha = [8,12]
    output = []
    for electrode in range(target_data.shape[1]):
        if electrode == skip:
            continue
        else:
            fft_result = np.fft.fft(target_data[:,electrode])
            freqs = np.fft.fftfreq(len(target_data[:,electrode]), d=1/hz)
            power_spectrum = np.abs(fft_result)**2 / target_data.shape[0]
            theta_power = np.sum(power_spectrum[(freqs >= theta[0]) & (freqs < theta[1])])
            alpha_power = np.sum(power_spectrum[(freqs >= alpha[0]) & (freqs < alpha[1])])
            output.extend([theta_power,alpha_power])
    return output

#Testing the function
if __name__ == "__main__":
    subject_file = r"C:\Users\kaibr\Downloads\DanDataScienceProjectFeelFreeToDelete\DanDataScienceProjectFeelFreeToDelete\subject_data\sub_59.cdt_data.csv"
    subject_data =  np.genfromtxt(subject_file,skip_header=1, delimiter=','    )
    print(get_power(500000,subject_data))