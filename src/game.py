import pygame
import pygame.freetype
from pygame.locals import *
from sprites.player import Player
import settings
from level import load_level
from main_menu import MainMenu
from components.pause_menu import PauseMenu

# Set the process DPI awareness
import ctypes
ctypes.windll.user32.SetProcessDPIAware()

class Game:
    def __init__(self):
        self.init_pygame()
        self.load_resources()
        self.setup_display()
        self.create_surfaces()
        self.init_game_objects()
        self.running = True
        self.paused = False
        self.main_menu = MainMenu(self.screen, self.oxanium, self.oxanium_bold)
        self.pause_menu = PauseMenu(self.screen, self.uifont, self.uifont)
        self.show_main_menu = True

        # FPS display variables
        self.fps_text = None
        self.fps_rect = None
        self.fps_timer = 1

    def init_pygame(self):
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()

    def load_resources(self):
        fonts = [
            ("uifont", "assets/fonts/emulogic.ttf"),
            ("oxanium", "assets/fonts/Oxanium-Medium.ttf"),
            ("oxanium_bold", "assets/fonts/Oxanium-ExtraBold.ttf"),
        ]
        for attr, path in fonts:
            try:
                setattr(self, attr, pygame.freetype.Font(path))
            except pygame.error as e:
                print(f"Error loading font {path}: {e}")
                pygame.quit()
                exit()

    def setup_display(self):
        self.screen_width, self.screen_height = settings.RESOLUTION
        display_mode = pygame.FULLSCREEN if settings.DISPLAY_MODE == "fullscreen" else pygame.RESIZABLE
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), display_mode, vsync=getattr(settings, "VSYNC"))
        self.update_offsets()

    def update_offsets(self):
        self.x_offset = (self.screen_width - settings.GAME_WIDTH) / 2
        self.y_offset = (self.screen_height - settings.GAME_HEIGHT) / 2

    def create_surfaces(self):
        self.game_surface = pygame.Surface((settings.GAME_WIDTH, settings.GAME_HEIGHT))
        self.top_ui_height = 50
        self.bottom_ui_height = 50
        self.map_area_height = settings.GAME_HEIGHT - self.top_ui_height - self.bottom_ui_height
        self.top_ui_surface = pygame.Surface((settings.GAME_WIDTH, self.top_ui_height))
        self.bottom_ui_surface = pygame.Surface((settings.GAME_WIDTH, self.bottom_ui_height))
        self.map_area_surface = pygame.Surface((settings.GAME_WIDTH, self.map_area_height))

    def init_game_objects(self):
        self.walls = pygame.sprite.Group()
        self.scores = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.level, player_x, player_y, self.blinky, self.pinky, self.inky, self.clyde = load_level(
            settings.LEVEL_FILE, self.walls, self.scores, settings.TILE_SIZE
        )
        self.player = Player(player_x, player_y)
        self.ghosts.add(self.blinky, self.pinky, self.inky, self.clyde)

    def run(self):
        while self.running:
            self.events()
            delta_time = self.clock.tick(settings.FPS) / 1000.0
            if self.show_main_menu:
                self.main_menu.draw(self.screen)
            elif not self.paused:
                self.update(delta_time)
                self.draw()
            else:
                self.draw()  # Draw game in background
                self.pause_menu.draw()
            self.update_fps_display(delta_time)
            pygame.display.flip()

    def update_fps_display(self, delta_time):
        self.fps_timer += delta_time
        if self.fps_timer >= 1.0:  # Update FPS every second
            self.fps_text, self.fps_rect = self.oxanium.render("FPS: " + str(int(self.clock.get_fps())) + " | Vsync: " + str(getattr(settings, "VSYNC")), settings.WHITE, size=24)
            self.fps_timer = 0
        if self.fps_text and self.fps_rect and settings.SHOW_FPS:
            self.fps_rect.topleft = (20, 20)
            self.screen.blit(self.fps_text, self.fps_rect)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.show_main_menu:
                self.running, self.show_main_menu = self.main_menu.events(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.paused:
                        self.running, self.paused = self.pause_menu.events(event)
                    else:
                        self.paused = True
                elif self.paused:
                    self.running, self.paused = self.pause_menu.events(event)
            elif event.type == pygame.MOUSEMOTION and self.paused:
                self.pause_menu.events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and self.paused:
                self.running, self.paused = self.pause_menu.events(event)
            elif event.type == VIDEORESIZE:
                self.screen_width, self.screen_height = event.size
                self.update_offsets()
                display_mode = pygame.FULLSCREEN if settings.DISPLAY_MODE == "fullscreen" else pygame.RESIZABLE
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), display_mode)

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.level, self.walls, self.scores, delta_time)
        player_pos = (
            self.player.rect.center[0] // settings.TILE_SIZE,
            self.player.rect.center[1] // settings.TILE_SIZE
        )
        self.ghosts.update(self.level, self.walls, delta_time, player_pos)

    def draw(self):
        self.screen.fill(settings.BLACK)
        self.draw_ui()
        self.draw_game_objects()
        if self.paused:
            self.pause_menu.apply_blur_effect()
            self.pause_menu.draw()

    def draw_ui(self):
        self.top_ui_surface.fill(settings.BLACK)
        score_text, score_text_rect = self.uifont.render(f"Score: {self.player.score:02}", settings.WHITE, size=16)
        score_text_rect.center = (settings.GAME_WIDTH // 2, self.top_ui_height // 2)
        self.top_ui_surface.blit(score_text, score_text_rect)
        self.game_surface.blit(self.top_ui_surface, (0, 0))

        self.bottom_ui_surface.fill(settings.BLACK)
        self.game_surface.blit(self.bottom_ui_surface, (0, settings.GAME_HEIGHT - self.bottom_ui_height))

    def draw_game_objects(self):
        self.map_area_surface.fill(settings.BLACK)
        self.walls.draw(self.map_area_surface)
        self.scores.draw(self.map_area_surface)
        self.player.draw(self.map_area_surface)
        if getattr(settings, "SHOW_DIRECTION_ARROW", False):
            direction_arrow = self.player.draw_direction_arrow()
            self.map_area_surface.blit(direction_arrow[0], direction_arrow[1])
        for ghost in self.ghosts:
            ghost.draw(self.map_area_surface)
        self.game_surface.blit(self.map_area_surface, (0, self.top_ui_height))
        self.screen.blit(self.game_surface, (self.x_offset, self.y_offset))
