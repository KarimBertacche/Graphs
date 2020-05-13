# use the Queue class to solve this problem with a breath first approach
class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, vertex):
        self.queue.append(vertex)

    def dequeue(self):
        # if there are vertexes in the queue
        if self.size() > 0:
            # remove the first one and return it
            return self.queue.pop(0)
        else:
            # else return none
            return None
        
    def size(self):
        # return the length of the queue
        return len(self.queue)

# generate a graph
class Graph:
    def __init__(self):
        # instantiate a vertices dictionary
        self.vertices = {}

    def add_vertex(self, vertex_id):
        # if the current vertex is not in the vertices dict
        if vertex_id not in self.vertices:
            # when adding a vertex, pass as value to the vertices dict a set at the vertex index
            self.vertices[vertex_id] = set()

    def add_edges(self, v1, v2):
        # use directed edges as the relationship is parent child vertices
        if v1 in self.vertices and v2 in self.vertices:
            # create the connection between the child vertex and parent
            self.vertices[v1].add(v2)



def earliest_ancestor(ancestors, starting_node):
    # BUILD THE GRAPH
    # create an instance of the graph class
    graph = Graph()
    
    # iterate over the ancestors
    for vertex_pairs in ancestors:
        # assign the parent vertex to a variable
        parent = vertex_pairs[0]
        # assign the child to a variable
        child = vertex_pairs[1]
        # and for both parent and child nodes add them to the vertices dictionary
        graph.add_vertex(child)
        graph.add_vertex(parent)
        # then connect child to ancestor(parent) vertex
        graph.add_edges(child, parent)

    # USE BFS TO TRAVERSE GRAPH
    # create a new instance of a queue
    q = Queue()
    # pass to the queue the starting node as a path
    q.enqueue([ starting_node ])

    # declare a variable which will hold the longest path
    len_longest_path = 1
    # and assign as the earliest ancestor a negative 1 for cases when there are no ancestors
    earliest_ancestor = -1

    # while the queue is not empty
    while q.size() > 0:
        # we can dequeue the next path
        path = q.dequeue()
        # then we can grab the current vertex which will be the last node in the list
        current_vertex = path[-1]

        # in case the length is equal and if the earliest ancestors is greater than the current vertex
        if len(path) >= len_longest_path and earliest_ancestor > current_vertex:
                # set the path as the longest path
                len_longest_path = len(path)
                # and if so change them
                earliest_ancestor = current_vertex
        # check if the current path length is greater then the currently held longest path
        elif len(path) > len_longest_path:
            # than we want to set that as the longest path
            len_longest_path = len(path)
            # and the earliest ancestor as the current vertex
            earliest_ancestor = current_vertex
        

        # assign the neighbour vertexes from the vertices dict on the current vertex index
        neighbours = graph.vertices[current_vertex]
        # then iterate over each ancestor in the neighbours set
        for ancestor in neighbours:
            # copy the path
            path_copy = list(path)
            # append to the path the ancestor
            path_copy.append(ancestor)
            # and then enqueue the newly updated path
            q.enqueue(path_copy)

    # return the earliest ancestor
    return earliest_ancestor