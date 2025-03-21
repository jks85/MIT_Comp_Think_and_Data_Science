###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: jks85
# Collaborators:
# Time:
from numpy.distutils.misc_util import green_text

from ps1_partition import get_partitions
import time
import os

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    # open and read text file
    with open(filename, 'r') as file:
        values = file.read() # get lines from text file

    # create name & weight dict. name/weight are separated by commas
    values = values.split('\n') # remove '\n' character and create list
    name_weight_list = [string.split(',') for string in values] # split name and weight
    name_weight_dict = {name:int(weight) for [name,weight] in name_weight_list} # create dict

    return name_weight_dict


# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    # create sorted dict
    dict_copy = cows.copy() # copy dict
    weight_sorted = sorted(dict_copy.items(), key=lambda x: x[1], reverse=True) # sort dict by weight
    cows_dict_sorted = {name: dict_copy[name] for name, weight in weight_sorted} # sorted dict. not needed?

    # create empty master list to contain all transport sub-lists
    master_list =[]

    # iterate over dict copy and add heaviest cow as long as there is room
    # delete item from dict after it is added
    while len(cows_dict_sorted) > 0:
        transp_list = [] # list for cows transported on this trip
        capacity = limit
        for name,weight in cows_dict_sorted.items(): # iterate over dictionary
            if weight <= capacity:
                transp_list.append(name) # add heaviest cows that fit to transport list
                capacity -= weight # reduce max capcity by cow weight
        master_list.append(transp_list)  # add transport list to master list
        for name in transp_list:
            del cows_dict_sorted[name]   # remove cows in transport list from dictionary




    return master_list

# test greedy_cow_transport

# cows1_file = 'ps1_cow_data.txt' # create file path
# cows_dict = load_cows(cows1_file) # create cows dict
# print(cows_dict)
# print(greedy_cow_transport(cows_dict, 9))
# print(greedy_cow_transport(cows_dict, 10))
# print(greedy_cow_transport(cows_dict, 12))


# for max_wt in [8, 10, 13]:
#     print(greedy_cow_transport(cows_dict,max_wt))

#
# cows3_file = 'ps1_cow_data_3.txt'
# cows_dict3 = load_cows(cows3_file)
# print(greedy_cow_transport(cows_dict3))

# Problem 3

# helper function to check cow weights for problem 3
def get_list_weight(names_list, cow_dict) -> int:
    '''
    Takes a list of cow names and a name/weight dictionary.
    Returns total weight of  cows in the list.
    :param names_list: list of cow names
    :param cow_dict:  dict containing cow name:weight as key:value pairs
    :return: integer representing total weight of cows in list
    '''

    weight_list = [cow_dict[name] for name in names_list]  # weights of cows in list of names
    return sum(weight_list)


def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    
    valid_list = [] # list to contain valid transports options
    optimal_list = [] # list to contain optimal transport solutions
    all_partitions = get_partitions(list(cows.keys())) # list of all possible cow partitions
    min_trips = len(cows.keys()) # initialize number of trips to max-- each cow taken separately

    valid_partition = None  # set variable to track validity of partition to false

    # iterate over all partitions, which are lists of lists
    for partition in all_partitions:

        num_trips = len(partition) # set current number of trips

        for trip in partition: # iterate over subpartitions
            valid_partition = False  # set variable to track validity of partition to false
            trip_weight = get_list_weight(trip,cows)
            if trip_weight > limit: # check if total weight of partition above max
                break
            else:
                valid_partition = True

        if valid_partition:
            if num_trips <= min_trips: # check if num trips less than or equal to current min
                #optimal_list.append((partition,num_trips))# add partition to optimal list
                valid_list.append((partition,num_trips))
                min_trips = num_trips   # adjust min # of trips

    # note once loop ends 'min_trips' contains the minimum # of trips for valid solutions
    #print('min # of trips:',min_trips)

    for partition,num_trip in valid_list:   # iterate over valid solutions and get min values
        if num_trip == min_trips:
            optimal_list.append(partition)

    return optimal_list





# ######################
# testing 3rd file  that i made using 4 cows from original file. cows/weights below
# {'Jesse': 6, 'Maybel': 3, 'Callie': 2, 'Maggie': 5}

# cows3_file = 'ps1_cow_data_3.txt'
# cows_dict3 = load_cows(cows3_file)

# print('Cow names3 dict:')
# print(list(cows_dict3.keys()))
# cow_names3 = list(cows_dict3.keys())
# # print('Cow names3 partitions:')
# # print(list(get_partitions(cow_names3)))
# # print('num Cow names3 partitions:')
# # print(len(list(get_partitions(cow_names3))))
# print('cows names3: ',cow_names3)
# print(' ')
# print('greedy solution:')
# print(greedy_cow_transport(cows_dict3)) # greedy algo solution
# print(' ')
# print('brute force solution(s):')
# print(brute_force_cow_transport(cows_dict3))



# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """

    cows1_file = 'ps1_cow_data.txt'  # create file path
    cows_dict = load_cows(cows1_file)  # create cows dict

    greedy_start = time.time()
    greedy_sol = greedy_cow_transport(cows_dict)
    greedy_end = time.time()
    greedy_time = greedy_end - greedy_start

    brute_start = time.time()
    brute_sol = brute_force_cow_transport(cows_dict)
    brute_end = time.time()
    brute_time = brute_end - brute_start

    print('greedy min: ', len(greedy_sol),'trips, ', 'greedy time: ',greedy_time,' seconds')
    print('brute min: ', len(brute_sol[0]),'trips, ', 'brute time: ', brute_time, ' seconds')

    # greedy algorithm returns a single optimal solution
    # brute algorithm returns a list of optimal solutions. size of first solution is extracted

compare_cow_transport_algorithms()
compare_cow_transport_algorithms()
compare_cow_transport_algorithms()
compare_cow_transport_algorithms()