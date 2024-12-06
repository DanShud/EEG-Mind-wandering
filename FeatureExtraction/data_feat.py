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
    target_data = None
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
                if isinstance(target_data, np.ndarray):
                    target_data = np.concatenate((target_data, data[int(start):int(event[i][2]), :]))
                else:
                    target_data =  data[int(start):int(event[i][2]), :]
            else: #if the bad block begins after start
                start = event[i][3]
    #checking if we need to close add anything
    if last_second+1 > start: 
        if isinstance(target_data, np.ndarray):
            target_data = np.concatenate((target_data, data[int(start):int(last_second+1), :]))
        else:
            target_data =  data[int(start):int(last_second+1), :]
    ###############################################################################
    theta = [4,8]
    alpha = [8,12]
    output = []
    for electrode in range(target_data.shape[1]):
        if electrode in skip:
            continue
        else:
            fft_result = np.fft.fft(target_data[:,electrode])
            freqs = np.fft.fftfreq(len(target_data[:,electrode]), d=1/hz)
            power_spectrum = np.abs(fft_result)**2 / target_data.shape[0]
            theta_power = np.sum(power_spectrum[(freqs >= theta[0]) & (freqs < theta[1])])
            alpha_power = np.sum(power_spectrum[(freqs >= alpha[0]) & (freqs < alpha[1])])
            output.extend([theta_power,alpha_power])
    return output

def ERPs(current_event, data, event):
    """
    This function find P2 and N2 peaks for the last 5 
    stimuli and averages them
    """
    #the electrodes that can be skipped
    skip = [6,7,11,12,13]
    #frequency of recording per ms
    hz = 2048 / 1000
    #intializing the values
    P2 = []
    N2 = []
    for i in range(data.shape[1]):
        if i not in skip:
            P2.append(0)
            N2.append(0)
    #trying to find 5 past events before probe
    past = 5
    count_P2 = 0
    count_N2 = 0 
    i = current_event - 1
    while past > 0: 
        #if it is not a bad block
        if event[i][1] != 700000:
            #then we need one event less 
            past -= 1
            #checking if this event is not a bad block
            P2_bad = 1
            N2_bad = 1
            #going through the past 15 events and checking if they are not bad blocks
            now = i
            #
            for j in range(now - 15, now): 
                if event[j][3]  > event[i][2] + 100 *  hz:
                    #marking if there is a bad block
                    P2_bad = 0
                    
                if event[j][3] > event[i][2] + 250 *  hz:
                    #marking if there is a bad block
                    N2_bad = 0
                    
            #if they are no bad blocks
            if  P2_bad:
                #increasing count of trial we took into accoutn
                count_P2 += 1
                #intializing the index in P2 array
                j = 0
                for electrode in range(data.shape[1]): 
                    if electrode not in skip: #if it is electrode of interest
                        #finding the maximum value in the time window of 100-250 ms post response
                        P2[j] += np.max(data[int(event[i][2] + (100*hz)):int(event[i][2] + (250*hz)), electrode])
                        j += 1
            if  N2_bad:
                #increasing count of trial we took into accoutn
                count_N2 += 1
                #intializing the index in P2 array
                j = 0
                for electrode in range(data.shape[1]): 
                    if electrode not in skip: #if it is electrode of interest
                        #finding the minimum value in the time window of 250-400 ms post response
                        N2[j] += np.min(data[int(event[i][2] + (250*hz)):int(event[i][2] + (400*hz)), electrode])
                        j += 1
        else:
            # read a bad block just get previous event
            i -= 1
    #finding the average
    for i in range(9):
        if count_P2:
            P2[i] /= count_P2
        if count_N2:
            N2[i] /= count_N2
    #merging them
    P2.extend(N2)
    return P2 


#Testing the function
if __name__ == "__main__":
    subject_file = ""
    event_file  = ""
    subject_data =  np.genfromtxt(subject_file,skip_header=1, delimiter=','    )
    event_data = np.genfromtxt(event_file,skip_header=1, delimiter=','    )   
    print(get_power(800,subject_data, event_data))