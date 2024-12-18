# 
from sklearn import svm
from sklearn.metrics import accuracy_score
import os
import pandas as pd
import matplotlib.pyplot as plt
import argparse


def parse_args():
  """Parse command line arguments (train and test arff files)."""
  parser = argparse.ArgumentParser(description='parsing command line arguments')

  parser.add_argument('-v','--viz',nargs='?', default=False, const=True)

  args = parser.parse_args()


def main():

  args = parse_args()
  viz = args.viz
  # Load dataset
  accuracies = []
  names = ["sart-stroop", "stroop-sart", "sart-sart", "stroop-stroop"]
  file_names = os.listdir("./FixedPowerData")
  
  train_partition = pd.DataFrame()
  test_partition = pd.DataFrame()
  
  target_sub = []
  part_size = []
  for train_set in ["sart","stroop"]:
    for name in sorted(file_names):
      #the code to train on sart or stroop
      if train_set in name:
        target_sub.append(name)
        csv_file = pd.read_csv("./FixedPowerData/" + name)
        csv_file.sample(frac=1)
        train = csv_file
        # Partition the dataset into train and test (partition across all test subjects)
        train_partition = pd.concat([train_partition, train])
      else:
        target_sub.append(name)
        csv_file = pd.read_csv("./FixedPowerData/" + name)
        csv_file.sample(frac=1)
        test = csv_file
        # Partition the dataset into train and test (partition across all test subjects)
        test_partition = pd.concat([test_partition, test]) 
    
      # if "sart" in name: # Only sart data
      #   target_sub.append(name)
      #   csv_file = pd.read_csv("./FixedPowerData/" + name)
      #   csv_file.sample(frac=1)
      #   num_part = int(len(csv_file) * (2/3))
      #   train = csv_file.iloc[:num_part]
      #   test = csv_file.iloc[num_part:]
      #   part_size.append(len(test))
      #   # Partition the dataset into train and test (partition across all test subjects)
      #   train_partition = pd.concat([train_partition, train])
      #   test_partition = pd.concat([test_partition, test])
      
    train_np = train_partition.to_numpy()
    test_np = test_partition.to_numpy()
    
    # Separate dataset into feature and label
    train_x = train_np[:, :-1]
    train_y = train_np[:, -1:].reshape(-1)
    test_x = test_np[:, :-1]
    test_y = test_np[:, -1:].reshape(-1)
    
  
    # Normalize data
    # train_x_mean = train_x.mean(axis=0)
    # train_x_std = train_x.std(axis=0)
    # train_x -= train_x_mean
    # train_x /= train_x_std
    
    # test_x_mean = test_x.mean(axis=0)
    # test_x_std = test_x.std(axis=0)
    # test_x -= test_x_mean
    # test_x /= test_x_std
    
    # Create SVM classifier and train model
    clf = svm.SVC(kernel='rbf', verbose=True, max_iter= 1000000)
    clf.fit(train_x, train_y)
    
    # Make prediction on test data
    # pred_y = clf.predict(test_x)
    # for i, name in zip(range(len(test_y)),target_sub):
    #   pred_y = clf.predict(test_x[i: i+part_size[i]])
    #   accuracy = accuracy_score(test_y[i: i+part_size[i]], pred_y)
      
    #   print(f"Participant {name} accuracy: {accuracy}")
    
    # Calculate accuracy of model
    accuracy = accuracy_score(test_y, clf.predict(test_x))
    accuracies.append(accuracy)
    print("Accuracy: " + str(accuracy))
    #print(clf.coef_)
    

    target_sub = []
  part_size = []
  for train_set in [("sart",2/3),("stroop",4/5)]:
    for name in sorted(file_names):
      #the code to train on sart or stroop
      if train_set[0] in name:
        target_sub.append(name)
        csv_file = pd.read_csv("../FixedPowerData/" + name)
        csv_file.sample(frac=1)
        # Partition the dataset into train and test (partition across all test subjects)
        train_partition = pd.concat([train_partition, train])
    
    num_part = int(len(csv_file) * train_set[1])
    train = csv_file[:num_part]
    test = csv_file[num_part:]

      # if "sart" in name: # Only sart data
      #   target_sub.append(name)
      #   csv_file = pd.read_csv("./FixedPowerData/" + name)
      #   csv_file.sample(frac=1)
      #   num_part = int(len(csv_file) * (2/3))
      #   train = csv_file.iloc[:num_part]
      #   test = csv_file.iloc[num_part:]
      #   part_size.append(len(test))
      #   # Partition the dataset into train and test (partition across all test subjects)
      #   train_partition = pd.concat([train_partition, train])
      #   test_partition = pd.concat([test_partition, test])
      
    train_np = train_partition.to_numpy()
    test_np = test_partition.to_numpy()
    
    # Separate dataset into feature and label
    train_x = train_np[:, :-1]
    train_y = train_np[:, -1:].reshape(-1)
    test_x = test_np[:, :-1]
    test_y = test_np[:, -1:].reshape(-1)
    
  
    # Normalize data
    # train_x_mean = train_x.mean(axis=0)
    # train_x_std = train_x.std(axis=0)
    # train_x -= train_x_mean
    # train_x /= train_x_std
    
    # test_x_mean = test_x.mean(axis=0)
    # test_x_std = test_x.std(axis=0)
    # test_x -= test_x_mean
    # test_x /= test_x_std
    
    # Create SVM classifier and train model
    clf = svm.SVC(kernel='rbf', verbose=True, max_iter= 1000000)
    clf.fit(train_x, train_y)
    
    # Make prediction on test data
    # pred_y = clf.predict(test_x)
    # for i, name in zip(range(len(test_y)),target_sub):
    #   pred_y = clf.predict(test_x[i: i+part_size[i]])
    #   accuracy = accuracy_score(test_y[i: i+part_size[i]], pred_y)
      
    #   print(f"Participant {name} accuracy: {accuracy}")
    
    # Calculate accuracy of model
    accuracy = accuracy_score(test_y, clf.predict(test_x))
    accuracies.append(accuracy)
    print("Accuracy: " + str(accuracy))
    #print(clf.coef_)


  if viz:
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('none')  # Set figure background to transparent
    ax.set_facecolor('none')  # Set axes background to transparent
    bars = ax.bar(names, accuracies)
    ax.bar_label(bars)
    # plt.bar(names, accuracies, color ='b', 
            # width = 0.4)

    plt.xlabel("Train-Test")
    plt.ylabel("Accuracy")
    plt.title("train/test partitions")
    plt.show()

if __name__ == "__main__":
  main()