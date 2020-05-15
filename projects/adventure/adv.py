from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# create a queue class to traverse the graph so I can apply FIFO to use bft
class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# initialise graph with a dictionary containing all direction marked with question marks
graph = {0: {"n": "?", "e": "?", "s": "?", "w": "?"}}

# instantiate a dictionary to go the opposite direction when there are no other exit available
inverse_directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

# this will be a set containing dictionaries of all previously explored rooms 
# available exits
room_unvisited_exits = list()

# use breath first approach to find shortest path
def change_direction(starting_room_id):
    # count = 0
    # if room_unvisited_exits and count / 2 == 0:
    #     ran_num = random.randint(0, len(room_unvisited_exits) - 1)
    #     random_index = random.randint(0, ran_num)
    #     unexplored_route = room_unvisited_exits[random_index]
    #     room_unvisited_exits.pop(random_index)
    #     current_room_id = unexplored_route[0]
    #     [room_exit] = random.sample(unexplored_route[1], 1)

    #     if graph[current_room_id][room_exit] == '?':

    #         count += random.randint(1, 100000000000000000)
    #         # if so return the path yet to be visited
    #         return [current_room_id]
    # else:
        # instantiate a queue
        q = Queue() 
        # place in the queue the starting room
        q.enqueue([starting_room_id])
        # initialise a set for the visited
        visited_rooms = set() 
        # while there are entrie in the queue
        while q.size() > 0:
            # dequeu the first path
            path = q.dequeue()
            # grab the last vertex(current room id) within the path
            current_room_id = path[-1]

            # if the current room is not in the visited set
            if current_room_id not in visited_rooms:
                # iterate over each exit in the current room
                for room_exit in graph[current_room_id]:
                    # check if the current room exit is still unvisited
                    if graph[current_room_id][room_exit] == '?':
                        # count += random.randint(1, 1000)
                        # if so return the path yet to be visited
                        return path
                # else add current room to the visited
                visited_rooms.add(current_room_id)
                # iterate over the each exit in the current room
                for exit_direction in graph[current_room_id]:
                    # create a new copy of the path
                    new_path = list(path)
                    # append the current room and the exit 
                    new_path.append(graph[current_room_id][exit_direction])
                    # pass it to the queue of paths
                    q.enqueue(new_path)

        # once the queue is empty, return none as the graph as been traversed
        return None 

while True:
    # grab current room id
    current_room_id = player.current_room.id
    # get all current room exits values
    current_room_exits = graph[current_room_id] 

    # initialise a list of all unvisited exits
    unvisited_exits = []

    # iterate over each direction in the list of exits
    for direction in current_room_exits:
        # and if the current direction is not been visited
        if current_room_exits[direction] == '?':
            # add it to the unvisited list 
            unvisited_exits.append(direction)

    # if there are elements in the unvisited list
    if len(unvisited_exits) > 0:

        # choose a random direction to take
        [chosenExit] = random.sample(unvisited_exits, 1)

        #############################
        current_room_exits = list()
        # save in set the remaining directions with the room id as key
        for room_exit in unvisited_exits:
            if room_exit is not chosenExit:
                current_room_exits.append(room_exit)
        
        if current_room_exits:
            room_unvisited_exits.append((current_room_id, tuple(current_room_exits)))
        #############################

        # add the chosen direction to the traveral path list
        traversal_path.append(chosenExit)
        # save the previous room id in case of needing to go back when no other exits are found
        prev_room_id = player.current_room.id

        # move the player in the chosen direction
        # this will change the current room
        player.travel(chosenExit)

        # now that we are in a new room
        # set the initial state of the room using a dictionary to pass all exits
        current_room_exits = {}

        # if the current room is not in the graph
        if player.current_room.id not in graph:
            # iterate over each exit within the room 
            for room_exit in player.current_room.get_exits():
                # and set those to the newly created dictionary
                current_room_exits[room_exit] = '?'
            # pass the current room to the graph with all its exits
            graph[player.current_room.id] = current_room_exits

        # set the previous room chosen direction to the current room
        graph[prev_room_id][chosenExit] =  player.current_room.id

        # and connect the current room in the same direction with the previous room
        graph[player.current_room.id][inverse_directions[chosenExit]] = prev_room_id
    else: 
        # if the player reaches a room with no unvisited exits
        # then change direction until a room with available exits is found
        unvisited_directions = change_direction(player.current_room.id)
        # if there are no unvisited then get out of the while loop
        if unvisited_directions is None:
            break

        # set the current room the very first vertex within the path
        current_room = unvisited_directions[0]
        # initialise a direction list
        directions = [] 

        # for each room within the unvisited list excluding the first room
        for room in unvisited_directions[1:]:
            # iterate over each room exit in the current room
            for room_exit in graph[current_room]:
                # if the room id within the path is equal to the current room id at exit 
                if room == graph[current_room][room_exit]: 
                    # then pass it to the directions list
                    directions.append(room_exit) 

        # iterate over each direction within the direction list
        for direction in directions:
            # move the player in that direction
            player.travel(direction)
            # add the direction taken to the traversal path list
            traversal_path.append(direction) 

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
