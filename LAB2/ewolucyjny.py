# ALGORYTM EWOLUCYJNY:
# - bez krzyżowania             +
# - z selekcją turniejową       +
# - z sukcesją generacyjną      +

# Schemat algorytmu:
# populacja bazowa ->                                                                                   +
# selekcja (turniejowa) -> wszystkie osobniki przechodzą, 2n turnijów                                   +
# mutacja -> nie każdy przechodzi, nie wszystkie wartości                                               +
#            prawdopodobieństwo zajścia pewne, losuje se ze 2 miasta i zamienia miejscami np            +
# sukcesja -> populacja po kombinacjach staje się populacją bazową                                      +

# Sugerowane rozkłady miast sztuk 30:               +
# jednorodny (taka szachownica)                     +
# duże skupiska grup                                +
# losowy                                            +
# Wskaż sekwencję tych miast. (najkrótszy cykl)     +

#  W raporcie należałoby wskazać
# jak zmiana liczby osobników w populacji wpływa na jakość uzyskanych rozwiązań przy ograniczonym budżecie. Warto
# również opisać zachowanie algorytmu dla różnych rodzajów danych wejściowych oraz wpływ zmiany parametrów. Przykładowe
# zbiory danych i/lub ich generatory należy samemu skonstruować na potrzebę zadania.

import math
import matplotlib.pyplot as plt
import numpy as np
from random import randint
from random import randrange
from random import sample
from random import choice


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


def generate_group_cities(neighbour_rad):       # 30 cities from definition
    main_cities = generate_random_cities(5)
    cities = []
    for city in main_cities:
        temporary_cities = []
        while len(temporary_cities) < 6:
            x = randint(city[0]-neighbour_rad, city[0]+neighbour_rad)
            y = randint(city[1]-neighbour_rad, city[1]+neighbour_rad)
            if [x,y] not in temporary_cities:
                temporary_cities.append([x,y])
        for city in temporary_cities:
            cities.append(city)
    return cities


def summary_distance(city_list):
    mode_city_list = city_list.copy()
    mode_city_list.append(mode_city_list[0])
    distance_sum = 0
    for i in range(len(mode_city_list)-1):
        distance_sum += distance(mode_city_list[i], mode_city_list[i+1])
    return distance_sum


def generate_population(members_quantity, city_list):
    population = []
    while len(population) < members_quantity:
        next_city = sample(city_list, len(city_list))
        if next_city not in population:
            population.append(next_city)
    return population


def turnee_select(population, func):
    new_population = []
    for i in range(len(population)):
        first_challenger = choice(population)
        second_challenger = choice(population)
        if func(first_challenger) >= func(second_challenger):
            new_population.append(second_challenger)
        else:
            new_population.append(first_challenger)
    return new_population


def modify_element(modify_list):
    if len(modify_list) > 0:
        first = randint(0, len(modify_list)-2)
        # second = randint(0, len(modify_list)-1)
        second = first + 1
        temp = modify_list[first]
        modify_list[first] = modify_list[second]
        modify_list[second] = temp
    return modify_list


def modify_population(population, mod_rate):
    number_to_be_modified = int(mod_rate * len(population))
    population_copy = population.copy()
    modified_elements = []
    while len(modified_elements) < number_to_be_modified:
        ele = choice(population_copy)
        population_copy.remove(ele)
        modified_elements.append(modify_element(ele))
    population_copy += modified_elements
    return population_copy


def turnee_winner_selection(comp_list, func):
    winner = comp_list[0]
    for i in range(len(comp_list)):
        if func(winner) >= func(comp_list[i]):
            winner = comp_list[i]
    return winner


def salesman_problem(cities_list, population_number, iterations, mod_rate):
    population = generate_population(population_number, cities_list)
    i = 0
    while i < iterations:
        new_temp_population = turnee_select(population, summary_distance)
        newer_temp_population = modify_population(new_temp_population, mod_rate)
        population = newer_temp_population.copy()
        i += 1
    winner = turnee_winner_selection(population, summary_distance)
    return winner

def draw(winner):
    for i in range(0, len(winner)-1):
        plt.plot([winner[i][0], winner[i+1][0]], [winner[i][1], winner[i+1][1]], 'ro-')
    plt.plot([winner[-1][0], winner[0][0]], [winner[-1][1], winner[0][1]], 'ro-')
    plt.title("Salesman route", fontsize=19)
    plt.xlabel("Iks", fontsize=10)
    plt.ylabel("Igrek", fontsize=10)
    plt.tick_params(axis='both', which='major', labelsize=9)
    plt.show()

random_cities = generate_chess_cities(7)
random_cities = [[15, 55], [20, 70], [65, 55], [95, 10], [20, 5], [95, 45], [10, 45]]
# random_cities = [[35, 85], [100, 35], [0, 65], [95, 10], [100, 50], [85, 25], [85, 95], [35, 95], [20, 45], [55, 45]]
print("Random cities: ", random_cities)
winner = salesman_problem(random_cities, 5000, 5000, 0)
print("Best route: ", winner )
draw(winner)
