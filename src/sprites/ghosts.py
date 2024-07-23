import pygame
import os
from settings import TILE_SIZE

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, ghost_name):
        super().__init__()
        self.direction = "left"
        self.load_images(ghost_name)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.move_speed = 150
        self.velocity = pygame.Vector2(0, 0)
    
    def load_images(self, name):
        base_path = "assets/images/ghosts"
        size = (TILE_SIZE, TILE_SIZE)
        image_path = os.path.join(base_path, f"{name}.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)

    def update(self, level, walls, delta_time, player_pos):
        ghost_x, ghost_y = self.rect.center
        tile_x, tile_y = ghost_x // TILE_SIZE, ghost_y // TILE_SIZE
        self.find_closest_neighbor(ghost_x, ghost_y, level, player_pos)
        self.calculate_movement()
        
        if self.velocity.length() > 0:
            self.move(self.velocity * delta_time, walls)
        
        self.teleport(tile_x, tile_y, len(level[0]), len(level))
    
    def find_closest_neighbor(self, x, y, level, target):
        tile_x = x // TILE_SIZE
        tile_y = y // TILE_SIZE
        wall_values = {'1', '2'}
        
        neighbors = [
            (tile_x, tile_y - 1, "up"),    # Up
            (tile_x + 1, tile_y, "right"), # Right
            (tile_x, tile_y + 1, "down"),  # Down
            (tile_x - 1, tile_y, "left")   # Left
        ]
        
        directions = ["up", "right", "down", "left"]
        direction_index = {dir: idx for idx, dir in enumerate(directions)}
        current_direction_idx = direction_index[self.direction]
        opposite_direction_idx = (current_direction_idx + 2) % 4

        passable_neighbors = [
            (nx, ny, direction) for (nx, ny, direction) in neighbors
            if 0 <= ny < len(level) and 0 <= nx < len(level[0]) and level[ny][nx] not in wall_values
        ]
        
        filtered_neighbors = [
            (nx, ny, direction) for (nx, ny, direction) in passable_neighbors 
            if direction_index[direction] != opposite_direction_idx
        ]

        if len(passable_neighbors) >= 2:
            distances = [
                (direction, (target[0] - nx) ** 2 + (target[1] - ny) ** 2)
                for (nx, ny, direction) in filtered_neighbors
            ]
            distances.sort(key=lambda item: (item[1], self.direction_priority(item[0])))
            
            if distances and self.is_close_to_center(x, y):
                self.rect.centerx = (tile_x + 0.5) * TILE_SIZE
                self.rect.centery = (tile_y + 0.5) * TILE_SIZE
                best_direction = distances[0][0]
                self.direction = best_direction
                print(f"Direction: {self.direction}, Filtered neighbors: {distances}")

    def is_close_to_center(self, x, y):
        tolerance = 2
        tile_center_x = (x // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
        tile_center_y = (y // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
        return abs(x - tile_center_x) < tolerance and abs(y - tile_center_y) < tolerance

    def direction_priority(self, direction):
        priorities = {"up": 1, "left": 2, "down": 3, "right": 4}
        return priorities[direction]

    def calculate_movement(self):
        self.velocity = pygame.Vector2(0, 0)
        if self.direction == "left":
            self.velocity.x = -self.move_speed
        elif self.direction == "right":
            self.velocity.x = self.move_speed
        elif self.direction == "up":
            self.velocity.y = -self.move_speed
        elif self.direction == "down":
            self.velocity.y = self.move_speed

    def move(self, movement, walls):
        self.rect.x += movement.x
        collision = pygame.sprite.spritecollideany(self, walls)
        if collision:
            if movement.x > 0:
                self.rect.right = collision.rect.left
            elif movement.x < 0:
                self.rect.left = collision.rect.right
        
        self.rect.y += movement.y
        collision = pygame.sprite.spritecollideany(self, walls)
        if collision:
            if movement.y > 0:
                self.rect.bottom = collision.rect.top
            elif movement.y < 0:
                self.rect.top = collision.rect.bottom
    
    def teleport(self, x, y, width, height):
        if x == -1 or x == width:
            self.rect.centerx = (width - abs(x) + 0.5) * TILE_SIZE
        elif y == -1 or y == height:
            self.rect.centery = (height - abs(y) + 0.5) * TILE_SIZE

class Blinky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, "blinky")
