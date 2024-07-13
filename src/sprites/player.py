import pygame, os
from settings import TILE_SIZE

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.direction = "right"
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
        self.tolerance = TILE_SIZE // 3  # Allow a half of tile_size tolerance for turning

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

    def update(self, keys, level, walls):
        dx = dy = 0
        current_x = self.rect.center[0] // TILE_SIZE
        current_y = self.rect.center[1] // TILE_SIZE

        # Calculate desired movement
        if keys[pygame.K_LEFT]:
            if self.direction in ["up", "down"] and level[current_y][current_x - 1] != '#':
                self.rect.centery = current_y * TILE_SIZE + TILE_SIZE // 2
                self.direction = "left"
            elif self.direction == "right":
                self.direction = "left"
            dx = -self.move_speed
        elif keys[pygame.K_RIGHT]:
            if self.direction in ["up", "down"] and level[current_y][current_x + 1] != '#':
                self.rect.centery = current_y * TILE_SIZE + TILE_SIZE // 2
                self.direction = "right"
            elif self.direction == "left":
                self.direction = "right"
            dx = self.move_speed
        elif keys[pygame.K_UP]:
            if self.direction in ["left", "right"] and level[current_y - 1][current_x] != '#':
                self.rect.centerx = current_x * TILE_SIZE + TILE_SIZE // 2
                self.direction = "up"
            elif self.direction == "down":
                self.direction = "up"
            dy = -self.move_speed
        elif keys[pygame.K_DOWN]:
            if self.direction in ["left", "right"] and level[current_y + 1][current_x] != '#':
                self.rect.centerx = current_x * TILE_SIZE + TILE_SIZE // 2
                self.direction = "down"
            elif self.direction == "up":
                self.direction = "down"
            dy = self.move_speed

        # Apply movement and check for collisions
        if dx != 0 or dy != 0:
            self.move(dx, dy, walls)

        # Update direction and animation frames
        self.animation_timer += 1
        if self.animation_timer >= self.animation_delay:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames[self.direction])
            self.image = self.animation_frames[self.direction][self.frame_index]

    def move(self, dx, dy, walls):
        self.rect.x += dx
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.x -= dx  # Undo the movement if there is a collision
        self.rect.y += dy
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.y -= dy  # Undo the movement if there is a collision
