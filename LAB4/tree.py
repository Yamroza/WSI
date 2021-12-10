import math
from regression import *

class Node:
    """Contains the information of the node and another nodes of the Decision Tree."""

    def __init__(self, value, parent = None, kids = None, is_leaf = False):
        
        self._value = value         # string podobno
        self._kids = kids           # Nodes
        self._parent = parent       # Node
        self._is_leaf = is_leaf     # boolean

        def set_value(self, value):
            self._value = value  
        
        def get_value(self):
            return self._value 

        def set_parent(self, parent):
            self._parent = parent  
        
        def get_parent(self):
            return self._parent 

        def set_kids(self, kids):
            self._kids = kids  
        
        def get_kids(self):
            return self._kids  
        
        def set_is_leaf(self, iss):
            self._is_leaf = iss  
        
        def get_is_leaf(self):
            return self._is_leaf  
        

class TreeClassifier:

    def __init__(self, dataset):

        self._data = dataset
        self._root = None 
        self._column_numbers = [i for i in range (len(dataset.colums))]
        # self.X = X  # features or predictors

        # self.feature_names = feature_names  # name of the features

        # self.labels = labels  # categories

        # self.labelCategories = list(set(labels))  # unique categories

        # # number of instances of each category
        # self.labelCategoriesCount = [list(labels).count(x) for x in self.labelCategories]
        
        # self.node = None  # nodes
        
        # # calculate the initial entropy of the system
        # self.entropy = self._get_entropy([x for x in range(len(self.labels))])
        

dataset = train_data = pd.read_csv('test.csv')
columns = [i for i in range (len(dataset.columns))]
print(columns)