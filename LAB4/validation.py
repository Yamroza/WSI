from tree import Tree
from dataset import Dataset
import pandas as pd 
import sklearn.model_selection as sc


def i3(train_data, test_data):
    tree = Tree(Dataset(train_data))
    test_rows = test_data.values.tolist()
    predictions = []
    for row in test_rows:
        pr = tree.predict(row)
        predictions.append(pr)
    return predictions


def metrics_vector(train_data, test_data):
    predictions = i3(train_data, test_data)
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

    return [recall, fall_out, precision, accuracy, f1_score]


def dataset_matrix(train_data, test_data):
    score_values = train_data[train_data.columns[-1]].unique()
    matrix_dataframe = pd.DataFrame(index=score_values, columns=score_values)
    for score in score_values:
        for score1 in score_values:
            matrix_dataframe.at[score, score1] = 0
    
    predictions = i3(train_data, test_data)
    real_values = test_data[test_data.columns[-1]].values

    for prediction, real_value in zip(predictions, real_values):
        matrix_dataframe.at[prediction, real_value] += 1

    return matrix_dataframe


def cross_validation(dataset, k):
    row_part = dataset.shape[0] // k
    matrix_vectors = []
    for i in range(k):
        test_data = dataset.iloc[i * row_part : (i + 1) * row_part, :]
        train_data_fp = dataset.iloc[:(i * row_part), :]
        train_data_sp = dataset.iloc[ (i + 1) * row_part: , :]
        train_data = pd.concat([train_data_fp, train_data_sp])
        matrix_vectors.append(metrics_vector(train_data, test_data))
    while len(matrix_vectors) > 1:
        matrix_vectors[0] = [matrix_vectors[0][i] + matrix_vectors[1][i] for i in range(len(matrix_vectors[0]))]
        del matrix_vectors[1]
    average_matrix_vector = [value/k for value in matrix_vectors[0]]
    return average_matrix_vector


def cross_validation_matrix(dataset, k):
    row_part = dataset.shape[0] // k
    for i in range(k):
        test_data = dataset.iloc[i * row_part : (i + 1) * row_part, :]
        train_data_fp = dataset.iloc[:(i * row_part), :]
        train_data_sp = dataset.iloc[ (i + 1) * row_part: , :]
        train_data = pd.concat([train_data_fp, train_data_sp])
        print(dataset_matrix(train_data, test_data))

def main():

    # do obserwacji:
    dataset = pd.read_csv('nursery.csv')
    metrics = cross_validation(dataset, 5)
    print("recall = ", metrics[0])
    print("fall_out = ", metrics[1])
    print("precion = ", metrics[2])
    print("accuracy = ", metrics[3])
    print("f1_score = ", metrics[4], "\n")
    train_data, test_data = sc.train_test_split(dataset, test_size = 0.25)
    print(dataset_matrix(train_data, test_data))


if __name__ == "__main__":
    main()

