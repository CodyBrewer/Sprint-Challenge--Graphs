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
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


# graph keep track of visited rooms
"""
{
    room_id: { exit_directions }
}
"""
visited = {}

# (current_room, last_direction_traveled)
stack = [(player.current_room, None)]

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def get_opposite(direction):
    if direction == 'n':
        return 's'
    if direction == 's':
        return 'n'
    if direction == 'w':
        return 'e'
    if direction == 'e':
        return 'w'

# loop while the stack is not empty
while len(stack) > 0:

    # current room is first position of the last item in the stack
    current_room = stack[-1][0]
    # direction traveled is second position of last item on stack
    direction_traveled = stack[-1][1]
    
    if current_room.id not in visited: # if the current room is not visited
        # initialize a set
        visited[current_room.id] = set()
    
    if direction_traveled: # if the direction traveled exists
        # add that direction to the room set
        visited[current_room.id].add(direction_traveled)
    
    if len(visited) == len(room_graph): # if the number of rooms visited equals the number of rooms in the room graph
        break  # break the loop
    
    # get a list of exits not traveled
    exits = [ e for e in current_room.get_exits() if e not in visited[current_room.id]]
    # if there are exits to choose from pick a random one
    random_direction = random.choice(exits) if len(exits) > 0 else None
    # get the opposite of the random direction
    opposite_direction = get_opposite(random_direction)

    if random_direction != None: # if there is a direction available
        # add that direction to the room set
        visited[current_room.id].add(random_direction)
        # put the next room in the stack with the direction traveled from
        stack.append((current_room.get_room_in_direction(random_direction), opposite_direction))
        # add the direction to the traversal path
        traversal_path.append(random_direction)
    else: # if no directions are available
        # add the direction to the traversal path
        traversal_path.append(direction_traveled)
        # take the previous room off the stack
        stack.pop()


# TRAVERSAL TEST - DO NOT MODIFY
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
