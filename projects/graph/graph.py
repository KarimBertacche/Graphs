"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        # pass to the dictionary of vertices a set with the vertex id as key
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        # check if both v1 & v2 are in the vertices dictionary
        if v1 in self.vertices and v2 in self.vertices:
            # if so to vertices at key vertex1 add vertex 2 creating an edge, connection between the two vertexes
            self.vertices[v1].add(v2)
        else:
            # if not throw an error message
            raise IndexError("Vertex does not exist!")

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        # return the set of connections/edges that the vertex has to others neighbour
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # create a queue instance
        q = Queue()
        # add to the queue the starting vertex
        q.enqueue(starting_vertex_id)
        # instantiate a visited set to avoid duplicates and better performance
        visited = set()
        # while the queue is not empty
        while q.size() > 0:
            # dequeue the first vertex
            v = q.dequeue()
            # if that vertex has not been visited
            if v not in visited:
                # mark it as visited by passing it to the set of visited vertex
                visited.add(v)
                # iterate over each neighbour of the current vertex
                for next_vertex in self.get_neighbors(v):
                    # and pass those to the queue 
                    q.enqueue(next_vertex)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # create a new stack instance
        s = Stack()
        # add to the stack the starting vertex
        s.push(starting_vertex_id)
        # instantiate a visited set to avoid duplicates and better performance
        visited = set()
        # while the stack is not empty
        while s.size() > 0:
            # remove the last added vertex
            v = s.pop()
            # if that vertex has not been visited
            if v not in visited:
                # mark it as visited by passing it to the set of visited vertex
                visited.add(v)
                # iterate over each neighbour of the current vertex
                for next_vertex in self.get_neighbors(v):
                    # and pass those to the queue 
                    s.push(next_vertex)

    def dft_recursive(self, starting_vertex, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        # on the next invokation, starts from scratch with an empty set has python holds a reference of the previously filled set otherwise
        if visited is None:
            # instantiate a visited using set to avoid duplicates and shorten run time
            visited = set()
            
        # check if the starting vertex(node) is already in the visited set
        if starting_vertex not in visited:
            # if not pass it to the visited set
            visited.add(starting_vertex)
            # iterate over each neighbour vertex to the starting one
            for neighbor in self.get_neighbors(starting_vertex):
                # and call dft_recursive on each neighbour
                self.dft_recursive(neighbor, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # instantiate a queue
        q = Queue()
        # pass the starting index inside the queue using a list so we can hold the path for each vertex
        q.enqueue([ starting_vertex ])
        # instantiate a visited set
        visited = set()
        # while there are paths in the queue keep iterating 
        while q.size() > 0:
            # grab the first path and store it in a path variable
            path = q.dequeue()
            # grab the current vertex from the end(last index) of the path 
            v = path[-1]
            # check if the current vertex is in the visited set
            if v not in visited:
                # if not pass it to the visited set
                visited.add(v)
                # check if the vertex matches the destination vertex
                if v == destination_vertex:
                    # if they match, return the path
                    return path
                # else move to the neighbour of the current vertex and repeat the process until match is found
                for neighbour in self.get_neighbors(v):
                    # pass to the queue a new instance of the path + neighbour
                    # the asterix is the same as the spread operator in js
                    # is called splat and is an alternative to the copy method
                    q.enqueue([*path, neighbour])

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        # instantiate a stack
        s = Stack()
        # pass the starting index inside the stack using a list so we can hold the path for each vertex
        s.push([ starting_vertex ])
        # instantiate a visited set
        visited = set()
        # while there are paths in the stack keep iterating 
        while s.size() > 0:
            # grab the last inserted path and store it in a path variable
            path = s.pop()
            # grab the current vertex from the end(last index) of the path 
            v = path[-1]
            # check if the current vertex is in the visited set
            if v not in visited:
                # if not pass it to the visited set
                visited.add(v)
                # check if the vertex matches the destination vertex
                if v == destination_vertex:
                    # if they match, return the path
                    return path
                # else move to the neighbour of the current vertex and repeat the process until match is found
                for neighbour in self.get_neighbors(v):
                    # pass to the stack a new instance of the path + neighbour
                    # the asterix is the same as the spread operator in js
                    # is called splat and is an alternative to the copy method
                    s.push([*path, neighbour])

    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        pass  # TODO

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
