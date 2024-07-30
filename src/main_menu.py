import pygame
from components.button import Button
from components.selector import Selector
from components.slider import Slider
from settings import WHITE, BLACK

class MainMenu:
    def __init__(self, screen, font, bold_font, title_font):
        self.screen = screen
        self.font = font
        self.bold_font = bold_font
        self.title_font = title_font
        self.current_menu = "main menu"
        self.menu_stack = []
        self.left_menu_item = 0
        self.right_menu_item = 0
        self.right_menu_status = False

        self.left_menu_surface = pygame.Surface((self.screen.get_width() / 4, self.screen.get_height() * 3 / 4))
        self.right_menu_surface = pygame.Surface((self.screen.get_width() / 2, self.screen.get_height() * 3 / 4))

        self.main_menu = {
            "main menu": {
                "play": {"type": "button", "value": 1},
                "options": {"type": "button", "value": "options"},
                "credits": {"type": "button", "value": "credits"},
                "quit": {"type": "button", "value": 0},
            },
            "options": {
                "gameplay": {"type": "button", "value": "gameplay"},
                "display": {"type": "button", "value": "display"},
                "sound": {"type": "button", "value": "sound"},
            },
            "gameplay": {
                "show direction arrow": {"type": "selector", "value": "SHOW_DIRECTION_ARROW", "options": [True, False]},
            },
            "display": {
                "display resolution": {"type": "selector", "value": "RESOLUTION", "options": pygame.display.list_modes()},
                "display mode": {"type": "selector", "value": "DISPLAY_MODE", "options": ["fullscreen", "windowed"]},
                "quality mode": {"type": "selector", "value": "QUALITY_MODE", "options": ["classic", "modern"]},
                "v-sync": {"type": "selector", "value": "VSYNC", "options": [1, 0]},
            },
            "sound": {
                "master volume": {"type": "slider", "value": "MASTER_VOLUME", "options": range(0, 11)},
                "music volume": {"type": "slider", "value": "MUSIC_VOLUME", "options": range(0, 11)},
                "sound effect volume": {"type": "slider", "value": "EFFECT_VOLUME", "options": range(0, 11)},
            },
        }
        self.create_elements()

    def create_elements(self):
        self.left_elements = []
        self.right_elements = {}
        menu_options = self.main_menu.get(self.current_menu, {})

        for i, title in enumerate(menu_options):
            pos = (50, self.left_menu_surface.get_height() / 2 + i * 40)
            self.left_elements.append(Button(text_input=title, action=menu_options[title]["value"], pos=pos, font=self.font, bold_font=self.bold_font, color=(229, 229, 229), hover_color=(252, 252, 252), rect_hover_color=WHITE))

            item = menu_options.get(title, {})
            if item["type"] == "button" and item["value"] in self.main_menu:
                submenu = self.main_menu[item["value"]]
                if submenu:
                    self.right_elements[title] = []
                    for j, (text, action) in enumerate(submenu.items()):
                        common_args = {'font': self.font, 'bold_font': self.bold_font, 'color': (229, 229, 229), 'hover_color': BLACK, 'rect_hover_color': WHITE}
                        pos = (0, self.right_menu_surface.get_height() / 3 + j * 60)
                        if action["type"] == "selector":
                            self.right_elements[title].append((Selector(screen=self.right_menu_surface, pos=pos, padding=10, name=text, options=action["options"], action=action["value"], **common_args), action))
                        elif action["type"] == "slider":
                            self.right_elements[title].append((Slider(screen=self.right_menu_surface, pos=pos, padding=10, name=text, options=action["options"], action=action["value"], **common_args), action))
                        elif action["type"] == "button":
                            self.right_elements[title].append((Button(pos=pos, text_input=text, action=action["value"], **common_args), action))

    def draw(self, screen):
        screen.fill((10, 16, 20))

        self.left_menu_surface.fill((10, 16, 20))
        title_text = self.title_font.render(self.current_menu.upper(), True, WHITE)
        title_text_rect = title_text.get_rect(topleft=(50, self.left_menu_surface.get_height() / 3))
        self.left_menu_surface.blit(title_text, title_text_rect)

        for i, element in enumerate(self.left_elements):
            if i == self.left_menu_item:
                element.change_style(self.left_menu_surface)
            else:
                element.reset_style(self.left_menu_surface)
            element.update(self.left_menu_surface)
        self.screen.blit(self.left_menu_surface, (0, self.screen.get_height() / 8))

        self.right_menu_surface.fill((10, 16, 20))
        if self.current_menu == "options" and not self.right_menu_status:
            right_menu_key = self.left_elements[self.left_menu_item].action
            if right_menu_key in self.right_elements:
                for element, _ in self.right_elements[right_menu_key]:
                    element.reset_style(self.right_menu_surface)
                    element.update(self.right_menu_surface)
        elif self.right_menu_status:
            right_menu_key = self.left_elements[self.left_menu_item].action
            if right_menu_key in self.right_elements:
                for i, (element, _) in enumerate(self.right_elements[right_menu_key]):
                    if i == self.right_menu_item:
                        element.change_style(self.right_menu_surface)
                    else:
                        element.reset_style(self.right_menu_surface)
                    element.update(self.right_menu_surface)
        self.screen.blit(self.right_menu_surface, (self.screen.get_width() / 4, self.screen.get_height() / 8))

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if self.right_menu_status:
                right_menu_key = self.left_elements[self.left_menu_item].action
                if right_menu_key in self.right_elements:
                    num_elements = len(self.right_elements[right_menu_key])
                    if event.key == pygame.K_UP:
                        self.right_menu_item = (self.right_menu_item - 1) % num_elements
                    elif event.key == pygame.K_DOWN:
                        self.right_menu_item = (self.right_menu_item + 1) % num_elements
                    elif event.key in [pygame.K_RETURN, pygame.K_LEFT, pygame.K_RIGHT]:
                        element = self.right_elements[right_menu_key][self.right_menu_item][0]
                        action = element.event(event)
                        return self.handle_action(action)
                    elif event.key == pygame.K_ESCAPE:
                        self.right_menu_status = False
            else:
                if event.key == pygame.K_UP:
                    self.left_menu_item = (self.left_menu_item - 1) % len(self.left_elements)
                elif event.key == pygame.K_DOWN:
                    self.left_menu_item = (self.left_menu_item + 1) % len(self.left_elements)
                elif event.key == pygame.K_RETURN:
                    left_action_key = self.left_elements[self.left_menu_item].action
                    if left_action_key in self.right_elements and self.current_menu == "options":
                        self.right_menu_status = True
                        self.right_menu_item = 0
                    else:
                        element = self.left_elements[self.left_menu_item]
                        action = element.event(event)
                        return self.handle_action(action)
                elif event.key == pygame.K_ESCAPE:
                    if self.right_menu_status:
                        self.right_menu_status = False
                    elif self.menu_stack:
                        self.current_menu = self.menu_stack.pop()
                        self.left_menu_item = 0
                        self.right_menu_item = 0
                        self.right_menu_status = False
                        self.create_elements()
        return True, True

    def handle_action(self, action):
        if action == 1:
            return True, False
        elif action == 0:
            return False, True
        elif isinstance(action, str) and action in self.main_menu:
            if self.current_menu != action:
                self.menu_stack.append(self.current_menu)
            self.current_menu = action
            self.left_menu_item = 0
            self.right_menu_item = 0
            self.right_menu_status = False
            self.create_elements()
        return True, True
