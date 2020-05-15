from random import randrange
from collections import deque

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME
        user_comb = []
        avg = num_users * avg_friendships // 2

        # Add users	
        for i in range(0, num_users):
            self.add_user(f"User {i}")

        # Create friendships
        while len(user_comb) < avg:
            friend1 = randrange(1, num_users)
            friend2 = randrange(1, num_users)
            while friend1 == friend2 or (friend1, friend2) in user_comb or (friend2, friend1) in user_comb:
                friend1 = randrange(1, num_users)
                friend2 = randrange(1, num_users)
            user_comb.append((friend1, friend2))


            for i in user_comb:
                self.add_friendship(i[0], i[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        # pass the user id tot he visited dictionary
        visited = {}  # Note that this is a dictionary, not a set
        # # !!!! IMPLEMENT ME

        # Add all edges of given vertex to queue
        if self.friendships[user_id]:
            for i in range(1, self.last_id + 1):
                visited[i] = self.bfs(user_id, i)

            return visited
        else:
            return 'No friends'

    def bfs(self, starting_vert, target_vert):
        queue = deque()
        visited = set()
        queue.append([starting_vert])
        while queue:
            # dequeue a list from queue
            dequeued_list = queue.popleft()
            path_end = dequeued_list[-1]
            # mark it as visited
            if path_end not in visited:
                # check if target vert == last item in list
                if path_end == target_vert:
                    return dequeued_list
                visited.add(path_end)
                # enqueue all of it's children
                for vert in self.friendships[path_end]:
                    path_copy = list(dequeued_list)
                    path_copy.append(vert)
                    queue.append(path_copy)


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
