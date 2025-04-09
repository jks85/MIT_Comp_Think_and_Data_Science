# 6.0002 Problem Set 2
# Graph optimization
# Name: jks85
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer: Nodes represent campus buildings while edge weights
# represent distances (total and outdoor).


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        1.Each entry in the map file consists of the following four positive
          integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
          e.g.
            32 76 54 23
          This entry would become an edge from 32 to 76.
        2. Last line in text file is *BLANK*

    Returns:
        a Digraph representing the map
    """

    print("Loading map from file...")
    with open(map_filename, 'r') as file:
        map_file = file.read()
    # split by carriage returns
    map_list = map_file.split('\n')

    print(map_list)
    # initialize list to hold nodes and edge info
    map_info = []

    # loop over list of strings and grab path values (nodes, edge weights)
    # cast edge weights to ints
    for vals in map_list:
        curr_vals = vals.split(' ')
        for i in range(2, len(curr_vals)):
            curr_vals[i] = int(curr_vals[i])
        map_info.append(curr_vals)
    map_info = map_info[:-1]   # remove last element which is blank

    # create graph from map info list
    graph = Digraph() # empty graph

    # list to hold node names
    mit_nodes = []

    # loop over map_info
    for edge in map_info:
        # create temp source and destination nodes
        temp_src = Node(edge[0])
        temp_dest = Node(edge[1])
        # add nodes to graph if missing
        if temp_src not in graph.nodes:
            graph.add_node(temp_src)
        if temp_dest not in graph.nodes:
            graph.add_node(temp_dest)
        # create edge and add to graph
        temp_edge = WeightedEdge(temp_src,temp_dest,edge[2],edge[3])
        graph.add_edge(temp_edge)

    # return graph
    return graph



# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out

#### TESTING load_map()

# # create graph
# test_graph = load_map('test_load_map.txt')


#
# Problem 3: Finding the Shortest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
# The objective function is the distance traveled, which we wish to minimize.
# The constraint is the maximum time spent outdoors.

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """


    ## helper function that computes *total* distance of edges in a path
    ## graph path is a list of node names (strings)
    def compute_path_dist(graph_path):
        path_length = 0               # initialize path length

        # loop over path members to compute edge weight
        for i in range(len(graph_path)-1):
            temp_src = Node(graph_path[i])    # create source node
            temp_dest = Node(graph_path[i+1]) # create dest node
            src_edges = digraph.get_edges_for_node(temp_src) # list of edges from source

            # get weight of desired edge & update path length
            for edge in src_edges:
                if edge.get_destination() == temp_dest:
                    path_length += edge.get_total_distance()
                    break

        return path_length

    # helper to compute outdoor path dist
    # note this assumes that nodes are connected by an edge...
    # path is a list of node names (strings)
    def compute_path_out_dist(graph_path):
        path_outdoor_length = 0                 # initialize path length

        # loop over path members to compute edge weight
        for i in range(len(graph_path)-1):
            temp_src = Node(graph_path[i])    # create source node
            temp_dest = Node(graph_path[i+1]) # create dest node
            src_edges = digraph.get_edges_for_node(temp_src) # list of edges from source

            # check if edge exists
            dests = [edge.get_destination() for edge in src_edges]
            if temp_dest not in dests:
                print('edge',temp_src,'->',temp_dest,'does not exist')
                #raise ValueError('Edge does not exist')


            # get weight of desired edge & update path length
            for edge in src_edges:
                if edge.get_destination() == temp_dest:
                    path_outdoor_length += edge.get_outdoor_distance()
                    break

        return path_outdoor_length


    # create temp nodes for start and end
    temp_start = Node(start)
    temp_end = Node(end)


    # validate start/end nodes
    if not (digraph.has_node(temp_start) and digraph.has_node(temp_end)):
        raise ValueError('Node(s) not in graph')



    # check if end node has been reached
    if temp_start == temp_end:
        print('solution found! updating...')
        new_dist = compute_path_dist(path) # compute current path length
        #new_path = path

        # compare to global solution and update variables
        if best_dist == float('inf') or new_dist < best_dist:
            best_dist = compute_path_dist(path)
            best_path = path
            print('local solution is better. best path:', best_path,', best dist:', best_dist)

        return best_path,best_dist

        # update total dist traveled
        # return tuple containing path as strings and total distance

    else:
        print('end not node found: continuing...')
        # loop over children of start node
        start_edges = digraph.get_edges_for_node(temp_start)  # list of edges from start node
        # print children
        start_children = []         # container for child nodes
        for edge in start_edges:
            start_children.append(edge.get_destination()) # add current children to a list
        test = [x.get_name() for x in start_children]
        print('printing children of node',temp_start,test)

        # loop over children and explore paths
        for child in start_children:
            # construct paths from start node
            temp_path = path[:] # copy initial path
            print('creating temp path:',temp_path)
            if temp_start.get_name() not in temp_path:
                temp_path.append(temp_start.get_name()) # add start node if missing
            if child.get_name() not in temp_path:
                temp_path.append(child.get_name())      # add child node if not in path (checks for cycles)

                # explore subtree from child node (if appropriate)
                temp_path_out_dist = compute_path_out_dist(temp_path)
                temp_path_dist =  compute_path_dist(temp_path)
                print('temp path',temp_path,'total outdoor path dist',temp_path_out_dist)
                # if temp path meets outdoor constraint
                if temp_path_out_dist <= max_dist_outdoors:
                    #if temp path is possibly optimal
                    if best_path == [] or temp_path_dist < best_dist:
                        print('recursive call...')
                        pot_sol = get_best_path(digraph,temp_path[-1],end,
                                                temp_path,max_dist_outdoors, best_dist, best_path)

                        if pot_sol != None:
                            if temp_path_dist < best_dist:
                                best_path,best_dist = pot_sol
                    else:
                        print('path not viable. skipping...')



    if best_path == []:
        return None
    else:
        return best_path,best_dist



# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    inf = float('inf') # create infinity for initial best distance
    initial_path = []
    best_dist = inf
    best_path = []

    best_solution = get_best_path(digraph, start, end, initial_path, max_dist_outdoors, best_dist, best_path)

    # check if no solution or best path is too long
    if best_solution == None or best_solution[1] > max_total_dist:
        raise ValueError('No solution found')
    else:
        best_path = best_solution[0]
        return best_path


# testing get_best_path() and directed_dfs()

mit_graph = load_map("mit_map.txt")
test_load_graph = load_map("test_load_map.txt")
#print(directed_dfs(mit_graph, 32, 56,100,100))
# print(directed_dfs(test_load_graph, 1, 2,100,100))
#print(get_best_path(test_load_graph, 1, 4, [], 100, float('inf'),[]))
print(get_best_path(mit_graph, 36, 24, [], 0, float('inf'),[]))


# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()
