from PIL import Image
import random as rnd
import math
import string
import time

#this is setting
maze_width = 20
maze_height = 20
size = 30
invert = False

start_point = (0, 0)
goal = (100, 100)

colors_dict = {
    "wall" : (0, 0, 0),
    "path1" : (255, 255, 255),
    "path2" : (217, 217, 217),
    "start" : (0, 252, 80),
    "goal" : (250, 42, 42)
}

#this is for debugging the hole
# debug_tag = {
#     2 : (255, 117, 107),#red
#     3 : (255, 253, 107),#yellow
#     4 : (113, 252, 106),#green
#     5 : (106, 252, 247)#blue
# }
def clamp(value, minimum, maximum): return min(maximum, max(minimum, value))

def ReadData(data):
    raw_maze = Image.new('RGBA', (len(data[0]) * size, len(data) * size))

    #turn numeral data to picture
    for y in range(len(data) * size):
        for x in range(len(data[0]) * size):
            mazeX = x // size
            mazeY = y // size
            a = data[mazeY][mazeX]

            if a == 1:
                color = colors_dict["path1" if (mazeX % 2 == 0) == (mazeY % 2 == 0) else "path2"]
            elif a == -1:
                color = colors_dict["start"]
            elif a == -2:
                color = colors_dict["goal"]
            else:
                color = colors_dict["wall"]

            raw_maze.putpixel((x, y), color)

    raw_maze.save('Generate//Image maze.png')

def Encrypt(data):
    raw_maze = Image.new('RGBA', (len(data[0]), len(data)))

    for y in range(len(data)):
        for x in range(len(data[0])):
            a = data[y][x]

            if a == 1:
                color = colors_dict["path1"]
            elif a == -1:
                color = colors_dict["start"]
            elif a == -2:
                color = colors_dict["goal"]
            else:
                color = colors_dict["wall"]

            raw_maze.putpixel((x, y), color)

    raw_maze.save('Generate//Encrypt maze.png')

def DivideRoom(data):
    rooms = [(0, 0, maze_width - 1, maze_height - 1)]

    while len(rooms) != 0:
    # for k in range(1):
        currentRoom = rooms[0]

        #select only 75% in the center to make it look good but if too small select 100%
        length_x = currentRoom[2] - currentRoom[0] + 1
        length_y = currentRoom[3] - currentRoom[1] + 1

        space_x = range(math.floor(length_x * 1 / 8) + currentRoom[0], max(1, currentRoom[2] - math.floor(length_x * 1 / 8)))
        space_y = range(math.floor(length_y * 1 / 8) + currentRoom[1], max(1, currentRoom[3] - math.floor(length_y * 1 / 8)))
        
        #check if room is too slim
        if len(space_x) == 0 or len(space_y) == 0:
            rooms.remove(currentRoom)
            continue
        
        #random the position of wall
        random_x = rnd.choice(space_x)
        random_y = rnd.choice(space_y)

        wall_x = random_x * 2 + 2
        wall_y = random_y * 2 + 2

        #draw the wall
        for n in range(currentRoom[1] * 2 + 1, (currentRoom[3] + 1) * 2 + 1):
            data[n][wall_x] = int(invert)

        for n in range(currentRoom[0] * 2 + 1, (currentRoom[2] + 1) * 2 + 1):
            data[wall_y][n] = int(invert)

        #make three hole in the three walls
        #there are 4 walls but we only want 3 holed walls
        abandoned_wall = rnd.randint(0, 3)
        if abandoned_wall != 0:
            data[rnd.randint(currentRoom[1], random_y) * 2 + 1][wall_x] = int(not invert)

        if abandoned_wall != 1:
            data[wall_y][rnd.randint(currentRoom[0], random_x) * 2 + 1] = int(not invert)

        if abandoned_wall != 2:
            data[rnd.randint(random_y + 1, currentRoom[3]) * 2 + 1][wall_x] = int(not invert)

        if abandoned_wall != 3:
            data[wall_y][rnd.randint(random_x + 1, currentRoom[2]) * 2 + 1] = int(not invert)

        #divide room into 4 regions, Q represent quadrants like in graph
        #Q2|Q1
        #-----
        #Q3|Q4
        #Q1
        q = (random_x + 1, currentRoom[1], currentRoom[2], random_y)
        if q[0] != q[2] and q[1] != q[3]:
            rooms.append(q)
        #Q2
        q = (currentRoom[0], currentRoom[1], random_x, random_y)
        if q[0] != q[2] and q[1] != q[3]:
            rooms.append(q)
        #Q3
        q = (currentRoom[0], random_y + 1, random_x, currentRoom[3])
        if q[0] != q[2] and q[1] != q[3]:
            rooms.append(q)
        #Q4
        q = (random_x + 1, random_y + 1, currentRoom[2], currentRoom[3])
        if q[0] != q[2] and q[1] != q[3]:
            rooms.append(q)

        #removing current rooms
        rooms.remove(currentRoom)

    return data

if __name__ == "__main__":
    start_time = time.time()

    #use seed
    seed = ''.join(rnd.choice(string.ascii_letters) for n in range(25))

    dungeon = []

    dungeon.append([int(invert)] * (2 * maze_width + 1))
    for i in range(2 * maze_height - 1):
        dungeon.append([int(invert)] + [int(not invert)] * (2 * maze_width - 1) + [int(invert)])
    dungeon.append([int(invert)] * (2 * maze_width + 1))


    rnd.seed(seed)
    dungeon = DivideRoom(dungeon)

    dungeon[clamp(start_point[1], 0, maze_height - 1) * 2 + 1][clamp(start_point[0], 0, maze_width - 1) * 2 + 1] = -1
    dungeon[clamp(goal[1], 0, maze_height - 1) * 2 + 1][clamp(goal[0], 0, maze_width - 1) * 2 + 1] = -2

    ReadData(dungeon)

    Encrypt(dungeon)

    print(seed)
    print(f'time use : {round(time.time() - start_time, 3)} seconds')