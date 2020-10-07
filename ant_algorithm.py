from random import randint, seed, choice, uniform
import math
import copy


class Ant:
    def __init__(self, start_place, number_of_cities):
        self.start_place = start_place
        self.current_place = self.start_place
        self.number_of_cities = number_of_cities
        self.visited_places = []
        self.pheromone_matrix = [[0]*self.number_of_cities for _ in range(self.number_of_cities)]

    def select_next_place(self, phrmns, distances):
        temp_pheromones = copy.deepcopy(phrmns)
        not_visited_places = [i for i in range(self.number_of_cities) if i not in self.visited_places]
        q_0 = 0.25
        q = uniform(0, 1)
        if q <= q_0:
            J = [temp_pheromones[self.current_place][i] ** 1 * distances[self.current_place][i]**6 if i in not_visited_places else 0 for i in range(self.number_of_cities)]
            self.next_place = J.index(max(J))
        else:   
            self.options = temp_pheromones[self.current_place]
            for i in range(len(self.options)):
                if i in self.visited_places:
                    self.options[i] = 0
            self.next_place = temp_pheromones[self.current_place].index(max(self.options))
        self.visited_places.append(self.next_place)
        self.current_place = self.next_place
    
    def sum_path(self, distances):
        sum = 0
        for i in range(1, len(self.visited_places)):
            prev, now = self.visited_places[i-1], self.visited_places[i]
            if prev < now:
                sum += distances[prev][now]
            elif prev > now:
                sum += distances[now][prev]
        return sum
    
    def pheromone_update(self, Q, matrix_distance):
        delta_tau = Q / self.sum_path(matrix_distance)
        for i in range(1, len(self.visited_places)):
            prev, now = self.visited_places[i-1], self.visited_places[i]
            self.pheromone_matrix[now][prev] = delta_tau
            self.pheromone_matrix[prev][now] = self.pheromone_matrix[now][prev]
        return self.pheromone_matrix

    
    def clear_pheromones(self):
        self.pheromone_matrix = [[0]*self.number_of_cities for _ in range(self.number_of_cities)]

    
def find_distance(first, second):
    X1, X2 = first[0], second[0]
    Y1, Y2 = first[1], second[1]
    if Y1 == Y2:
        return math.fabs(X2-X1)
    elif X1 == X2:
        return math.fabs(Y2-Y1)
    else:
        return math.sqrt((X2-X1)**2 + (Y2-Y1)**2)

def matrix_distance(nodes):
    count = len(nodes.keys())
    i, j = 0, 0
    distance_matrix = [[0]*count for i in range(count)]
    for key1 in nodes.keys():
        for key2 in nodes.keys():
            distance_matrix[i][j] = find_distance(nodes[key1], nodes[key2])
            j+=1
        i+=1
        j=0
    return distance_matrix

def update_pheromones(ants, pheromones, ro=0.4):
    for i in range(len(pheromones)):
        for j in range(i, len(pheromones[0])):
            pheromones[i][j] = pheromones[i][j] * (1 - ro) + sum(ant.pheromone_matrix[i][j] for ant in ants)
            pheromones[j][i] = pheromones[i][j]

def update_probabilities(ants, 
                         distances, number_of_cities, pheromones, probabilities,
                         alpha=1, beta=6):

    for i in range(number_of_cities):
        for j in range(i, number_of_cities):
            if i != j:
                probabilities[i][j] = (pheromones[i][j] ** alpha) / (distances[i][j] ** beta)
                
                probabilities[i][j] /= sum((pheromones[l][k] ** alpha) / (distances[l][k] ** beta) if k != l else 0
                                            for k in range(number_of_cities) for l in range(k, number_of_cities))
                probabilities[j][i] = probabilities[i][j]

def find_shortest_path(nodes, alpha, beta, Q, ro):
    
    number_of_cities = len(list(nodes.keys()))
    distances = matrix_distance(nodes)   
    pheromones = [[1 for j in range(number_of_cities)] for i in range(number_of_cities)]


    probabilities = [[0] * number_of_cities for _ in range(number_of_cities)]
    update_probabilities([], distances, number_of_cities, pheromones, probabilities)

    number_of_ants = number_of_cities
    ants = [Ant(i, number_of_cities) for i in range(number_of_ants)]
    all_paths = dict()
    t = 0
    while t < 200:
        for ant in ants:
            ant.visited_places.append(ant.start_place)
            for city in range(number_of_cities-1):
                ant.select_next_place(probabilities, distances)
            ant.visited_places.append(ant.start_place)
            ant.current_place = ant.start_place
            ant.pheromone_update(100, distances)
            all_paths[ant.sum_path(distances)] = ant.visited_places
            print(ant.visited_places, ant.sum_path(distances))
        if len([ant for ant in ants if ant.sum_path(distances) == min(all_paths.keys())]) == number_of_ants:
            min_distance = min(all_paths.keys())
            break
        update_pheromones(ants, pheromones)
        update_probabilities(ants, distances,number_of_cities, pheromones, probabilities)

        for ant in ants:
            ant.visited_places = []
            ant.clear_pheromones()
        
        t+=1
    nodes_keys = list(nodes.keys())
    network = []
    min_distance = min(all_paths.keys())
    for i in range(number_of_cities + 1):
        network.append(nodes_keys[all_paths[min_distance][i]])
    print(network, min(all_paths.keys()))
    return network



        


