"""
This file contains the class and function that allows to read
and parse throught the data whil will be later used to extract
features necessary for training
Author: Danylo Shudrenko
Date: 12/9/2024
"""

#MY IMPORTS
import numpy as np 
from data_feat import*
import csv
#MY CLASSES

class Sub:
    '''
    This class stores the featurized data about
    subject and converts it to csv that is 
    further used for the training
    '''
    def __init__ (self, col_names):
        #intializing the class
        self.data = [col_names]

    def append(self, data_point):
        #appendign data point
        self.data.append(data_point)
    
    def csv_save(self, file_name):
        '''
        This method saves subject's featurized
        data as a CSV file
        '''
        counter = 0
        for i in range(1, len(self.data)):
            counter += self.data[i][-1]
        if counter > 2 and counter < len(self.data) - 2:
            with open(file_name, mode = "w", newline="") as file: 
                writer = csv.writer(file)
                writer.writerows(self.data)
                file.close()

    def cleaner(self):
        """
        This function deletes rows with weird data
        """
        #initializing the list of elements to delete
        lines_to_delete = []
        #going through every line of data
        for i in range(1, len(self.data)):
            flag = 1
            #checking if P2 are negative
            for j in range(18, 27):
                if self.data[i][j] <= 0: 
                    lines_to_delete.append(i)
                    flag = 0
                    break
            if flag:
                #checking if N2 is positive
                for j in range(27, 35):
                    if self.data[i][j] >= 0: 
                        lines_to_delete.append(i)
                        break
        lines_to_delete.reverse()
        for line in lines_to_delete:
            self.data.pop(line)



#MY FUNCTIONS

def parsing(filepath_data, filepath_event):
    '''
    This function open the csv files as data frames
    based on their location and parses through them
    '''
    #opening files
    data = np.loadtxt(filepath_data, delimiter=",", dtype=float, skiprows = 1)
    event =np.loadtxt(filepath_event, delimiter=",", dtype=float, skiprows = 1)
    #first I will be working with SART data
    col_names = ["F3_t","F3_a","Fz_t","Fz_a","F4_t","F4_a","C3_t","C3_a","Cz_t",
                 "Cz_a","C4_t","C4_a","P3_t","P3_a","Pz_t","Pz_a","P4_t","P4_a",
                 "F3_P2", "Fz_P2", "F4_P2", "C3_P2", "Cz_P2", "C4_P2", "P3_P2", "Pz_P2", "P4_P2",
                 "F3_N2", "Fz_N2", "F4_N2", "C3_N2", "Cz_N2", "C4_N2", "P3_N2", "Pz_N2", "P4_N2", "label"
                 ]
    sart = Sub(col_names)
    #going through all the events
    for i in range(len(event)):
        #intializing label and features
        label = 0
        feat_val = []
        #finding the label 
        if event[i][1] == 24: 
            if event[i + 1][1] == 16:
                label = 1
            #finding feature values
            feat_val = get_power(i, data, event)
            feat_val.extend(ERPs(i, data, event))
            feat_val.append(label)
            sart.append(feat_val)
    sart.cleaner()
    stroop = Sub(col_names)
    for i in range(len(event)):
        #intializing label and features
        label = 0
        feat_val = []
        #finding the label 
        if event[i][1] == 40: 
            if event[i + 1][1] == 32:
                label = 1
            #finding feature values
            feat_val = get_power(i, data, event)
            feat_val.extend(ERPs(i, data, event))
            feat_val.append(label)
            stroop.append(feat_val)
    stroop.cleaner()
    #returning parsed and featurized data
    return (sart, stroop)



            




