import pandas as pd
import statistics
import math
import sklearn.model_selection as sc
from sklearn.utils import shuffle
import seaborn as sn
from matplotlib import pyplot as plt


def get_dataframe(file_name="./LAB7/wine.data",
                   header_list=["Wine class", "Alcohol", "Malic acid", "Ash",
                                "Alcalinity of ash", "Magnesium", "Total phenols",
                                "Flavanoids", "Nonflavanoid phenols", "Proanthocyanins", 
                                "Color intensity", "Hue", "OD280/OD315 of diluted wines", "Proline"]):
                    
                                
    dataframe = pd.read_csv(file_name, names=header_list)
    cols = dataframe.columns.tolist()
    cols = cols[1:] + cols[:1]
    return dataframe[cols]


def split_by_class(dataset):
        mini_datasets = []
        values = []
        classes = dataset.columns.tolist()[-1]
        for value in dataset[classes].unique():
            values.append(value)
            mini_class = dataset[dataset[classes] == value]
            mini_class.drop(classes, axis=1, inplace=True)
            mini_datasets.append(mini_class)
        return mini_datasets, values


def stats_for_column(column):
    return [statistics.mean(column), statistics.stdev(column), len(column)]


def stats_for_dataset(dataset):
    stats_for_dataset = []
    for column in dataset.columns.tolist():
        stats_for_dataset.append(stats_for_column(dataset[column].tolist()))
    return stats_for_dataset


def stats_for_classes(dataset):
    mini_classes, values = split_by_class(dataset)
    classes_stats = []
    for mini_class in mini_classes:
        classes_stats.append(stats_for_dataset(mini_class))
    return classes_stats, values


def gauss_func(x, average, stdev):
    return 1/math.sqrt(2*math.pi*stdev**2) * math.e**(-(x - average)**2/(2*stdev**2))


def predicted_probabilities(stats, row):
    rows = sum([element[0][2] for element in stats])
    probubles = []
    for class_stats in stats:
        probab = class_stats[0][2] / rows
        for i in range (len(class_stats)):
            probab *= gauss_func(row[i], class_stats[i][0], class_stats[i][1])
        probubles.append(probab)
    return probubles


def predict_class(stats, values, row):
    probubles = predicted_probabilities(stats, row)
    class_prob = max(probubles)
    max_index = probubles.index(class_prob)
    return values[max_index]


def predict_dataset(train_data, test_data):
    classes_stats, values = stats_for_classes(train_data)
    predictions = []
    real_values = []
    for index, row in test_data.iterrows():
        chosen_row = row.tolist()
        if len(chosen_row) > 0:
            row_values = chosen_row[:-1]
            real_value = chosen_row[-1]
            predictions.append(predict_class(classes_stats, values, row_values))
            real_values.append(int(real_value))
    return predictions, real_values


def metrics_vector(train_data, test_data):
    predictions, real_values =  predict_dataset(train_data, test_data)
    real_values = test_data[test_data.columns[-1]].values
    t_p, f_p, f_n, t_n  = 0, 0, 0, test_data.shape[0]
    for score_value in test_data[test_data.columns[-1]].unique():
        for prediction, real_value in zip(predictions, real_values):
            if prediction == score_value and real_value != score_value:
                f_p += 1
            if real_value == score_value and prediction != score_value:
                f_n += 1 
            if real_value == score_value and prediction == score_value:
                t_p += 1
    f_p /= 2 
    f_n /= 2 
    t_n = t_n - t_p - f_n - f_p
    recall = f_p / (f_p + t_n)
    fall_out = f_p / (f_p + t_n)
    precision = t_p / (t_p + f_p)
    accuracy = (t_p + t_n) / ( t_p + t_n + f_n + f_p)
    f1_score = (2 * recall * precision) / (recall + precision)
    return [predictions, real_values, recall, fall_out, precision, accuracy, f1_score]

    
def confusion_matrix(predictions, real_values):
    data = {'y_Actual':    real_values,
            'y_Predicted': predictions}
    df = pd.DataFrame(data, columns=['y_Actual','y_Predicted'])
    confusion_matrix = pd.crosstab(df['y_Predicted'], df['y_Actual'], rownames=['Predicted'], colnames=['Actual'])
    sn.heatmap(confusion_matrix, annot=True, cmap='Blues', fmt='g')
    plt.savefig("proba_dobra.png")


def main():
    dataset = get_dataframe()
    dataset = shuffle(dataset)
    train_data, test_data = sc.train_test_split(dataset, test_size = 0.1)
    predictions, real_values = predict_dataset(train_data, test_data)
    confusion_matrix(predictions, real_values)
    print(predictions)
    print(real_values)
    
     # data = open("new_bayes.txt", 'a')
    # rows = dataset.shape[0]
    # for test_size in [0.7, 0.8, 0.9]:
    #     train_data = dataset[int(rows * test_size) :]
    #     test_data = dataset[: int(rows * (1-test_size))]
    #     predictions, real_values, recall, fall_out, precision, accuracy, f1_score = metrics_vector(train_data, test_data)
    #     print(predictions)
    #     print(real_values)
        # line = (f'0;{test_size};{recall};{fall_out};{precision};{accuracy};{f1_score}')
        # line_png = line + ".png"
        # line += "\n"
        # data.write(line)
        # confusion_matrix(predictions, real_values, line_png)
    # data.close()


if __name__ == "__main__":
    main()