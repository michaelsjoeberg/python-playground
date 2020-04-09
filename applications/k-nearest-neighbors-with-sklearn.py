# https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

# assign column names
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'Class']

# read dataset into dataframe
dataset = pd.read_csv(url, names=names)
#dataset.head()

# preprocessing
x = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 4].values

# train-test split
from sklearn.model_selection import train_test_split

# 80% train data, 20% test data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20)

# feature scaling
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(x_train)

x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

# training and predictions
from sklearn.neighbors import KNeighborsClassifier

classifier = KNeighborsClassifier(n_neighbors=5)
classifier.fit(x_train, y_train)

y_prediction = classifier.predict(x_test)
#y_prediction

# evaluate
from sklearn.metrics import classification_report, confusion_matrix

print(confusion_matrix(y_test, y_prediction))
print(classification_report(y_test, y_prediction))

'''
Michael Sjoeberg
2020-04-09
https://github.com/michaelsjoeberg/python-playground/blob/master/applications/k-nearest-neighbors-with-sklearn.py
'''