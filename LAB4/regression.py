from os import truncate
from typing import ValuesView
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# train_data.info()
# print(count("recommend", "score", train_data))

# train_data = pd.read_csv('nursery.csv')


class Dataset:

    def __init__(self, file):
        self.dataset = pd.read_csv(file)


    def get_dataset_columns(self):
        return [column for column in self.dataset.columns] 


    def get_category_id(self, category):
        columns = self.get_dataset_columns()
        found = False
        id = 0
        while not found:
            if columns[id] == category:
                found = True
            else:
                id += 1
        return id

    def count(self, value, category):
        # number = dataset.score.value_counts()
        last_column = category
        # last_column = dataset.columns[-1]
        number = self.dataset[last_column].value_counts()[value]
        return number

    def frequency(self, value, category):
        return self.count(value, category) / len(self.dataset.index)

    def complete_entropy(self):      #entropia zbioru U (całego)
        complete_entropy = 0
        last_column = self.dataset.columns[-1]
        for value in self.dataset[last_column].unique():
            freq = self.frequency(value, last_column)
            entropy = -freq * np.log(freq)
            complete_entropy += entropy
        return complete_entropy

    def category_entropy(self, category):
        cat_entropy = 0
        cat_id = self.get_category_id(category)
        last_column = self.dataset.columns[-1]
        last_id = self.get_category_id(last_column)
        for value in self.dataset[category].unique():
            # print("Value : " + value)
            freq = self.frequency(value, category)
            cat_count = self.count(value, category)
            # print("Cat_count : " + str(cat_count))
            h = 0
            for score_value in self.dataset[last_column].unique():
                matches = 0
                for row in range(len(self.dataset.index)):
                    if self.dataset.iat[row, cat_id] == value and self.dataset.iat[row, last_id] == score_value:
                        matches += 1
                # print(score_value + " - matches: " + str(matches))
                divided_frequency = matches / cat_count
                if divided_frequency != 0:
                    h += - divided_frequency * np.log(divided_frequency)
            cat_entropy += h * freq
        return cat_entropy

    def inf_gain(self, category):
        return self.complete_entropy() - self.category_entropy(category)

    def dsc_inf_gains(self):
        entropies = []
        columns = self.get_dataset_columns()
        columns.pop()
        for column in columns:
            entropies.append([self.inf_gain(column), column])
        entropies.sort(reverse=True)
        return entropies

# train_data = pd.read_csv('test.csv')

# def get_category_id(category, dataset):
#     columns = get_dataset_columns(dataset)
#     found = False
#     id = 0
#     while not found:
#         if columns[id] == category:
#             found = True
#         else:
#             id += 1
#     return id


# def get_dataset_columns(dataset):
#     return [column for column in dataset.columns]


# def count(value, category, dataset):
#     # number = dataset.score.value_counts()
#     last_column = category
#     # last_column = dataset.columns[-1]
#     number = dataset[last_column].value_counts()[value]
#     return number


# def frequency(value, category, dataset):
#     return count(value, category, dataset) / len(dataset.index)


# def complete_entropy(dataset):      #entropia zbioru U (całego)
#     complete_entropy = 0
#     last_column = dataset.columns[-1]
#     for value in dataset[last_column].unique():
#         freq = frequency(value, last_column, dataset)
#         entropy = -freq * np.log(freq)
#         complete_entropy += entropy
#     return complete_entropy


# def category_entropy(category, dataset):
#     cat_entropy = 0
#     cat_id = get_category_id(category, dataset)
#     last_column = dataset.columns[-1]
#     last_id = get_category_id(last_column, dataset)
#     for value in dataset[category].unique():
#         # print("Value : " + value)
#         freq = frequency(value, category, dataset)
#         cat_count = count(value, category, dataset)
#         # print("Cat_count : " + str(cat_count))
#         h = 0
#         for score_value in dataset[last_column].unique():
#             matches = 0
#             for row in range(len(dataset.index)):
#                 if dataset.iat[row, cat_id] == value and dataset.iat[row, last_id] == score_value:
#                     matches += 1
#             # print(score_value + " - matches: " + str(matches))
#             divided_frequency = matches / cat_count
#             if divided_frequency != 0:
#                 h += - divided_frequency * np.log(divided_frequency)
#         cat_entropy += h * freq
#     return cat_entropy


# def inf_gain(category, dataset):
#     return complete_entropy(dataset) - category_entropy(category, dataset)


# print(train_data.iat[2,1])
# print(train_data.columns[-1])

# # Testing inf_gain func:
# print("Complete entropy : ")
# print(complete_entropy(train_data))
# print("Category entropy : ")
# print(category_entropy("x1", train_data))
# print("Inf gain for category entropy : ")
# print(inf_gain("x1", train_data))

# def dsc_inf_gains(dataset):
#     entropies = []
#     columns = get_dataset_columns(dataset)
#     columns.pop()
#     for column in columns:
#         entropies.append([inf_gain(column, dataset), column])
#     entropies.sort(reverse=True)
#     return entropies






