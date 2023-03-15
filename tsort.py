from sys import argv
from stack_array import *


class Vertex:
    def __init__(self, key):
        '''Add whatever parameters/attributes are needed'''
        self.key = key
        self.in_deg = 0
        self.adj_vert = []
        self.visited = False


def tsort(vertices):
    '''
    * Performs a topological sort of the specified directed acyclic graph.  The
    * graph is given as a list of vertices where each pair of vertices represents
    * an edge in the graph.  The resulting string return value will be formatted
    * one vertex per line in topologically sorted order.
    *
    * Raises a ValueError if:
    *   - vertices is emtpy with the message "input contains no edges"
    *   - vertices has an odd number of vertices (incomplete pair) with the
    *     message "input contains an odd number of tokens"
    *   - the graph contains a cycle (isn't acyclic) with the message 
    *     "input contains a cycle"'''
    # raise ValueError if the input list has no contents
    if len(vertices) == 0:
        raise ValueError("input contains no edges")
    # raise ValueError if the input list has an odd length (results in one vert w/o pair)
    if len(vertices) % 2 == 1:
        raise ValueError("input contains an odd number of tokens")
    # initialize dictionary as "dict" to hold the list of vertices
    dict = {}
    # loop through input list to add all vert to dict
    for i in range(0, len(vertices)-1, 2):
        # if verts are same, then v1 == v2 and v2 is in v1 adj list, which results in a cycle so raise ValueError
        if vertices[i] == vertices[i+1]:
            raise ValueError("input contains a cycle")
        # check if v1 in already in dictionary
        try:
            dict[vertices[i]]
        # v1 is not in dict, add to dict
        except KeyError:
            dict[vertices[i]] = Vertex(vertices[i])
        # now that v1 is in dict,
        finally:
            # check if v2 is already in dict
            try:
                dict[vertices[i+1]]
            # v2 is not in dict, add to dict
            except KeyError:
                dict[vertices[i+1]] = Vertex(vertices[i+1])
            # now that v2 is in dict, increase in_deg by 1
            finally:
                dict[vertices[i+1]].in_deg += 1
            # now that v1 is in dict, add v2 to adjacency list
            dict[vertices[i]].adj_vert.append(dict[vertices[i+1]])
    # initialize stack to run the tSort
    stack = Stack(10)
    # initialize string to add popped verts to
    sorted_str_lst = []
    # iterate through dictionary
    for key in dict:
        # if vert is its own vert_adj list, raise ValueError because it is a cycle
        if dict[key] in dict[key].adj_vert:
            raise ValueError("input contains a cycle")
        # add to stack the verts with an in_deg of 0
        if dict[key].in_deg == 0:
            stack.push(dict[key])
    # iterate through stack
    while not stack.is_empty():
        # get the vert on top of the stack
        v = stack.pop()
        # loop through the vert's adj_list
        for vert in v.adj_vert:
            # decrease in_deg of each vert in the vert's adj_list
            dict[vert.key].in_deg -= 1
            # if the vert who's in_deg just decreased == 0, the immediately push onto stack
            if dict[vert.key].in_deg == 0:
                stack.push(vert)
            # raise ValueError if the in_deg is negative
            elif dict[vert.key].in_deg < 0:
                raise ValueError("input contains a cycle")
        # ensure the vert is not already in ordered list and ensure it has not yet been visited
        if v.visited is False:
            # append the popped vert to the return list (will turn into string at the end to save time)
            sorted_str_lst.append(v.key + "\n")
            # set visited to True so vert will not be visited again
            v.visited = True
        # if the key was already in the list, then there was a loop so raise ValueError
        else:
            raise ValueError("input contains a cycle")
        dict.pop(v.key)
    if len(dict) > 0:
        raise ValueError("input contains a cycle")
    return_str = "".join(map(str, sorted_str_lst))
    # return the string of the verts in order
    return return_str


# 100% Code coverage NOT required
def main():
    '''Entry point for the tsort utility allowing the user to specify
       a file containing the edge of the DAG.  Use this code 
       if you want to run tests on a file with a list of edges'''
    if len(argv) != 2:
        print("Usage: python3 tsort.py <filename>")
        exit()
    try:
        f = open(argv[1], 'r')
    except FileNotFoundError as e:
        print(argv[1], 'could not be found or opened')
        exit()

    vertices = []
    for line in f:
        vertices += line.split()

    try:
        result = tsort(vertices)
        print(result)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
