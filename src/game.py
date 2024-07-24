import pygame
from sprites.player import Player
from settings import *
from level import load_level

class Game:
    def __init__(self):
        # Initialize fonts
        self.uifont = pygame.font.Font("assets/fonts/emulogic.ttf", 16)

        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Define UI heights
        self.top_ui_height = 50
        self.bottom_ui_height = 50
        self.map_area_height = SCREEN_HEIGHT - self.top_ui_height - self.bottom_ui_height

        # Create surfaces for UI areas
        self.top_ui_surface = pygame.Surface((SCREEN_WIDTH, self.top_ui_height))
        self.bottom_ui_surface = pygame.Surface((SCREEN_WIDTH, self.bottom_ui_height))
        self.map_area_surface = pygame.Surface((SCREEN_WIDTH, self.map_area_height))

        # Initialize sprite groups
        self.walls = pygame.sprite.Group()
        self.scores = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()

        # Load level and initialize game objects
        self.level, player_x, player_y, self.blinky, self.pinky, self.inky, self.clyde = load_level(
            LEVEL_FILE, self.walls, self.scores, TILE_SIZE
        )
        self.player = Player(player_x, player_y)
        self.player_sprites = pygame.sprite.Group(self.player)
        self.ghosts.add(self.blinky, self.pinky, self.inky, self.clyde)

        self.running = True

    def run(self):
        while self.running:
            self.events()
            delta_time = self.clock.tick(FPS) / 1000.0
            self.update(delta_time)
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.level, self.walls, self.scores, delta_time)
        player_pos = (
            self.player.rect.center[0] // TILE_SIZE,
            self.player.rect.center[1] // TILE_SIZE
        )
        self.ghosts.update(self.level, self.walls, delta_time, player_pos)

    def draw(self):
        self.screen.fill(BLACK)

        # Draw top UI
        self.top_ui_surface.fill(BLACK)
        score_text = self.uifont.render(f"Score:{self.player.score:02}", True, WHITE)
        score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, self.top_ui_height // 2))
        self.top_ui_surface.blit(score_text, score_text_rect)
        self.screen.blit(self.top_ui_surface, (0, 0))

        # Draw bottom UI
        self.bottom_ui_surface.fill(BLACK)
        self.screen.blit(self.bottom_ui_surface, (0, SCREEN_HEIGHT - self.bottom_ui_height))

        # Draw map area
        self.map_area_surface.fill(BLACK)
        self.walls.draw(self.map_area_surface)
        self.scores.draw(self.map_area_surface)
        self.player_sprites.draw(self.map_area_surface)
        self.ghosts.draw(self.map_area_surface)
        self.screen.blit(self.map_area_surface, (0, self.top_ui_height))

        pygame.display.flip()
