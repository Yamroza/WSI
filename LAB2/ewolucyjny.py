# ALGORYTM EWOLUCYJNY:
# - bez krzyżowania
# - z selekcją turniejową
# - z sukcesją generacyjną

# Sugerowane rozkłady miast sztuk 30:
# jednorodny (taka szachownica)
# duże skupiska grup
# losowy
# Wskaż sekwencję tych miast. (najkrótszy cykl)

#  W raporcie należałoby wskazać
# jak zmiana liczby osobników w populacji wpływa na jakość uzyskanych rozwiązań przy ograniczonym budżecie. Warto
# również opisać zachowanie algorytmu dla różnych rodzajów danych wejściowych oraz wpływ zmiany parametrów. Przykładowe
# zbiory danych i/lub ich generatory należy samemu skonstruować na potrzebę zadania.

import math
from random import randint
from random import randrange

CITY_QUANTITY = 30


def distance(city_1, city_2):
    return math.sqrt((city_1[0] - city_2[0])**2 + (city_1[1] - city_2[1])**2)


def generate_random_cities(city_quantity):
    cities = []
    while len(cities) < city_quantity:
        x = randint(0, 101)
        y = randint(0, 101)
        if [x,y] not in cities:
            cities.append([x,y])
    return cities


def generate_chess_cities(city_quantity):
    cities = []
    while len(cities) < city_quantity:
        x = randrange(0, 101, 5)
        y = randrange(0, 101, 5)
        if [x,y] not in cities:
            cities.append([x,y])
    return cities


def generate_group_cities(city_quantity):
    cities = []
    while len(cities) < city_quantity:
        x = randint(0, 101)
        y = randint(0, 101)
        if [x,y] not in cities:
            cities.append([x,y])
    return cities


# def make_city_list(city_list):
#     city_list.append(city_list[0])
#     return city_list


def summary_distance(city_list):
    # city_list = make_city_list(city_list)
    city_list.append(city_list[0])
    distance_sum = 0
    for i in range(len(city_list)-1):
        distance_sum += distance(city_list[i], city_list[i+1])
    return distance_sum
