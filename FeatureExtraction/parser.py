"""
This file contains the class and function that allows to read
and parse throught the data whil will be later used to extract
features necessary for training
Author: Danylo Shudrenko
Date: 12/4/2024
"""

#MY IMPORTS
import numpy as np 

#MY CLASSES

class Sub:
    '''
    This class stores the featurized data about
    subject and converts it to csv that is 
    further used for the training
    '''
    def __init__ (self, data, col_names):
        #intializing the class
        self.data = [col_names]

    def append(self, data_point):
        #appendign data point
        self.data.append(data_point)
    
    def csv_save(self):
        '''
        This method saves subject's featurized
        data as a CSV file
        '''
        pass 


#MY FUNCTIONS

def parsing(filepath_data, filepath_event):
    '''
    This function open the csv files as data frames
    based on their location and parses through them
    '''
    #opening files
    data = np.loadtxt(filepath_data, delimiter=",", dtype=float, skiprows=1)
    event =np.loadtxt(filepath_data, delimiter=",", dtype=float, skiprows=1)
    #first I will be working with SART data
    #going through all the events
    for i in range(len(event)):
        #intializing label and features
        label = 0
        features = []
        #finding the label 
        if event[i][1] == 24: 
            if event[i + 1][1] == 16:
                label = 1
            while 
            




