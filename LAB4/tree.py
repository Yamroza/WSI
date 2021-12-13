from dataset import Dataset

class AllNode:
    def __init__(self, dataset, is_leaf, category = None, kids = None, parent_value = None):

        self.dataset = dataset
        self.category = category 
        self.kids = kids
        self.parent_value = parent_value
        if self.kids:
            self.is_leaf = False
        else:
            self.is_leaf = True
            self.prediction = self.count_prediction()

    def get_category(self):
        return self.category

    def get_kids(self):
        return self.kids

    def show(self):
        if self.is_leaf:
            print("-----> ", self.prediction)
        else:
            if self.parent_value:
                print(self.parent_value)
            print("\nKategoria: ", self.category)
            for kid in self.kids:
                print(self.category, end=" ")
                kid.show()

    def save(self, file):
        if self.is_leaf:
            data = open(file, 'a')
            line = ("-----> " + self.prediction)
            data.write(line)
        else:
            data = open(file, 'a')
            if self.parent_value:
                line = (" " + self.parent_value)
                data.write(line)
            line2 = ("\nKategoria: " + self.category)
            data.write(line2)

            for kid in self.kids:
                line = (self.category + " ")
                data.write(line)
                kid.save(file)

        
    def count_prediction(self):
        best_values = [] 
        best_freq = 0 
        last_column = self.dataset.last_column()
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
        if len(self.dataset.get_dataset_columns()) == 1:
            return AllNode(self.dataset, True, None, None, self.value)
        entropies = self.dataset.dsc_inf_gains()
        best_ent_tuple = entropies[0]
        best_entropy = best_ent_tuple[0]
        if best_entropy == 0:
            return AllNode(self.dataset, True, None, None, self.value)
        best_category = best_ent_tuple[1]
        mini_datasets, values = self.dataset.split_by_category_plus(best_category)
        kids = []
        for mini_dataset, value in zip(mini_datasets, values):
            kid = Tree(Dataset(mini_dataset), value)
            kids.append(kid)
        return AllNode(self.dataset, False, best_category, kids, self.value)

    def show(self):
        if self.value:
            print(" - Wartosc : ", self.value, end="")
        self.tree.show()

    def save(self, file):
        if self.value:
            data = open(file, 'a')
            line = (" - Wartosc : " + self.value)
            data.write(line)
        self.tree.save(file)


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
                # print("\n\ncategory: ", category)
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
        

