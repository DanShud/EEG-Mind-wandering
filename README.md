# Predicting Episodes of Mind-Wandering Based on EEG Recordings
**Date of last edit:** 12/10/2024
**Authors:** Dan Shudrenko, Kai Britt, Ben Jiang 

## Project description
Please see the presentation following the link: https://docs.google.com/presentation/d/1hhglEtu1wiVbnQMD9HLInSBZO80fBzj4UeyEVY4FyDM/edit?usp=sharing
### Data
The data come from (n = 37) participants recruited at Haverford College for Compton and colleagues (2024) study.

Cleaned featurized data separated by task for each participant can be found in **FixedPowerData folder**

Cleaned featurized data merged for both tasks for each participant can be found in **DataMerged folder**
### Goal
Replicate the machine learning algorithm utilized by Jin and colleagues (2019) to predict mind-wandering episodes based on different types of EEG recording. 
### References
Compton, R. J., Shudrenko, D., Mann, K., Turdukulov, E., Ng, E., & Miller, L. (2024). Effects of task context on EEG correlates of mind-wandering. _Cognitive, Affective, & Behavioral Neuroscience_, 24(1), 72–86. https://doi.org/10.3758/s13415-023-01138-9

Jin, C. Y., Borst, J. P., & van Vugt, M. K. (2019). Predicting task-general mind-wandering with EEG. Cognitive, Affective, & Behavioral Neuroscience, 19(4), 1059–1073. https://doi.org/10.3758/s13415-019-00707-1
## Implementation
### Data processing
**MatLabIntialProcessing folder** contains the following step
1. Extracting voltage values and event markers:
Converted MATLAB tables to CSV tables using PowerShell bash code

**FeatureExtraction folder** contains the following steps

2. Participants were excluded on the following basis:
- Missing event markers in the original data
- Less than 3 episodes of mind-wandering or being on task, i.e. participant likely didn't respond to the mind-wandering probe truly
3. During extraction for the features below the time blocks marked as "bad blocks"—issues with the EEG recording—were excluded. If such an exclusion resulted in one or more missing features for the data point, the data point was excluded from the analysis. 
4. Event-related potentials (ERPs): 
- Highest voltage at 100-250 ms for P2
- Lowest voltage from 250 to 450 ms for N2
4. Power of alpha waves and theta waves:
We utilized Fourier transformation from MNE EEG python package to quantify the power of theta and alpha frequencies 5000 ms prior to stimuli
### Training Model
We group data by the two different tasks: “sart” and “stroop”. 2/3 of data points are used for training, 1/3 of data points are used for testing. Since each subject only has around 10-15 data points, using this partition will avoid a very discrete accuracy. The training was done using SVM, "rbf" kernel. Please look at the **ModelTraining folder** for more information. 

### Vizualization
Run stroop_from_sart or svm_individual.py with the -v flag from the ModelTraining Directory
### Results
- For training on individual subjects, the average accuracy was 55%
- For training on Sart data and testing on Stroop data, accuracy was 56%
- For training on Stroop data and testing on Sart data, accuracy was 61%

### Lab Notebook
**Dan Shudrenko: 11/30 (2 hours):**
- Creating general setup, e.g., GitHub repositories, readme file 
- Figured a way to access the data in the needed format
- Get accustomed to the data type and come up with the conceptual implementation of the project

**Dan Shudrenko and Kai: 12/2 (2.5 hours):**
- Figured out how to extract data
- (Kai) understood data.
- data is 2048 Hz

**Kai: 12/3 (2 hours):**
- Modified Matlab script
- Wrote Powershell script to iterate over subjects and get data as CSV 
- extracted some sample data

**Dan: 12/3 (1 hours):**
- Manually downloaded and converted all the data: I HATE SOFRTWARE FOR PSYCHOLOFY RESEARCH

**Dan: 12/4 (4 hours):**
- Featurized the data

**Kai: 12/4 (1 hours):**
- Developed function for extracting band frequencies

**Dan and Kai: 12/5 (1 hours):**
- Debugging

**Dan, Kai and Ben: 12/5 (1 hours):**
- Examined featurized data and decided how to train the model

**Ben: 12/6 (2 hours):**
- Parsed data and trained the initial SVM model

**Dan, Kai and Ben: 12/7 (4 hours):**
- Finished training begin visualization

**Dan, Kai and Ben: 12/8 (2 hours):**
- Made a presentation

**Dan 12/10 (1 hours):**
- Finished Readme file and commented my code
