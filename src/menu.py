import pygame
from components.button import Button
from components.selector import Selector
from components.slider import Slider
import settings

class BaseMenu:
    ITEM_VERTICAL_SPACING = 70
    MAX_VISIBLE_ITEMS = 7

    def __init__(self, screen, font, bold_font):
        self.screen = screen
        self.font = font
        self.bold_font = bold_font
        self.current_menu = ""
        self.menu_stack = []
        self.menu_item_stack = []
        self.left_menu_item = 0
        self.right_menu_item = 0
        self.right_menu_status = False
        self.scroll_offset = 0

        self.left_menu_surface = pygame.Surface((self.screen.get_width() / 4, self.MAX_VISIBLE_ITEMS * self.ITEM_VERTICAL_SPACING), pygame.SRCALPHA)
        self.right_menu_surface = pygame.Surface((self.screen.get_width() / 2, self.MAX_VISIBLE_ITEMS * self.ITEM_VERTICAL_SPACING), pygame.SRCALPHA)
        self.right_menu_content_surface = pygame.Surface((self.right_menu_surface.get_width(), 0), pygame.SRCALPHA)

        self.left_elements_cache = {}
        self.right_elements_cache = {}

    def create_elements(self, menu_structure):
        for menu_name, menu_items in menu_structure.items():
            self.left_elements_cache[menu_name] = self.create_left_menu_elements(menu_items)
            self.right_elements_cache[menu_name] = self.create_right_menu_elements(menu_items, menu_structure)
        self.left_elements = self.left_elements_cache.get(self.current_menu, [])

    def create_left_menu_elements(self, menu_items):
        elements = []
        for i, (title, item) in enumerate(menu_items.items()):
            pos = (50, self.left_menu_surface.get_height() / 2 + i * 40)
            elements.append(
                Button(
                    screen=self.left_menu_surface,
                    text_input=title,
                    action=item["value"],
                    pos=pos,
                    font=self.font,
                    bold_font=self.bold_font,
                    font_size=26,
                    color=settings.WHITE,
                    hover_color=settings.BRIGHT_WHITE,
                    rect_hover_color=None
                )
            )
        return elements

    def create_right_menu_elements(self, menu_items, menu_structure):
        right_elements = {}
        for title, item in menu_items.items():
            if item["type"] == "button" and item.get("right_menu", False):
                submenu_name = item["value"]
                submenu_items = menu_structure.get(submenu_name, {})
                right_elements[title] = []
                for j, (text, action) in enumerate(submenu_items.items()):
                    pos = (0, j * self.ITEM_VERTICAL_SPACING + 35)
                    common_args = {
                        'pos': pos,
                        'screen': self.right_menu_content_surface,
                        'font': self.font,
                        'font_size': 24,
                        'color': settings.WHITE,
                        'hover_color': settings.BLACK,
                        'rect_hover_color': settings.WHITE
                    }
                    if action["type"] == "selector":
                        right_elements[title].append((Selector(name=text, options=action["options"], action=action["value"], **common_args), action))
                    elif action["type"] == "slider":
                        right_elements[title].append((Slider(name=text, range_values=action["options"], action=action["value"], **common_args), action))
                    elif action["type"] == "button":
                        right_elements[title].append((Button(text_input=text, bold_font=self.bold_font, action=action["value"], **common_args), action))
        return right_elements

    def draw(self):
        self.screen.fill(settings.MENU_BG_COLOR)
        self.left_menu_surface.fill((0, 0, 0, 0))
        self.right_menu_surface.fill((0, 0, 0, 0))
        self.draw_title()
        self.draw_left_elements()
        self.draw_right_menu()
        self.screen.blit(self.left_menu_surface, (0, self.screen.get_height() / 4))

    def draw_title(self):
        title_text, title_text_rect = self.bold_font.render(self.current_menu.upper(), settings.WHITE, size=70)
        title_text_rect.topleft = (50, self.left_menu_surface.get_height() / 4)
        self.left_menu_surface.blit(title_text, title_text_rect)

    def draw_left_elements(self):
        for i, element in enumerate(self.left_elements):
            element.change_style(i == self.left_menu_item)
            element.update()

    def draw_right_menu(self):
        right_menu_key = self.left_elements[self.left_menu_item].action
        if right_menu_key in self.right_elements_cache.get(self.current_menu, {}):
            content_height = len(self.right_elements_cache[self.current_menu][right_menu_key]) * self.ITEM_VERTICAL_SPACING
            self.right_menu_content_surface = pygame.transform.scale(self.right_menu_content_surface,(self.right_menu_surface.get_width(), content_height))
            self.right_menu_content_surface.fill((0, 0, 0, 0))

            if self.right_menu_status:
                visible_elements = self.right_elements_cache[self.current_menu][right_menu_key][self.scroll_offset:self.scroll_offset + self.MAX_VISIBLE_ITEMS]
                for i, (element, _) in enumerate(visible_elements):
                    element.screen = self.right_menu_content_surface
                    element.change_style(i == (self.right_menu_item - self.scroll_offset))
                    element.update()
            else:
                for element, _ in self.right_elements_cache[self.current_menu][right_menu_key][:self.MAX_VISIBLE_ITEMS]:
                    element.screen = self.right_menu_content_surface
                    element.change_style(False)
                    element.update()

            self.blit_right_menu_content()
        self.screen.blit(self.right_menu_surface, (self.screen.get_width() / 4, self.screen.get_height() / 4))

    def blit_right_menu_content(self):
        if self.right_menu_content_surface.get_height() <= self.right_menu_surface.get_height():
            self.right_menu_surface.blit(self.right_menu_content_surface,(0, (self.right_menu_surface.get_height() - self.right_menu_content_surface.get_height()) / 2 - self.scroll_offset * self.ITEM_VERTICAL_SPACING))
        else:
            self.right_menu_surface.blit(self.right_menu_content_surface,(0, -self.scroll_offset * self.ITEM_VERTICAL_SPACING))

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.navigate_menu(-1)
            elif event.key == pygame.K_DOWN:
                self.navigate_menu(1)
            elif event.key in [pygame.K_RETURN, pygame.K_RIGHT, pygame.K_LEFT]:
                return self.select_menu_item(event)
            elif event.key == pygame.K_ESCAPE:
                return self.navigate_back()
        return True, True

    def navigate_menu(self, direction):
        if self.right_menu_status:
            right_menu_key = self.left_elements[self.left_menu_item].action
            if right_menu_key in self.right_elements_cache.get(self.current_menu, {}):
                num_elements = len(self.right_elements_cache[self.current_menu][right_menu_key])
                self.right_menu_item = (self.right_menu_item + direction) % num_elements
                self.adjust_scroll()
        else:
            self.left_menu_item = (self.left_menu_item + direction) % len(self.left_elements)

    def adjust_scroll(self):
        if self.right_menu_item < self.scroll_offset:
            self.scroll_offset = self.right_menu_item
        elif self.right_menu_item >= self.scroll_offset + self.MAX_VISIBLE_ITEMS:
            self.scroll_offset = self.right_menu_item - self.MAX_VISIBLE_ITEMS + 1

    def select_menu_item(self, event):
        if self.right_menu_status:
            right_menu_key = self.left_elements[self.left_menu_item].action
            if right_menu_key in self.right_elements_cache.get(self.current_menu, {}):
                element = self.right_elements_cache[self.current_menu][right_menu_key][self.right_menu_item][0]
                action = element.event(event)
                return self.handle_action(action)
        else:
            left_action_key = self.left_elements[self.left_menu_item].action
            if left_action_key in self.right_elements_cache.get(self.current_menu, {}) and self.menu[self.current_menu][left_action_key].get("right_menu", False):
                self.right_menu_status = True
                self.right_menu_item = 0
                self.scroll_offset = 0
            else:
                element = self.left_elements[self.left_menu_item]
                action = element.event(event)
                return self.handle_action(action)
        return True, True

    def navigate_back(self):
        if self.right_menu_status:
            self.right_menu_status = False
        elif self.menu_stack:
            self.current_menu = self.menu_stack.pop()
            self.left_menu_item = self.menu_item_stack.pop()
            self.right_menu_item = 0
            self.right_menu_status = False
            self.left_elements = self.left_elements_cache.get(self.current_menu, [])
        else:
            return True, not (self.__class__.__name__ == 'PauseMenu')
        return True, True

    def handle_action(self, action):
        if action == 1:
            return True, False
        elif action == 0:
            return False, True
        elif isinstance(action, str) and action in self.menu:
            if self.current_menu != action:
                self.menu_stack.append(self.current_menu)
                self.menu_item_stack.append(self.left_menu_item)
            self.current_menu = action
            self.left_menu_item = 0
            self.right_menu_item = 0
            self.right_menu_status = False
            self.left_elements = self.left_elements_cache.get(self.current_menu, [])
        return True, True


class MainMenu(BaseMenu):
    def __init__(self, screen, font, bold_font):
        super().__init__(screen, font, bold_font)
        self.menu = {
            "main menu": {
                "play": {"type": "button", "value": 1},
                "options": {"type": "button", "value": "options"},
                "credits": {"type": "button", "value": "credits"},
                "quit": {"type": "button", "value": 0},
            },
            "options": {
                "gameplay": {"type": "button", "value": "gameplay", "right_menu": True},
                "display": {"type": "button", "value": "display", "right_menu": True},
                "sound": {"type": "button", "value": "sound", "right_menu": True},
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
        self.current_menu = "main menu"
        self.create_elements(self.menu)

class PauseMenu(BaseMenu):
    def __init__(self, screen, font, bold_font):
        super().__init__(screen, font, bold_font)
        self.menu = {
            "pause menu": {
                "resume": {"type": "button", "value": 1},
                "options": {"type": "button", "value": "options"},
                "quit": {"type": "button", "value": 0},
            },
            "options": {
                "gameplay": {"type": "button", "value": "gameplay", "right_menu": True},
                "display": {"type": "button", "value": "display", "right_menu": True},
                "sound": {"type": "button", "value": "sound", "right_menu": True},
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
        self.current_menu = "pause menu"
        self.create_elements(self.menu)
