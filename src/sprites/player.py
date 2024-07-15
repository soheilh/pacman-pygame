import pygame, os
from settings import TILE_SIZE

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.direction = "right"
        self.desired_direction = "right"
        self.frame_index = 0
        self.animation_frames = {
            "left": [],
            "right": [],
            "up": [],
            "down": []
        }
        self.load_images()
        self.image = self.animation_frames[self.direction][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.animation_timer = 0
        self.animation_delay = 10  # Adjust speed of animation
        self.move_speed = 2  # Adjust speed of movement
        self.score = 0

    def load_images(self):
        # Load images for all directions
        base_path = "assets/images/"
        size = (TILE_SIZE, TILE_SIZE)
        for direction in self.animation_frames:
            for i in range(1, 4):
                image_path = os.path.join(base_path, f"pacman-{direction}", f"{i}.png")
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(image, size)
                self.animation_frames[direction].append(image)

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
            self.move(dx, dy, walls)

        # Update animation frames
        self.update_animation()

        # Check for score collisions and update score
        self.score_collision(scores)

        # Check for boundray collisions and teleport if needed
        self.teleport(tile_x, tile_y, len(level[0]), len(level))

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
        if self.desired_direction == "left" and tile_x > 0 and level[tile_y][tile_x - 1] not in wall and (tile_y + 0.5) * TILE_SIZE == center_y:
            self.direction = "left"
            dx = -self.move_speed
            dy = 0
        elif self.desired_direction == "right" and tile_x < len(level[0]) - 1 and level[tile_y][tile_x + 1] not in wall and (tile_y + 0.5) * TILE_SIZE == center_y:
            self.direction = "right"
            dx = self.move_speed
            dy = 0
        elif self.desired_direction == "up" and tile_y > 0 and level[tile_y - 1][tile_x] not in wall and (tile_x + 0.5) * TILE_SIZE == center_x:
            self.direction = "up"
            dx = 0
            dy = -self.move_speed
        elif self.desired_direction == "down" and tile_y < len(level) - 1 and level[tile_y + 1][tile_x] not in wall and (tile_x + 0.5) * TILE_SIZE == center_x:
            self.direction = "down"
            dx = 0
            dy = self.move_speed

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

    def move(self, dx, dy, walls):
        self.rect.x += dx
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.x -= dx  # Undo the movement if there is a collision
        self.rect.y += dy
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.y -= dy  # Undo the movement if there is a collision

    def update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_delay:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames[self.direction])
            self.image = self.animation_frames[self.direction][self.frame_index]

    def score_collision(self, scores):
        collided_score = pygame.sprite.spritecollideany(self, scores)
        if collided_score:
            scores.remove(collided_score)
            self.score += 1

    def teleport(self, x, y, width, height):
        if x == -1 or x == width:
            self.rect.centerx = (width - abs(x)) * TILE_SIZE
            self.desired_direction = self.direction
        elif y == -1 or y == height:
            self.rect.centery = (height - abs(y)) * TILE_SIZE
            self.desired_direction = self.direction
