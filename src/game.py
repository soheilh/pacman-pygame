import pygame
from pygame.locals import *
from sprites.player import Player
import settings
from settings import *
from level import load_level
from components.pause_menu import PauseMenu

class Game:
    def __init__(self):
        self.init_pygame()
        self.load_resources()
        self.setup_display()
        self.create_surfaces()
        self.init_game_objects()
        self.running = True
        self.paused = False
        self.pause_menu = PauseMenu(self.screen, self.uifont, self.title_font)  # Initialize PauseMenu

    def init_pygame(self):
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()

    def load_resources(self):
        try:
            self.uifont = pygame.font.Font("assets/fonts/emulogic.ttf", 16)
            self.title_font = pygame.font.Font("assets/fonts/emulogic.ttf", 40)
        except pygame.error as e:
            print(f"Error loading font: {e}")
            pygame.quit()
            exit()

    def setup_display(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.x_offset = (self.screen_width - GAME_WIDTH) / 2
        self.y_offset = (self.screen_height - GAME_HEIGHT) / 2

    def create_surfaces(self):
        self.game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.top_ui_height = 50
        self.bottom_ui_height = 50
        self.map_area_height = GAME_HEIGHT - self.top_ui_height - self.bottom_ui_height
        self.top_ui_surface = pygame.Surface((GAME_WIDTH, self.top_ui_height))
        self.bottom_ui_surface = pygame.Surface((GAME_WIDTH, self.bottom_ui_height))
        self.map_area_surface = pygame.Surface((GAME_WIDTH, self.map_area_height))

    def init_game_objects(self):
        self.walls = pygame.sprite.Group()
        self.scores = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.level, player_x, player_y, self.blinky, self.pinky, self.inky, self.clyde = load_level(
            LEVEL_FILE, self.walls, self.scores, TILE_SIZE
        )
        self.player = Player(player_x, player_y)
        self.player_sprites = pygame.sprite.Group(self.player)
        self.ghosts.add(self.blinky, self.pinky, self.inky, self.clyde)

    def run(self):
        while self.running:
            self.events()
            delta_time = self.clock.tick(FPS) / 1000.0
            if not self.paused:
                self.update(delta_time)
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused  # Toggle pause state
                elif self.paused:
                    self.running, self.paused = self.pause_menu.events(event)
            elif event.type == pygame.MOUSEMOTION and self.paused:
                self.pause_menu.events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and self.paused:
                self.running, self.paused = self.pause_menu.events(event)

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
        self.draw_ui()
        self.draw_game_objects()
        if self.paused:
            self.pause_menu.apply_blur_effect()
            self.pause_menu.draw()
        pygame.display.flip()

    def draw_ui(self):
        self.top_ui_surface.fill(BLACK)
        score_text = self.uifont.render(f"Score: {self.player.score:02}", True, WHITE)
        score_text_rect = score_text.get_rect(center=(GAME_WIDTH // 2, self.top_ui_height // 2))
        self.top_ui_surface.blit(score_text, score_text_rect)
        self.game_surface.blit(self.top_ui_surface, (0, 0))

        self.bottom_ui_surface.fill(BLACK)
        self.game_surface.blit(self.bottom_ui_surface, (0, GAME_HEIGHT - self.bottom_ui_height))

    def draw_game_objects(self):
        self.map_area_surface.fill(BLACK)
        self.walls.draw(self.map_area_surface)
        self.scores.draw(self.map_area_surface)
        self.player_sprites.draw(self.map_area_surface)
        
        # Dynamically check the updated setting
        show_direction_arrow = getattr(settings, "SHOW_DIRECTION_ARROW")
        if show_direction_arrow:
            direction_arrow = self.player.draw_direction_arrow()
            self.map_area_surface.blit(direction_arrow[0], direction_arrow[1])
        
        self.ghosts.draw(self.map_area_surface)
        self.game_surface.blit(self.map_area_surface, (0, self.top_ui_height))
        self.screen.blit(self.game_surface, (self.x_offset, self.y_offset))
