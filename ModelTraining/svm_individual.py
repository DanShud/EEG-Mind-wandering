"""
Name: Ben Jiang
Date: Dec 10, 2024
Description: This file parses the merged data by name, partitions the data, and trains the svm model for each individual participant. 
"""

from sklearn import svm
from sklearn.metrics import accuracy_score
import os
import pandas as pd
import argparse
import numpy as np


def parse_args():
    """Parse command line arguments (train and test arff files)."""
    parser = argparse.ArgumentParser(description='parsing command line arguments')

    parser.add_argument('-v','--viz',nargs='?', default=False, const=True)

    args = parser.parse_args()

    return args
import matplotlib.pyplot as plt

def main():
  # Load dataset
  args = parse_args()
  viz = args.viz
  file_names = os.listdir("../DataMerged")
  
  accuracies = []
  tprs = []
  tnrs = []
  mind_wanderin_rate = []
  
  for name in sorted(file_names):
    #the code to train on sart or stroop
    if True:
      print(name)
      csv_file = pd.read_csv("../DataMerged/" + name)
      csv_file.sample(frac=1)
      
      # Use 2/3 for sart, 4/5 for stroop
      num_part = int(len(csv_file) * (2/3))
      train = csv_file.iloc[:num_part]
      test = csv_file.iloc[num_part:]
      
      train_np = train.to_numpy()
      test_np = test.to_numpy()
      
      # Separate dataset into feature and label
      train_x = train_np[:, :-1]
      train_y = train_np[:, -1:].reshape(-1)
      test_x = test_np[:, :-1]
      test_y = test_np[:, -1:].reshape(-1)
  
      mind_wanderin_rate.append((sum(train_y) + sum(test_y)) / (len(train_y) + len(test_y)))
 
      # Normalize data
      train_x_mean = train_x.mean(axis=0)
      train_x_std = train_x.std(axis=0)
      train_x -= train_x_mean
      train_x /= train_x_std
      
      test_x_mean = test_x.mean(axis=0)
      test_x_std = test_x.std(axis=0)
      test_x -= test_x_mean
      test_x /= test_x_std
  
      # Create SVM classifier and train model
      clf = svm.SVC(kernel='rbf', verbose=True, max_iter= 1000000)
      clf.fit(train_x, train_y)
      pred_y = clf.predict(test_x)
      accuracy = accuracy_score(test_y,  pred_y)
      accuracies.append(accuracy)
      tpr = 0
      tnr = 0
      for i in range(len(test_y)):
        if test_y[i] == 1 and test_y[i] == pred_y[i]:
          tpr += 1
        elif test_y[i] == 0 and test_y[i] == pred_y[i]:
          tnr += 1
      
      tpr = tpr / sum(test_y)
      tnr = tnr / (len(test_y) - sum(test_y))
      tprs.append(tpr)
      tnrs.append(tnr)

        


      print(f"Accuracy for {name}: {str(accuracy)}")
  
  
  
  print(f"Total accuracy: {sum(accuracies) / len(accuracies)}")
  # print(tnrs)
  # print(tprs)  
  # print(mind_wanderin_rate)
  
  if viz:
    plt.scatter(mind_wanderin_rate, tprs, label="Individual Subject")
    plt.xlabel("Mind wandering rate")
    plt.ylabel("True positive rate")
    plt.title("Mind wandering rate vs. True positive rate")
    plt.legend()
    plt.savefig("mwr:tpr.png", format="png")
    
    
    plt.clf()

    width = 0.2  # Adjust bar width
    subjects = np.arange(len(file_names))  # 0, 1, 2, ...

    # Plotting
    plt.bar(subjects - width, tprs, width, label="True positive rate")
    plt.bar(subjects + width, tnrs, width, label="True negative rate")
    plt.bar(subjects, accuracies, width, label="Accuracy")

    # Labels and legend
    plt.xlabel("Subjects")
    plt.xticks(subjects, subjects)  # Align x-ticks with group centers
    plt.title("Performance Measure")
    plt.legend()

    # Save and show the plot
    plt.savefig("individual_performance.png",transparent=True)
    plt.clf()
        

if __name__ == "__main__":
  main()