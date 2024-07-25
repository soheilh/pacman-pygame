import pygame
from pygame.locals import *
from sprites.player import Player
from settings import *
from level import load_level
from components.button import Button

class Game:
    def __init__(self):
        self.init_pygame()
        self.load_resources()
        self.setup_display()
        self.create_surfaces()
        self.init_game_objects()
        self.running = True
        self.paused = False
        self.menu_selected = 0

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
                    if event.key == pygame.K_UP:
                        self.menu_selected = (self.menu_selected - 1) % len(self.buttons)
                    elif event.key == pygame.K_DOWN:
                        self.menu_selected = (self.menu_selected + 1) % len(self.buttons)
                    elif event.key == pygame.K_RETURN:
                        if self.menu_selected == 0:
                            self.paused = False  # Resume game
                        elif self.menu_selected == 1:
                            self.running = False  # Quit game

            elif event.type == pygame.MOUSEBUTTONDOWN and self.paused:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(self.buttons):
                    if button.check_for_input(mouse_pos):
                        if i == 0:
                            self.paused = False  # Resume game
                        elif i == 1:
                            self.running = False  # Quit game
                        break

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
            self.draw_pause_screen()
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
        self.ghosts.draw(self.map_area_surface)
        self.game_surface.blit(self.map_area_surface, (0, self.top_ui_height))
        self.screen.blit(self.game_surface, (self.x_offset, self.y_offset))

    def draw_pause_screen(self):
        # Apply blur effect
        self.apply_blur_effect()

        # Draw pause title
        title_text = self.title_font.render("PAUSE MENU", True, WHITE)
        title_text_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
        self.screen.blit(title_text, title_text_rect)

        # Create pause menu buttons (ensure this runs only once)
        if not hasattr(self, 'buttons'):
            self.buttons = []
            menu_options = ["Resume", "Quit"]
            for i, option in enumerate(menu_options):
                button = Button(
                    pos=(self.screen_width // 2, self.screen_height // 2 + i * 50),
                    text_input=option,
                    font=self.uifont,
                    color=WHITE,
                    hover_color=BLACK,
                    rect_hover_color=WHITE,
                )
                self.buttons.append(button)

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        for i, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_pos):
                self.menu_selected = i
            if i == self.menu_selected:
                button.change_style(self.screen)
            else:
                button.reset_style()
            button.update(self.screen)

    def apply_blur_effect(self):
        scale_down_factor = 0.1
        small_surface = pygame.transform.smoothscale(self.screen, (int(self.screen_width * scale_down_factor), int(self.screen_height * scale_down_factor)))
        blurred_surface = pygame.transform.smoothscale(small_surface, (self.screen_width, self.screen_height))
        for _ in range(2):
            small_surface = pygame.transform.smoothscale(blurred_surface, (int(self.screen_width * scale_down_factor), int(self.screen_height * scale_down_factor)))
            blurred_surface = pygame.transform.smoothscale(small_surface, (self.screen_width, self.screen_height))
        self.screen.blit(blurred_surface, (0, 0))
