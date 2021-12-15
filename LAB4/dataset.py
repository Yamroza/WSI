import numpy as np


class Dataset:

    def __init__(self, dataset):

        self.dataset = dataset

    def frequency(self, value, category):
        number = self.dataset[category].value_counts()[value]
        return number / len(self.dataset.index)


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
        cat_values = self.dataset[category].unique()
        for cat_value in cat_values:
            work_dataset = Dataset(self.dataset[self.dataset[category] == cat_value])
            cat_entropy += work_dataset.complete_entropy()
        return cat_entropy


    def inf_gain(self, category):
        return self.complete_entropy() - self.category_entropy(category)


    def best_inf_gains(self):
        entropies = []
        columns = [column for column in self.dataset.columns] 
        columns.pop()
        for column in columns:
            entropies.append([self.inf_gain(column), column])
        entropies.sort(reverse=True)
        return entropies[0]


    def split_by_category_plus(self, category):
        mini_categories = []
        values = []
        for value in self.dataset[category].unique():
            values.append(value)
            mini_category = self.dataset[self.dataset[category] == value]
            mini_category.drop(category, axis=1, inplace=True)
            mini_categories.append(mini_category)
        return mini_categories, values


    def get_category_id(self, category):
        columns = self.dataset.columns
        found = False
        id = 0
        while not found:
            if columns[id] == category:
                found = True
            else:
                id += 1
        return id
