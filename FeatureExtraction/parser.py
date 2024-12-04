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

'''
class Subject: 
    """
    This class contains original data from one subject
    """

    def __init__ (self, data, events):
        #input: df with voltage data and df with event markers
        self.data = data
        self.events = events
'''

class Data_point: 

    def __init__ (self):
        self = self


class Sub_SART:
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
    df_data = pd.read_csv(filepath_data)
    df_event = pd.read_csv(filepath_event)
    #first I will be working with SART data



