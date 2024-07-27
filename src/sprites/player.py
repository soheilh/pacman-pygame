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
        self.arrow_image = pygame.image.load("assets/images/other/arrow.png").convert_alpha()
        self.angles = {
            "right": [0, (TILE_SIZE, 0)],
            "up": [90, (0, -TILE_SIZE)],
            "left": [180, (-TILE_SIZE, 0)],
            "down": [270, (0, TILE_SIZE)]
        }
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.animation_timer = 0
        self.animation_delay = 6  # Adjust speed of animation
        self.move_speed = 200  # Adjust speed of movement (pixels per second)
        self.velocity = pygame.Vector2(0, 0)
        self.score = 0

    def load_images(self):
        # Load images (one set of images)
        base_path = "assets/images/pacman"
        size = (TILE_SIZE * 1.25, TILE_SIZE * 1.25)
        for i in range(1, 4):
            image_path = os.path.join(base_path, f"{i}.png")
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, size)
            self.animation_frames.append(image)

    def update(self, keys, level, walls, scores, delta_time):
        center_x, center_y = self.rect.center
        tile_x = center_x // TILE_SIZE
        tile_y = center_y // TILE_SIZE
        # Set desired direction based on key presses
        self.set_desired_direction(keys)
        # Check if we can turn to the desired direction
        self.check_turning(tile_x, tile_y, center_x, center_y, level)
        # Calculate current direction movement
        self.calculate_movement()
        # Apply movement and check for collisions
        if self.velocity.length() > 0:
            self.move(self.velocity * delta_time, walls)
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
        if in_range and self.is_close_to_center(center_x, center_y):
            if self.desired_direction == "left" and tile_x > 0 and level[tile_y][tile_x - 1] not in wall:
                self.direction = "left"
                self.rect.centery = (tile_y + 0.5) * TILE_SIZE
            elif self.desired_direction == "right" and tile_x < len(level[0]) - 1 and level[tile_y][tile_x + 1] not in wall:
                self.direction = "right"
                self.rect.centery = (tile_y + 0.5) * TILE_SIZE
            elif self.desired_direction == "up" and tile_y > 0 and level[tile_y - 1][tile_x] not in wall:
                self.direction = "up"
                self.rect.centerx = (tile_x + 0.5) * TILE_SIZE
            elif self.desired_direction == "down" and tile_y < len(level) - 1 and level[tile_y + 1][tile_x] not in wall:
                self.direction = "down"
                self.rect.centerx = (tile_x + 0.5) * TILE_SIZE

    def is_close_to_center(self, center_x, center_y):
        tolerance = 3
        return abs(center_x % TILE_SIZE - TILE_SIZE // 2) < tolerance and abs(center_y % TILE_SIZE - TILE_SIZE // 2) < tolerance

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

    def update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_delay:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.frame_index]
            self.original_image = self.image  # Update the original image
        # Rotate the image based on the direction
        self.image = pygame.transform.rotate(self.original_image, self.angles[self.direction][0])

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

    def draw_direction_arrow(self):
        arrow_image = pygame.transform.scale(self.arrow_image, (TILE_SIZE, TILE_SIZE))
        angle = self.angles[self.desired_direction][0]
        rotated_arrow = pygame.transform.rotate(arrow_image, angle)
        offset = self.angles[self.desired_direction][1]
        arrow_rect = rotated_arrow.get_rect(center=(self.rect.centerx + offset[0], self.rect.centery + offset[1]))
        return rotated_arrow, arrow_rect.topleft

    def draw(self, screen):
        # Calculate the top-left position to blit the image centered on the rect
        top_left_x = self.rect.centerx - self.image.get_width() / 2
        top_left_y = self.rect.centery - self.image.get_height() / 2
        # Blit the image at the calculated position
        screen.blit(self.image, (top_left_x, top_left_y))
