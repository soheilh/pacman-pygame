import pygame
from sprites.player import Player
from settings import *
from level import load_level

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.scores = pygame.sprite.Group()
        
        # Load level and create walls, scores, and get initial player position
        self.level, player_x, player_y = load_level(LEVEL_FILE, self.walls, self.scores, TILE_SIZE)
        self.player = Player(player_x, player_y)
        self.all_sprites.add(self.player)

    def run(self):
        while self.running:
            self.events()
            delta_time = self.clock.tick(FPS) / 1000.0  # Time per frame in seconds
            self.update(delta_time)
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.level, self.walls, self.scores, delta_time)

    def draw(self):
        self.screen.fill(BLACK)
        self.walls.draw(self.screen)
        self.scores.draw(self.screen)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
