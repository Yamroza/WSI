import pandas as pd
import statistics
import math

# return pandas dataset with classes as a last column
def get_dataframe(file_name="./LAB7/wine.data",
                   header_list=["Wine class", "Alcohol", "Malic acid", "Ash",
                                "Alcalinity of ash", "Magnesium", "Total phenols",
                                "Flavanoids", "Nonflavanoid phenols", "Proanthocyanins", 
                                "Color intensity", "Hue", "OD280/OD315 of diluted wines", "Proline"]):
                    
                                
    dataframe = pd.read_csv(file_name, names=header_list)
    cols = dataframe.columns.tolist()
    cols = cols[1:] + cols[:1]
    return dataframe[cols]


def separate_by_class(dataset):
    separated = dict()
    for i in range(len(dataset.index)):
        vector = dataset.loc[i, :].values.tolist()
        class_value = vector[-1]
        if (class_value not in separated):
            separated[class_value] = list()
        separated[class_value].append(vector)
    return separated


def average_value(num_list):
    return statistics.mean(num_list)

def stdev(num_list):
    return statistics.stdev(num_list)

def stats_for_column(column):
    return [average_value(column), stdev(column), len(column)]


def stats_for_dataset(dataset):
    stats_for_dataset = []
    for column in dataset.columns.tolist():
        stats_for_dataset.append(stats_for_column(dataset[column].tolist()))
    del(stats_for_dataset[-1])
    return stats_for_dataset


def stats_for_classes(dataset):
    separated = separate_by_class(dataset)
    summaries = dict()
    for class_value, rows in separated.items():
        summaries[class_value] = stats_for_dataset(pd.DataFrame.from_records(rows))
    return summaries


def gauss_func(x, average, stdev):
    return 1/math.sqrt(2*math.pi*stdev**2) * math.e**(-(x - average)**2/(2*stdev**2))


def predicted_probabilities(stats, row):
    rows = sum([stats[label][0][2] for label in stats])
    probabilities = dict()
    for class_value, class_summaries in stats.items():
        probabilities[class_value] = stats[class_value][0][2]/float(rows)
        for i in range(len(class_summaries)):
            mean, stdev, count = class_summaries[i]
            probabilities[class_value] *= gauss_func(row[i], mean, stdev)
    return probabilities


def main():
    my_dataframe = get_dataframe()
    classes_stats = stats_for_classes(my_dataframe)

    vector = my_dataframe.loc[3, :].values.tolist()
    print(vector)
    del(vector[-1])
    predicted = predicted_probabilities(classes_stats, vector)
    print(predicted)


if __name__ == "__main__":
    main()