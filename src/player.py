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

    def update(self, keys):
        # Update direction based on keys pressed
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            self.direction = "left"
            dx = -self.move_speed
        elif keys[pygame.K_RIGHT]:
            self.direction = "right"
            dx = self.move_speed
        elif keys[pygame.K_UP]:
            self.direction = "up"
            dy = -self.move_speed
        elif keys[pygame.K_DOWN]:
            self.direction = "down"
            dy = self.move_speed

        # Apply movement and check for collisions
        if dx != 0 or dy != 0:
            self.move(dx, dy)

        # Update direction and animation frames
        self.animation_timer += 1
        if self.animation_timer >= self.animation_delay:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames[self.direction])
            self.image = self.animation_frames[self.direction][self.frame_index]

    def move(self, dx, dy):
        self.rect.x += dx
