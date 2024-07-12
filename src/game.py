import pygame
from player import Player
from settings import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()
        self.player = Player(100, 100)
        self.all_sprites.add(self.player)

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.all_sprites.update(keys)

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
