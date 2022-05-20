# Used for reading command line arguments
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
from itertools import cycle
import sys
import getopt

import json

import numpy as np
import random

train_size = 10000
valid_size = 2000
graph_max = 64
output_path = '../data/cycle_data.json'

# Variable for data analysis
cycles_count = 0


# Generates a tuple (x_array, y_node_num)

def checkCycle(current_node, node_list, matrix, visited, parent):
    visited[current_node] = True
    for node in node_list:
        if (matrix[current_node][node] == 1):
            if visited[node] == False:
                if (checkCycle(node, node_list, matrix, visited, current_node) == True):
                    return True

            elif parent != current_node:
                return True
    
    return False

def generate_graph():
    global graph_max
    global cycles_count

    graph_size = random.randrange(graph_max)
    graph_nodes = random.choices(range(graph_max), k=graph_size)

    max_edges = int(graph_size*(graph_size-1)/2)

    if (max_edges == 0):
        edges_num = 0
    else:
        edges_num = random.randrange(max_edges)

    adj_matrix = np.zeros((graph_max, graph_max))
    for n in range(edges_num):
        (x, y) = random.choices(graph_nodes, k=2)
        # check if edge is already filled
        if (x != y):
            adj_matrix[x, y] = 1
            adj_matrix[y, x] = 1

    # cycle checking algorithm
    # https://www.geeksforgeeks.org/detect-cycle-undirected-graph/
    has_cycle = 0
    visited = [False] * (graph_max)
    for i in graph_nodes:
        if visited[i] == False:
            if (checkCycle(i, graph_nodes, adj_matrix, visited, -1) == True):
                has_cycle = 1
                break

    cycles_count += has_cycle

    # numpy arrays are not supported by json
    return (adj_matrix.tolist(), has_cycle)


def parse_CLI(argv):
    global train_size
    global valid_size
    global graph_max
    global output_path

    try:
        opts, args = getopt.getopt(argv, "ho:v:t:g:")
    except getopt.GetoptError:
        print('Error with arguments, try running with -h')
        sys.exit()

    for opt, arg in opts:

        print(opt, arg)

        if opt == '-h':
            print('-h: Print help message')
            print('-o: Set output File Path')
            print(f'-t: Set training data size (Default {train_size})')
            print(f'-v: Set validation data size (Default {valid_size})')
            print(f'-g: Set graph maximum size (Default {graph_max})')
            sys.exit()

        elif opt == '-o':
            output_path = arg

        elif opt == '-v':
            try:
                valid_size = int(arg)
            except ValueError:
                print('Validation Data size must be integer')
                sys.exit()
            if (valid_size <= 0):
                print('Validation Data size must be positive')
                sys.exit()

        elif opt == '-t':
            try:
                train_size = int(arg)
            except ValueError:
                print('Training Data size must be integer')
                sys.exit()
            if (train_size <= 0):
                print('Training Data size must be positive')
                sys.exit()

        elif opt == '-g':
            try:
                graph_max = int(arg)
            except ValueError:
                print('Graph size must be integer')
                sys.exit()
            if (graph_max <= 0):
                print('Graph size must be positive')
                sys.exit()


if __name__ == "__main__":
    parse_CLI(sys.argv[1:])
    with open(output_path, 'w') as f:
        # initialize json object
        data_object = {
            'x_train': [],
            'y_train': [],
            'x_valid': [],
            'y_valid': []
        }

        cycles_count = 0

        for i in range(train_size):
            if ((i+1) % 1000 == 0):
                print(f'{i+1}-th training output done')

            (arr, num) = generate_graph()
            data_object['x_train'].append(arr)
            data_object['y_train'].append(num)
        
        print(f'Graphs with cycle: {cycles_count}/{train_size}')

        cycles_count = 0

        for j in range(valid_size):
            if ((j+1) % 1000 == 0):
                print(f'{(j+1)}-th validation output done')

            (arr, num) = generate_graph()
            data_object['x_valid'].append(arr)
            data_object['y_valid'].append(num)

        print(f'Graphs with cycle: {cycles_count}/{valid_size}')

        # output json
        print(f'Writing to {output_path}...')
        f.write(json.dumps(data_object))
        f.close()
