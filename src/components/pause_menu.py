import pygame
from components.button import Button
from components.selector import Selector
from settings import WHITE, BLACK

class PauseMenu:
    def __init__(self, screen, uifont, title_font):
        self.screen = screen
        self.uifont = uifont
        self.title_font = title_font
        self.current_menu = 'pause menu'
        self.menu_stack = []  # Stack to keep track of menu history
        self.menu_selected = 0
        self.pause_menu = {
            "pause menu": {
                "Resume": {"type": "button", "value": 1},
                "Settings": {"type": "button", "value": "settings"},
                "Quit": {"type": "button", "value": 0},
            },
            "settings": {
                "Show Direction Arrow": {"type": "selector", "value": "SHOW_DIRECTION_ARROW", "options": [True, False]},
                "Back": {"type": "button", "value": "pause menu"}
            }
        }
        self.create_elements()

    def create_elements(self):
        self.elements = []
        menu_options = self.pause_menu[self.current_menu]
        for i, (text, action) in enumerate(menu_options.items()):
            pos = (self.screen.get_width() // 2, self.screen.get_height() // 2 + i * 40)
            common_args = {'screen': self.screen, 'pos': pos, 'font': self.uifont, 'font_size': 16, 'color': WHITE, 'hover_color': BLACK, 'rect_hover_color': WHITE}
            if action["type"] == "selector":
                self.elements.append((Selector(name=text, options=action["options"], action=action["value"], **common_args), action))
            elif action["type"] == "button":
                self.elements.append((Button(text_input=text, bold_font=self.uifont, action=action["value"], **common_args), action))

    def draw(self):
        title_text, title_text_rect = self.title_font.render(self.current_menu.upper(), WHITE, size=60)
        title_text_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 3)
        self.screen.blit(title_text, title_text_rect)
        for i, (element, _) in enumerate(self.elements):
            if i == self.menu_selected:
                element.change_style(True)
            else:
                element.change_style(False)
            element.update()

    def apply_blur_effect(self):
        scale_down_factor = 0.1
        small_surface = pygame.transform.smoothscale(self.screen, (int(self.screen.get_width() * scale_down_factor), int(self.screen.get_height() * scale_down_factor)))
        blurred_surface = pygame.transform.smoothscale(small_surface, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(blurred_surface, (0, 0))

    def events(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for i, (element, _) in enumerate(self.elements):
                if element.check_for_input(mouse_pos):
                    self.menu_selected = i
                    break
            else:
                self.menu_selected = None

        elif event.type == pygame.MOUSEBUTTONDOWN and self.menu_selected is not None:
            element = self.elements[self.menu_selected][0]
            action = element.event(event)
            if action in [1, 0] or isinstance(action, str) and action in self.pause_menu:
                return self.handle_action(action)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.current_menu == 'pause menu':
                    return True, False  # Resume game
                else:
                    self.current_menu = self.menu_stack.pop() if self.menu_stack else 'pause menu'
                    self.menu_selected = 0
                    self.create_elements()
                    return True, True  # Remain paused
            if self.menu_selected is None:
                self.menu_selected = 0
            elif event.key == pygame.K_UP:
                self.menu_selected = (self.menu_selected - 1) % len(self.elements)
            elif event.key == pygame.K_DOWN:
                self.menu_selected = (self.menu_selected + 1) % len(self.elements)
            else:
                element = self.elements[self.menu_selected][0]
                action = element.event(event)
                return self.handle_action(action)

        return True, True

    def handle_action(self, action):
        if action == 1:
            return True, False  # Resume game
        elif action == 0:
            return False, False  # Quit game
        elif isinstance(action, str) and action in self.pause_menu:
            if self.current_menu != action:
                self.menu_stack.append(self.current_menu)  # Push current menu to stack
            self.current_menu = action
            self.menu_selected = None
            self.create_elements()
        return True, True
