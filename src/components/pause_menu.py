import pygame
from components.button import Button
from settings import WHITE, BLACK

class PauseMenu:
    def __init__(self, screen, uifont, title_font):
        self.screen = screen
        self.uifont = uifont
        self.title_font = title_font
        self.buttons = []
        self.menu_selected = 0
        self.create_buttons()

    def create_buttons(self):
        menu_options = ["Resume", "Quit"]
        for i, option in enumerate(menu_options):
            button = Button(
                pos=(self.screen.get_width() // 2, self.screen.get_height() // 2 + i * 40),
                text_input=option,
                font=self.uifont,
                color=WHITE,
                hover_color=BLACK,
                rect_hover_color=WHITE,
            )
            self.buttons.append(button)

    def draw(self):
        # Draw pause title
        title_text = self.title_font.render("PAUSE MENU", True, WHITE)
        title_text_rect = title_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 3))
        self.screen.blit(title_text, title_text_rect)

        # Draw buttons
        for i, button in enumerate(self.buttons):
            if i == self.menu_selected:
                button.change_style(self.screen)
            else:
                button.reset_style()
            button.update(self.screen)

    def apply_blur_effect(self):
        scale_down_factor = 0.1
        small_surface = pygame.transform.smoothscale(self.screen, (int(self.screen.get_width() * scale_down_factor), int(self.screen.get_height() * scale_down_factor)))
        blurred_surface = pygame.transform.smoothscale(small_surface, (self.screen.get_width(), self.screen.get_height()))
        for _ in range(2):
            small_surface = pygame.transform.smoothscale(blurred_surface, (int(self.screen.get_width() * scale_down_factor), int(self.screen.get_height() * scale_down_factor)))
            blurred_surface = pygame.transform.smoothscale(small_surface, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(blurred_surface, (0, 0))

    def events(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for i, button in enumerate(self.buttons):
                if button.check_for_input(mouse_pos):
                    self.menu_selected = i
                    break
                else:
                    self.menu_selected = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, button in enumerate(self.buttons):
                if button.check_for_input(mouse_pos):
                    if i == 0:
                        return True, False  # Resume game
                    elif i == 1:
                        return False, False  # Quit game
            return True, True
