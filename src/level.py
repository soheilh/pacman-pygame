import pygame
from sprites.wall import Wall
from sprites.score import Score
from settings import WALL_COLOR

def load_level(file_path, wall_group, score_group, tile_size):
    initial_player_x = 18 * tile_size
    initial_player_y = 15 * tile_size

    with open(file_path, 'r') as file:
        level = [[col for col in row] for row in file]
    for y, row in enumerate(level):
        for x, tile in enumerate(row):
            if tile == '#':
                wall = Wall(x * tile_size, y * tile_size, tile_size, tile_size, WALL_COLOR)
                wall_group.add(wall)
            elif tile == 'p':
                initial_player_x = x * tile_size
                initial_player_y = y * tile_size
            elif tile == '.':
                score = Score(x * tile_size, y * tile_size, tile_size)
                score_group.add(score)

    return level, initial_player_x, initial_player_y
