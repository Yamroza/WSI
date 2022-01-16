from turtle import shape
import pandas as pd


def get_dataframe(file_name="./LAB7/wine.data",
                   header_list=["Alcohol", "Malic acid", "Ash",
                                "Alcalinity of ash", "Magnesium", "Total phenols",
                                "Flavanoids", "Nonflavanoid phenols", "Proanthocyanins", 
                                "Color intensity", "Hue", "OD280/OD315 of diluted wines", "Proline"]):
    return pd.read_csv(file_name, names=header_list)

print(shape(get_dataframe()))