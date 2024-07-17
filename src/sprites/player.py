import pygame
import os
from settings import TILE_SIZE

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.direction = "right"
        self.desired_direction = "right"
        self.frame_index = 0
        self.animation_frames = []
        self.load_images()
        self.image = self.animation_frames[self.frame_index]
        self.original_image = self.image  # Store the original image for rotation
        self.angles = {
            "right": 0,
            "up": 90,
            "left": 180,
            "down": 270
        }
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.animation_timer = 0
        self.animation_delay = 6  # Adjust speed of animation
        self.move_speed = 3  # Adjust speed of movement
        self.score = 0

    def load_images(self):
        # Load images (one set of images)
        base_path = "assets/images/pacman"
        size = (TILE_SIZE, TILE_SIZE)
        for i in range(1, 4):
            image_path = os.path.join(base_path, f"{i}.png")
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, size)
            self.animation_frames.append(image)

    def update(self, keys, level, walls, scores):
        center_x, center_y = self.rect.center
        tile_x = center_x // TILE_SIZE
        tile_y = center_y // TILE_SIZE
        # Set desired direction based on key presses
        self.set_desired_direction(keys)
        # Check if we can turn to the desired direction
        self.check_turning(tile_x, tile_y, center_x, center_y, level)
        # Calculate current direction movement
        dx, dy = self.calculate_movement()
        # Apply movement and check for collisions
        if dx != 0 or dy != 0:
            self.move(dx, dy, walls, len(level[0]), len(level))
        # Check for boundary collisions and teleport if needed
        self.teleport(tile_x, tile_y, len(level[0]), len(level))
        # Update animation frames
        self.update_animation()
        # Check for score collisions and update score
        self.score_collision(scores)

    def set_desired_direction(self, keys):
        if keys[pygame.K_LEFT]:
            self.desired_direction = "left"
        elif keys[pygame.K_RIGHT]:
            self.desired_direction = "right"
        elif keys[pygame.K_UP]:
            self.desired_direction = "up"
        elif keys[pygame.K_DOWN]:
            self.desired_direction = "down"

    def check_turning(self, tile_x, tile_y, center_x, center_y, level):
        wall = ['1', '2']
        in_range = 0 < tile_x < len(level[0]) - 1 and 0 < tile_y < len(level) - 1
        if in_range:
            if self.desired_direction == "left" and tile_x > 0 and level[tile_y][tile_x - 1] not in wall and (tile_y + 0.5) * TILE_SIZE == center_y:
                self.direction = "left"
            elif self.desired_direction == "right" and tile_x < len(level[0]) - 1 and level[tile_y][tile_x + 1] not in wall and (tile_y + 0.5) * TILE_SIZE == center_y:
                self.direction = "right"
            elif self.desired_direction == "up" and tile_y > 0 and level[tile_y - 1][tile_x] not in wall and (tile_x + 0.5) * TILE_SIZE == center_x:
                self.direction = "up"
            elif self.desired_direction == "down" and tile_y < len(level) - 1 and level[tile_y + 1][tile_x] not in wall and (tile_x + 0.5) * TILE_SIZE == center_x:
                self.direction = "down"

    def calculate_movement(self):
        dx = dy = 0
        if self.direction == "left":
            dx = -self.move_speed
        elif self.direction == "right":
            dx = self.move_speed
        elif self.direction == "up":
            dy = -self.move_speed
        elif self.direction == "down":
            dy = self.move_speed
        return dx, dy

    def move(self, dx, dy, walls, width, height):
        self.rect.x += dx
        collision = pygame.sprite.spritecollideany(self, walls)
        if collision:
            if dx > 0:
                self.rect.right = collision.rect.left
            elif dx < 0:
                self.rect.left = collision.rect.right
        self.rect.y += dy
        collision = pygame.sprite.spritecollideany(self, walls)
        if collision:
            if dy > 0:
                self.rect.bottom = collision.rect.top
            elif dy < 0:
                self.rect.top = collision.rect.bottom

    def update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_delay:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.frame_index]
            self.original_image = self.image  # Update the original image
        # Rotate the image based on the direction
        self.image = pygame.transform.rotate(self.original_image, self.angles[self.direction])

    def score_collision(self, scores):
        collided_score = pygame.sprite.spritecollideany(self, scores)
        if collided_score:
            scores.remove(collided_score)
            self.score += 1

    def teleport(self, x, y, width, height):
        if x == -1 or x == width:
            self.rect.centerx = (width - abs(x) + 0.5) * TILE_SIZE
        elif y == -1 or y == height:
            self.rect.centery = (height - abs(y) + 0.5) * TILE_SIZE
