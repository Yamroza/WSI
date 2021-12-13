from tree import Tree, AllNode
from dataset import Dataset
import pandas as pd 
import numpy as np



# def predict_with_cross_validate(dataset, k):
#     rows = len(dataset.index)
#     part = rows / k
#     for i in range(k):
#         if i = 0:
#         train_dataset = dataset.iloc[,2*i - 1]
#         test_dataset = dataset.iloc[:(i-1), (2*i - i)]
#         df_1 = df.iloc[:1000,:]



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
# Precision = TP / (TP + FP)
# Accuracy = (TP + TN) / (TP + TN + FP + FN)


def true_positive(train_data, test_data):
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
    precistion = t_p / (t_p + f_p)
    accuracy = (t_p + t_n) / ( t_p + t_n + f_n + f_p)

    return t_p, f_p/2, t_n, f_n/2 



def draw_matrix(train_data, test_data):
    score_values = train_data[train_data.columns[-1]].unique()
    # wektor = 
    print("            " , end = "")
    for score_value in score_values:
        print(score_value, end = "  ")
    print("")
    for score_value in score_values:
        print(score_value) #, wektor)


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
    # predictions = i3(train_data, test_data)
    # should_be = test_data[test_data.columns[-1]].values
    # for element, should in zip(predictions, should_be):
    #     if element == should:
    #         print("Wyszlo: " , element , "Powinno: ", should, "   Dobrze")
    #     else:
    #         print("Wyszlo: " , element , "Powinno: ", should, "   ŹLE")


    # t_p, f_p, t_n, f_n = true_positive(train_data, test_data)
    # print("TP: ", t_p)
    # print("FP: ", f_p)
    # print("TN: ", t_n)
    # print("FN: ", f_n)
    # print("suma: " , t_p +f_p+ t_n+ f_n )

    print(dataset_matrix(train_data, test_data))

    # draw_matrix(train_data, test_data)


    # train_data = Dataset(dataset)
    # tree = Tree(train_data)
    # tree.save("drewo.txt")
    # pr = tree.predict(["C",1,"ok","xd"])
    # row = ["usual","proper","complete","1","convenient","convenient","nonprob","recommended", "cos"]
    # pr = tree.predict(['usual', 'proper', 'complete', '2', 'convenient', 'inconv', 'problematic', 'recommended'])
    # pr = tree.predict(row)
    # print(pr)

if __name__ == "__main__":
    main()

