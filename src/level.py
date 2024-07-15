import pygame
from sprites.wall import Wall
from sprites.score import Score

def load_level(file_path, wall_group, score_group, tile_size):
    initial_player_x = 18 * tile_size
    initial_player_y = 15 * tile_size

    with open(file_path, 'r') as file:
        level = [list(line.replace("\n", "")) for line in file]

    for y, row in enumerate(level):
        for x, tile in enumerate(row):
            if tile == '1' or tile == '2':
                wall = None
                
                # Determine the dimensions of the level
                max_x = len(level[0]) - 1
                max_y = len(level) - 1
                
                # Set adjacency variables, handling out-of-bounds by defaulting to False
                top = (y > 0) and (level[y - 1][x] == tile)
                bottom = (y < max_y) and (level[y + 1][x] == tile)
                left = (x > 0) and (level[y][x - 1] == tile)
                right = (x < max_x) and (level[y][x + 1] == tile)
                top_right = (y > 0 and x < max_x) and (level[y - 1][x + 1] == tile)
                top_left = (y > 0 and x > 0) and (level[y - 1][x - 1] == tile)
                bottom_right = (y < max_y and x < max_x) and (level[y + 1][x + 1] == tile)
                bottom_left = (y < max_y and x > 0) and (level[y + 1][x - 1] == tile)
                
                # Check for border conditions and internal conditions
                if (left and not right and not top and bottom) or (top and bottom and left and right and not bottom_left):
                    wall = Wall(x * tile_size, y * tile_size, tile_size, tile_size, f"{tile}-circle-topright")
                elif (not left and right and not top and bottom) or (top and bottom and left and right and not bottom_right):
                    wall = Wall(x * tile_size, y * tile_size, tile_size, tile_size, f"{tile}-circle-topleft")
                elif (top and not bottom and left and not right) or (top and bottom and left and right and not top_left):
                    wall = Wall(x * tile_size, y * tile_size, tile_size, tile_size, f"{tile}-circle-bottomright")
                elif (top and not bottom and not left and right) or (top and bottom and left and right and not top_right):
                    wall = Wall(x * tile_size, y * tile_size, tile_size, tile_size, f"{tile}-circle-bottomleft")
                elif left and right:
                    wall = Wall(x * tile_size, y * tile_size, tile_size, tile_size, f"{tile}-line-horizontal")
                elif top and bottom:
                    wall = Wall(x * tile_size, y * tile_size, tile_size, tile_size, f"{tile}-line-vertical")

                if wall is None:
                    wall = Wall(x * tile_size, y * tile_size, tile_size, tile_size, None)
                wall_group.add(wall)
            
            elif tile == 'p':
                initial_player_x = x * tile_size
                initial_player_y = y * tile_size
            elif tile == '.':
                score = Score(x * tile_size, y * tile_size, tile_size)
                score_group.add(score)

    return level, initial_player_x, initial_player_y
