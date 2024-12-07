from sklearn import svm
from sklearn.metrics import accuracy_score
import os
import pandas as pd

def main():
  # Load dataset
  file_names = os.listdir("../DataMerged")
  
  accuracies = []
  
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
      
      accuracy = accuracy_score(test_y, clf.predict(test_x))
      accuracies.append(accuracy)
      print(f"Accuracy for {name}: {str(accuracy)}")
  
  
  
  print(f"Total accuracy: {sum(accuracies) / len(accuracies)}")
  


if __name__ == "__main__":
  main()