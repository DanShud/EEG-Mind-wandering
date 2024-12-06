from sklearn import svm
from sklearn.metrics import accuracy_score
import os
import pandas as pd

def main():
  # Load dataset
  file_names = os.listdir("./Data_featurized")
  
  train_partition = pd.DataFrame()
  test_partition = pd.DataFrame()
  
  
  for name in file_names:
    if "sart" in name: # Only sart data
      csv_file = pd.read_csv("./Data_featurized/" + name)
      train = csv_file.iloc[:10]
      test = csv_file.iloc[10:]
      
      # Partition the dataset into train and test (partition across all test subjects)
      train_partition = pd.concat([train_partition, train])
      test_partition = pd.concat([test_partition, test])
    
  train_np = train_partition.to_numpy()
  test_np = test_partition.to_numpy()
  
  # Separate dataset into feature and label
  train_x = train_np[:, :-1]
  train_y = train_np[:, -1:].reshape(-1)
  test_x = test_np[:, :-1]
  test_y = test_np[:, -1:].reshape(-1)
    
  # Create SVM classifier and train model
  clf = svm.SVC(kernel='linear', verbose=True, max_iter=10000000)
  clf.fit(train_x, train_y)
  
  # Make prediction on test data
  pred_y = clf.predict(test_x)
  
  # Calculate accuracy of model
  accuracy = accuracy_score(test_y, pred_y)
  
  print("Accuracy: " + str(accuracy))
  


if __name__ == "__main__":
  main()