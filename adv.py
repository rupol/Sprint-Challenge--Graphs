from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def explore(player):
    # create an empty set to track visited rooms
    visited = set()

    # store previous directions (in case we need to back track)
    backtrack_path = []

    # while all the rooms are not yet explored
    while len(visited) < len(world.rooms):
        # current is the room object we are currently in
        current = player.current_room

        # unexplored directions from current room
        current_exits = current.get_exits()
        unexplored = [direction for direction in current_exits if current.get_room_in_direction(
            direction) not in visited]

        # mark current room as visited
        visited.add(current)

        # if there are unexplored rooms, pick a random direction and explore
        if unexplored:
            direction = unexplored[random.randint(
                0, len(unexplored)-1)]
            player.travel(direction)
            backtrack_path.append(direction)
            traversal_path.append(direction)

        # otherwise, we're at a dead end, back track
        else:
            # get the last direction we went in
            last_direction = backtrack_path.pop(-1)
            # reverse the last direction to go back
            reverse_direction = {'s': 'n', 'n': 's', 'w': 'e', 'e': 'w'}
            player.travel(reverse_direction[last_direction])
            traversal_path.append(reverse_direction[last_direction])

    return traversal_path


traversal_path = explore(player)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
