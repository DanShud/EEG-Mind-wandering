"""
This file runs through all the files in the data folder and 
performs feature extraction and outputs it in the reponsive file
Author: Dan Shudrenko
Date: 12/9/2024
"""

#MY IMPORTS
from Parse import*
import os

#MY FUNCTIONS
def main(): 
    #setting the path to directory
    directory_path = "D:/DataSci F24/Data"
    #finding all files in the directory
    files = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename) 
        files.append(file_path)
    files = sorted(files)
    #parsing and saving the files
    for i in range(0, len(files), 2): 
        sart, strop = parsing(files[i], files[i+1])
        sart.csv_save("./" + files[i][files[i].rfind("\\"):-3] + "_sart.csv")
        strop.csv_save("./" + files[i][files[i].rfind("\\"):-3] + "_stroop.csv")


if __name__ == "__main__": 
    main()