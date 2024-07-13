import pygame
from sprites.wall import Wall

def load_level(file_path, wall_group, tile_size):
    with open(file_path, 'r') as file:
        level = [[col for col in row] for row in file]
    for y, row in enumerate(level):
        for x, tile in enumerate(row):
            if tile == '#':
                wall = Wall(x * tile_size, y * tile_size, tile_size, tile_size, (255, 255, 255))
                wall_group.add(wall)
    return level
