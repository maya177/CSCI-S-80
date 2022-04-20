import csv
import sys
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

months = {'Jan': 0,
        'Feb': 1,
        'Mar': 2,
        'Apr': 3,
        'May': 4,
        'June': 5,
        'Jul': 6,
        'Aug': 7,
        'Sep': 8,
        'Oct': 9,
        'Nov': 10,
        'Dec': 11}

with open('shopping.csv', 'r') as file:
    lines = list(csv.DictReader(file))

for line in lines:
    for month in months:
        if line['Month'] == month:
            line['Month'] = months[month]
            print(months[month])
            print(line['Month'])