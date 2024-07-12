import pygame
import os

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

    def load_images(self):
        # Load images for all directions
        base_path = "assets/images/"
        for direction in self.animation_frames:
            for i in range(1, 4):
                image_path = os.path.join(base_path, f"pacman-{direction}", f"{i}.png")
                image = pygame.image.load(image_path).convert_alpha()
                self.animation_frames[direction].append(image)

    def update(self, keys):
        # Update direction based on keys pressed
        if keys[pygame.K_LEFT]:
            self.direction = "left"
            self.rect.x -= 5
        elif keys[pygame.K_RIGHT]:
            self.direction = "right"
            self.rect.x += 5
        elif keys[pygame.K_UP]:
            self.direction = "up"
            self.rect.y -= 5
        elif keys[pygame.K_DOWN]:
            self.direction = "down"
            self.rect.y += 5

        # Update direction and animation frames
        self.animation_timer += 1
        if self.animation_timer >= self.animation_delay:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames[self.direction])
            self.image = self.animation_frames[self.direction][self.frame_index]
