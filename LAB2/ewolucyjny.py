import math
import matplotlib.pyplot as plt
from random import randint
from random import randrange
from random import sample
from random import choice
import timeit


# generating lists of cities
def generate_random_cities(city_number):
    cities = []
    while len(cities) < city_number:
        x = randint(0, 101)
        y = randint(0, 101)
        if [x,y] not in cities:
            cities.append([x,y])
    return cities


def generate_chess_cities(city_number, distance):
    cities = []
    while len(cities) < city_number:
        x = randrange(0, 101, distance)
        y = randrange(0, 101, distance)
        if [x,y] not in cities:
            cities.append([x,y])
    return cities


def generate_group_cities(groups, elements, neighbour_rad):       # 30 cities from definition
    main_cities = generate_random_cities(groups)
    cities = []
    for city in main_cities:
        temporary_cities = []
        while len(temporary_cities) < elements:
            x = randint(city[0]-neighbour_rad, city[0]+neighbour_rad)
            y = randint(city[1]-neighbour_rad, city[1]+neighbour_rad)
            if [x,y] not in temporary_cities:
                temporary_cities.append([x,y])
        for city in temporary_cities:
            cities.append(city)
    return cities


# distance between two chosen cities
def distance(city_1, city_2):
    return math.sqrt((city_1[0] - city_2[0])**2 + (city_1[1] - city_2[1])**2)


# summary distance between next cities from list
def summary_distance(city_list):
    mode_city_list = city_list.copy()
    mode_city_list.append(mode_city_list[0])
    distance_sum = 0
    for i in range(len(mode_city_list)-1):
        distance_sum += distance(mode_city_list[i], mode_city_list[i+1])
    return distance_sum


# population generation based on city list
def generate_population(members_number, city_list):
    population = []
    end = members_number
    while len(population) < end:
        next_city = sample(city_list, len(city_list))
        if next_city not in population:
            population.append(next_city)
    return population


# tourney selection
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


# modification of one element
def modify_element(modify_list):
    if len(modify_list) > 0:
        first = randint(0, len(modify_list)-2)
        # second = randint(0, len(modify_list)-1)
        second = first + 1
        temp = modify_list[first]
        modify_list[first] = modify_list[second]
        modify_list[second] = temp
    return modify_list


# population modification
def modify_population(population, mod_rate):
    number_to_be_modified = int(mod_rate * len(population))
    population_copy = population.copy()
    modified_elements = []
    while len(modified_elements) < number_to_be_modified:
        ele = choice(population_copy)
        modified_elements.append(modify_element(ele))
        population_copy.remove(ele)
    population_copy += modified_elements
    return population_copy


# selection of final winner
def turnee_winner_selection(comp_list, func):
    winner = comp_list[0]
    for i in range(len(comp_list)):
        if func(winner) >= func(comp_list[i]):
            winner = comp_list[i]
    return winner


# final algorithm composition
def salesman_problem(cities_list, population_number, iterations, mod_rate):
    population = generate_population(population_number, cities_list)
    i = 0
    while i < iterations:
        new_temp_population = turnee_select(population, summary_distance)
        population = modify_population(new_temp_population, mod_rate)
        i += 1
    winner = turnee_winner_selection(population, summary_distance)
    return winner


# drawing a plot of cities
def draw(winner):
    for i in range(0, len(winner)-1):
        plt.plot([winner[i][0], winner[i+1][0]], [winner[i][1], winner[i+1][1]], 'ro-')
    plt.plot([winner[-1][0], winner[0][0]], [winner[-1][1], winner[0][1]], 'ro-')
    plt.xlabel("Iks", fontsize=10)
    plt.ylabel("Igrek", fontsize=10)
    plt.tick_params(axis='both', which='major', labelsize=9)
    plt.show()


# times:
def route_time(cities_list, population_number, iterations, mod_rate):
    return timeit.Timer(lambda: (salesman_problem(cities_list, population_number, iterations, mod_rate))).timeit(number=1)


# TESTY:
CITY_NUMBER = 30
CITY_LIST = generate_random_cities(7)
POPULATION_NUMBER = 100
ITERATIONS = 50
MOD_RATE = 0.1

plt.title("Salesman route\n Exec. time: %f s, population: %d,\niterations: %d, mutate ratio = %f" % (route_time(CITY_LIST, POPULATION_NUMBER, ITERATIONS, MOD_RATE), POPULATION_NUMBER, ITERATIONS, MOD_RATE ))
print("City list: ", CITY_LIST)
route = salesman_problem(CITY_LIST, POPULATION_NUMBER, ITERATIONS, MOD_RATE)
print("Best route: ", route)
draw(route)
