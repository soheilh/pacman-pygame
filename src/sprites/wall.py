import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, type):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        if type:
            self.image = pygame.image.load(f"assets/images/wall/{type}.png")
        else:
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))  # Fill with a transparent color
