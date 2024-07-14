import pygame
from settings import SCORE_COLOR

class Score(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        self.width = tile_size // 5
        self.image = pygame.Surface((self.width, self.width), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Make the surface transparent
        pygame.draw.rect(self.image, SCORE_COLOR, (0, 0, self.width, self.width))
        self.rect = self.image.get_rect(center=(x + tile_size // 2, y + tile_size // 2))
