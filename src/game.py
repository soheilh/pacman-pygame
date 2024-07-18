import pygame
from sprites.player import Player
from settings import *
from level import load_level

class Game:
    def __init__(self):
        self.uifont = pygame.font.Font("assets/fonts/emulogic.ttf", 16)

        # Screen dimensions
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Define UI heights
        self.top_ui_height = 50
        self.bottom_ui_height = 50
        self.map_area_height = SCREEN_HEIGHT - self.top_ui_height - self.bottom_ui_height

        # Create surfaces for UI areas
        self.top_ui_surface = pygame.Surface((SCREEN_WIDTH, self.top_ui_height))
        self.bottom_ui_surface = pygame.Surface((SCREEN_WIDTH, self.bottom_ui_height))

        # Map area surface
        self.map_area_surface = pygame.Surface((SCREEN_WIDTH, self.map_area_height))

        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.scores = pygame.sprite.Group()

        # Load level and create walls, scores, and get initial player position
        self.level, player_x, player_y = load_level(LEVEL_FILE, self.walls, self.scores, TILE_SIZE)
        self.player = Player(player_x, player_y)
        self.all_sprites.add(self.player)

        # Initialize font for displaying score and other UI elements
        self.font = pygame.font.Font(None, 36)

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

        # Draw top UI
        self.top_ui_surface.fill(BLACK)
        score_text = self.uifont.render(f"Score:{self.player.score:02}", True, WHITE)
        score_text_rect = score_text.get_rect()
        self.top_ui_surface.blit(score_text, (10, (self.top_ui_height - score_text_rect.height) // 2))
        self.screen.blit(self.top_ui_surface, (0, 0))

        # Draw bottom UI
        self.bottom_ui_surface.fill(BLACK)
        self.screen.blit(self.bottom_ui_surface, (0, SCREEN_HEIGHT - self.bottom_ui_height))

        # Draw map area
        self.map_area_surface.fill(BLACK)
        self.walls.draw(self.map_area_surface)
        self.scores.draw(self.map_area_surface)
        self.all_sprites.draw(self.map_area_surface)
        self.screen.blit(self.map_area_surface, (0, self.top_ui_height))

        pygame.display.flip()
