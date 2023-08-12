from PIL import Image
import math

maze_path = "maze solve//Encrypt maze.png"
size = 1

colors_dict = {
    "wall" : (0, 0, 0),
    "path1" : (255, 255, 255),
    "path2" : (217, 217, 217),
    "start" : (0, 252, 80),
    "goal" : (250, 42, 42),
    "trace" : (22, 250, 174)
}

color_numbers = {
    "goal" : -2,
    "wall" : -1,
    "path" : 0,
    "start" : 1
}

def ReadData(data):
    raw_maze = Image.new('RGBA', (len(data[0]) * size, len(data) * size))

    #turn numeral data to picture
    for y in range(len(data) * size):
        for x in range(len(data[0]) * size):
            mazeX = x // size
            mazeY = y // size
            a = data[mazeY][mazeX]

            if a == 0:
                color = colors_dict["path1" if (mazeX % 2 == 0) == (mazeY % 2 == 0) else "path2"]
            elif a == 1:
                color = colors_dict["trace"]
            elif a == -1:
                color = colors_dict["wall"]
            elif a == -2:
                color = colors_dict["goal"]

            raw_maze.putpixel((x, y), color)

    raw_maze.save('maze solve//Solved maze.png')

def NearestColor(color):

    def calc(color_1, color_2):
        distance = math.pow(math.pow(color_2[0] - color_1[0], 2) + 
                            math.pow(color_2[1] - color_1[1], 2) + 
                            math.pow(color_2[2] - color_1[2], 2), 1/2)

        opposite_color = (255 - color_1[0], 255 - color_1[1], 255 - color_1[2])

        max_distance = math.pow(math.pow(opposite_color[0] - color_1[0], 2) + 
                            math.pow(opposite_color[1] - color_1[1], 2) + 
                            math.pow(opposite_color[2] - color_1[2], 2), 1/2)
        
        return 1 - distance / max_distance
    
    color_comparison = {
        "wall" : (0, 0, 0),
        "path" : (255, 255, 255),
        "start" : (0, 255, 0),
        "goal" : (255, 0, 0)
    }

    score = [(calc(color, value), name) for name, value in color_comparison.items()]

    score.sort(reverse=True)

    return color_numbers[score[0][1]]

def Enigma():
    raw_image = Image.open(maze_path)

    image_width, image_height = raw_image.size

    data = [
        [NearestColor(raw_image.getpixel((x, y))) for x in range(image_width)] for y in range(image_height)
    ]

    return data

def Bombe(data):
    #open node
    nodes = []

    weight_map = [
        [0 for i in data[0]] for i in data
    ]

    #find start point
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[x][y] == 1:
                weight_map[y][x] = 1    
                nodes.append((x, y))
                break

    
    #djiskr algorithm
    last_node = -1
    while nodes:
        current_node = nodes[0]
        node_value = weight_map[current_node[1]][current_node[0]]

        surrounded_node = [
            (x + current_node[0], y + current_node[1]) 
            for x in range(-1, 2) for y in range(-1, 2) 
            if (x == 0 or y == 0) and not (x == 0 and y == 0)
        ]

        for each in surrounded_node:
            if weight_map[each[1]][each[0]] == 0 and data[each[1]][each[0]] == 0:
                weight_map[each[1]][each[0]] = node_value + 1
                nodes.append(each)

            elif data[each[1]][each[0]] == -2:
                weight_map[each[1]][each[0]] = node_value + 1
                last_node = each
                break

        nodes.remove(current_node)

    #backstracking
    current_node = last_node
    while weight_map[current_node[1]][current_node[0]] != 1 and last_node != -1:
        data[current_node[1]][current_node[0]] = 1
        value = weight_map[current_node[1]][current_node[0]]
        
        surrounded_node = [
            (x + current_node[0], y + current_node[1]) 
            for x in range(-1, 2) for y in range(-1, 2) 
            if (x == 0 or y == 0) and not (x == 0 and y == 0)
        ]

        for each in surrounded_node:
            if weight_map[each[1]][each[0]] == value - 1:
                current_node = each
                break
    
    return data

if __name__ == "__main__":
    #turn maze image into 2d array
    engima_code = Enigma()
    ReadData(engima_code)

    #this function will solve the maze
    engima_code = Bombe(engima_code)

    #read maze array and turn them to picture
    ReadData(engima_code)