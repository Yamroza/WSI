from tree import Tree
from dataset import Dataset
import pandas as pd 


def i3(train_data, test_data):
    tree = Tree(Dataset(train_data))
    test_rows = test_data.values.tolist()
    predictions = []
    for row in test_rows:
        pr = tree.predict(row)
        predictions.append(pr)
    return predictions

# TP - True positive: dobrze wyszlo
# TN - True Negative: dobrze wyszło 
# FP - False Positive: wyszło że jest tą klasą a nią nie jest
# FN - False Negative: jest tą klasą a pokazało że nią nie jest

# Recall = FP / (FP + TN)
# Fall-out = FP / (FP + TN)
# Precision = TP / (TP + FP)
# Accuracy = (TP + TN) / (TP + TN + FP + FN)
# F1 score = (2 * Recall * Precision) / (Recall + Precision)


def metrics_vector(train_data, test_data):
    predictions = i3(train_data, test_data)
    real_values = test_data[test_data.columns[-1]].values
    t_p = 0
    f_p = 0
    t_n = 0
    f_n = test_data.shape[0]
    for score_value in test_data[test_data.columns[-1]].unique():
        for prediction, real_value in zip(predictions, real_values):
            if prediction == score_value and real_value != score_value:
                f_p += 1
            if real_value == score_value and prediction != score_value:
                f_n += 1 
            if real_value == score_value and prediction == score_value:
                t_p += 1
    f_n = f_n - t_p - t_n - f_p
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


def main():
    dataset = pd.read_csv('nursery.csv')
    train_data = dataset.iloc[:12000, :]
    test_data = dataset.iloc[12000:, :]
    
    # t_p, f_p, t_n, f_n = true_positive(train_data, test_data)
    metrics =  metrics_vector(train_data, test_data)
    print("recall = ", metrics[0])
    print("fall_out = ", metrics[1])
    print("precion = ", metrics[2])
    print("accuracy = ", metrics[3])
    print("f1_score = ", metrics[4], "\n")
    # print("TP: ", t_p)
    # print("FP: ", f_p)
    # print("TN: ", t_n)
    # print("FN: ", f_n)
    # print("suma: " , t_p +f_p+ t_n+ f_n )

    print(dataset_matrix(train_data, test_data))

    # draw_matrix(train_data, test_data)

if __name__ == "__main__":
    main()

