"""
This file merges the data from csv for sart and stroop tasks into one file
Author: Dan Shudrenko
Last edited: 12/8/2024 
"""

#my imports
import os
import pandas as pd

def main(): 
    # Specify the directory containing the files
    directory = "../FixedPowerData"

    # Get all files in the directory
    files = os.listdir(directory)

    # Create a set of base names without suffixes for matching pairs
    base_names = {file[:file.rfind('_')] for file in files}

    # Iterate over the base names and process only those with both _sart and _stroop files
    for base_name in base_names:
        print(base_name)
        sart_file = f"{base_name}_sart.csv"
        stroop_file = f"{base_name}_stroop.csv"
        print(sart_file)
        
        if sart_file in files and stroop_file in files:
            # Load the SART file (with headers)
            sart_data = pd.read_csv(os.path.join(directory, sart_file))
            
            # Load the Stroop file (without headers)
            stroop_data = pd.read_csv(os.path.join(directory, stroop_file), header=0)
            
            # Append the stroop_data (without its column names)
            merged_data = pd.concat([sart_data, stroop_data], ignore_index=True)
            
            # Save the merged data to a new file
            merged_file = os.path.join(directory, f"{base_name}_merged.csv")
            merged_data.to_csv(merged_file, index=False)
            
if __name__ == "__main__": 
    main()