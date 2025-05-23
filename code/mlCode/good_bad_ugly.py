# -*- coding: utf-8 -*-
"""good_bad_ugly.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FdkubISuG8CL5mrmCxYdYX0ZqsXMPYgF
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from imblearn.over_sampling import RandomOverSampler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

train_data = pd.read_csv('../../data/ML/train-test/train.csv', sep = '\t')

test_data = pd.read_csv('../../data/ML/train-test/train.csv', sep = '\t')

train_data = train_data.drop(columns=['Project', 'file', 'ChangeValue'])
# train_data = train_data.drop(columns=[
#                          "SLOCStandard",
#                          "Readability",
#                          "McCabe",
#                          "MaximumBlockDepth",
#                          "uniqueFanOut",
#                          "MaintainabilityIndex",
#                          "isGetterSetter",
#                          "Parameters"
#                         ])
train_data = train_data[train_data.Type != 'noise']
train_data = train_data[train_data.Type != 'bad']
test_data = test_data.drop(columns=['Project', 'file', 'ChangeValue'])
# test_data = test_data.drop(columns=[
#                          "SLOCStandard",
#                          "Readability",
#                          "McCabe",
#                          "MaximumBlockDepth",
#                          "uniqueFanOut",
#                          "MaintainabilityIndex",
#                          "isGetterSetter",
#                          "Parameters"
#                         ])
test_data = test_data[test_data.Type != 'noise']
test_data = test_data[test_data.Type != 'bad']

train_x = train_data.drop(columns=['Type'])
test_x = test_data.drop(columns=['Type'])
train_y = train_data["Type"]
test_y = test_data["Type"]

ros = RandomOverSampler(random_state=0)
train_x, train_y = ros.fit_resample(train_x, train_y)



"""**### Training with RandomForest**"""

#rf_cls = RandomForestClassifier(n_estimators = 10)
#rf_cls = LogisticRegression(random_state=0, max_iter = 1000)
rf_cls = DecisionTreeClassifier(random_state=0, max_depth = 10)
rf_cls.fit(train_x, train_y)

pred_train_y = rf_cls.predict(train_x)

# Calculate accuracy
accuracy = accuracy_score(train_y, pred_train_y)   # https://medium.com/@maxgrossman10/accuracy-recall-precision-f1-score-with-python-4f2ee97e0d6
print("Training Accuracy: ", accuracy)

# Calculate precision
precision = precision_score(train_y, pred_train_y, average='macro')
print("Training Precision: ", precision)

# Calculate recall (sensitivity)
recall = recall_score(train_y, pred_train_y, average='macro')
print("Training Recall: ", recall)

# Calculate F1-score
f1 = f1_score(train_y, pred_train_y, average='macro')
print("Training F1-Score: ", f1)

pred_test_y = rf_cls.predict(test_x)

# Calculate accuracy
accuracy = accuracy_score(test_y, pred_test_y)   # https://medium.com/@maxgrossman10/accuracy-recall-precision-f1-score-with-python-4f2ee97e0d6
print("Testing Accuracy: ", accuracy)

# Calculate precision
precision = precision_score(test_y, pred_test_y, average='macro')
print("Testing Precision: ", precision)

# Calculate recall (sensitivity)
recall = recall_score(test_y, pred_test_y, average='macro')
print("Testing Recall: ", recall)

# Calculate F1-score
f1 = f1_score(test_y, pred_test_y, average='macro')
print("Testing F1-Score: ", f1)





