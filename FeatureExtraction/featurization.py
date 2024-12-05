"""
This file contains all the functions neccessary to extract all the features 
Author: Dan Shudrenko, Kai Britt
Date: 12/4/2024
"""
import numpy as np
def get_power(last_second : int, data):
    """
    preforms fouier transform given 5 second interval given the last second of the interval in the format of 
    1x18 where [F3_t,F3_a,Fz_t,Fz_a,F4_t,F4_a,C3_t,C3_a,Cz_t,Cz_a,C4_t,C4_a,P3_t,P3_a,Pz_t,Pz_a,P4_t,P4_a]
    """

    skip = [6,7,11,12,13]
    output = []
    hz = 2048
    interval = 5 * hz
    target_data = data[last_second-interval:last_second+1,:]
    
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

if __name__ == "__main__":
    subject_file = r"C:\Users\kaibr\Downloads\DanDataScienceProjectFeelFreeToDelete\DanDataScienceProjectFeelFreeToDelete\subject_data\sub_59.cdt_data.csv"
    subject_data =  np.genfromtxt(subject_file,skip_header=1, delimiter=','    )
    print(get_power(500000,subject_data))