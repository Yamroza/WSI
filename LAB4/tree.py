from dataset import Dataset


class AllNode:

    def __init__(self, dataset, category = None, kids = None, parent_value = None):
        self.dataset = dataset
        self.category = category 
        self.kids = kids
        self.parent_value = parent_value
        if self.kids:
            self.is_leaf = False
        else:
            self.is_leaf = True
            self.prediction = self.count_prediction()


    def count_prediction(self):
        best_values = [] 
        best_freq = 0 
        last_column = self.dataset.dataset.columns[-1]
        for value in self.dataset.dataset[last_column].unique():
            if self.dataset.frequency(value, last_column) > best_freq:
                best_freq = self.dataset.frequency(value, last_column)
                best_values = [value]
            elif self.dataset.frequency(value, last_column) == best_freq:
                best_values.append(value)
            
        if len(best_values) == 1:
            return best_values[0]
        else:
            return best_values


class Tree:
    
    def __init__(self, data, value = None):
        self.dataset = data
        self.value = value
        self.tree = self._build_tree()
        

    def _build_tree(self):
        if len(self.dataset.dataset.columns) == 1:
            return AllNode(self.dataset, None, None, self.value)
        entropy = self.dataset.best_inf_gains()
        best_entropy = entropy[0]
        if best_entropy == 0:
            return AllNode(self.dataset, None, None, self.value)
        best_category = entropy[1]
        mini_datasets, values = self.dataset.split_by_category_plus(best_category)
        kids = []
        for mini_dataset, value in zip(mini_datasets, values):
            kid = Tree(Dataset(mini_dataset), value)
            kids.append(kid)
        return AllNode(self.dataset, best_category, kids, self.value)


    def predict(self, row):
        if self.tree.is_leaf:
            return self.tree.prediction
        
        if len(self.tree.kids) == 0:
            return self._build_tree().prediction

        for kid in self.tree.kids:  
            if kid.tree.is_leaf:
                id = self.dataset.get_category_id(self.tree.category)
                if kid.value == row[id]:
                    return kid.tree.prediction
            else: 
                category = self.tree.category
                id = self.dataset.get_category_id(category)
                if kid.value == row[id]:
                    del row[id]
                    return kid.predict(row)
                                     # jezeli taka wartosc nie wystapila:
        category = self.tree.category
        best_freq = 0
        best_value = None
        for value in self.dataset.dataset[category].unique():
            if self.dataset.frequency(value, category) > best_freq:
                best_freq = self.dataset.frequency(value, category)
                best_value = value
        row[id] = best_value
        return self.predict(row)
        

