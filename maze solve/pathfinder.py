from PIL import Image
import math

maze_path = "maze solve//maze.png"
size = 1

colors_dict = {
    "wall" : (0, 0, 0),
    "path1" : (255, 255, 255),
    "path2" : (217, 217, 217),
    "start" : (0, 252, 80),
    "goal" : (250, 42, 42)
}

color_numbers = {
    "wall" : -1,
    "path" : 0,
    "start" : -2,
    "goal" : -3
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
            elif a == -2:
                color = colors_dict["start"]
            elif a == -3:
                color = colors_dict["goal"]
            elif a == -1:
                color = colors_dict["wall"]

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

def Decrypt():
    raw_image = Image.open(maze_path)

    image_width, image_height = raw_image.size

    data = [
        [NearestColor(raw_image.getpixel((x, y))) for x in range(image_width)] for y in range(image_height)
    ]

    return data

if __name__ == "__main__":
    j = Decrypt()
    ReadData(j)