import pygame
from components.button import Button
from components.selector import Selector
from components.slider import Slider
import settings

class MainMenu:
    ITEM_VERTICAL_SPACING = 70
    MAX_VISIBLE_ITEMS = 7

    def __init__(self, screen, font, bold_font):
        """Initialize the MainMenu with screen, font, and bold_font."""
        self.screen = screen
        self.font = font
        self.bold_font = bold_font
        self.current_menu = "main menu"
        self.menu_stack = []
        self.menu_item_stack = []
        self.left_menu_item = 0
        self.right_menu_item = 0
        self.right_menu_status = False
        self.scroll_offset = 0

        # Create surfaces for left and right menus
        self.left_menu_surface = pygame.Surface((self.screen.get_width() / 4, self.MAX_VISIBLE_ITEMS * self.ITEM_VERTICAL_SPACING))
        self.right_menu_surface = pygame.Surface((self.screen.get_width() / 2, self.MAX_VISIBLE_ITEMS * self.ITEM_VERTICAL_SPACING))
        self.right_menu_content_surface = pygame.Surface((self.right_menu_surface.get_width(), 0))

        # Define the main menu structure
        self.main_menu = {
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
        self.create_elements()

    def create_elements(self):
        """Create UI elements for the current menu."""
        self.left_elements = []
        self.right_elements = {}
        menu_options = self.main_menu.get(self.current_menu, {})

        for i, title in enumerate(menu_options):
            pos = (50, self.left_menu_surface.get_height() / 2 + i * 40)
            self.left_elements.append(Button(screen=self.left_menu_surface, text_input=title, action=menu_options[title]["value"], pos=pos, font=self.font, bold_font=self.bold_font, font_size=26, color=settings.WHITE, hover_color=settings.BRIGHT_WHITE, rect_hover_color=None))

            item = menu_options.get(title, {})
            if item["type"] == "button" and item.get("right_menu", False) and item["value"] in self.main_menu:
                submenu = self.main_menu[item["value"]]
                if submenu:
                    self.right_elements[title] = []
                    for j, (text, action) in enumerate(submenu.items()):
                        pos = (0, j * self.ITEM_VERTICAL_SPACING + 35)
                        common_args = {'pos': pos, 'screen': self.right_menu_content_surface, 'font': self.font, 'font_size': 24, 'color': settings.WHITE, 'hover_color': settings.BLACK, 'rect_hover_color': settings.WHITE}
                        if action["type"] == "selector":
                            self.right_elements[title].append((Selector(name=text, options=action["options"], action=action["value"], **common_args), action))
                        elif action["type"] == "slider":
                            self.right_elements[title].append((Slider(name=text, range_values=action["options"], action=action["value"], **common_args), action))
                        elif action["type"] == "button":
                            self.right_elements[title].append((Button(text_input=text, bold_font=self.bold_font, action=action["value"], **common_args), action))

    def draw(self, screen):
        """Draw the current menu and its elements on the screen."""
        screen.fill(settings.MENU_BG_COLOR)
        self.left_menu_surface.fill(settings.MENU_BG_COLOR)
        title_text, title_text_rect = self.bold_font.render(self.current_menu.upper(), settings.WHITE, size=70)
        title_text_rect.topleft = (50, self.left_menu_surface.get_height() / 4)
        self.left_menu_surface.blit(title_text, title_text_rect)

        for i, element in enumerate(self.left_elements):
            if i == self.left_menu_item:
                element.change_style(True)
            else:
                element.change_style(False)
            element.update()
        self.draw_right_menu()
        self.screen.blit(self.left_menu_surface, (0, self.screen.get_height() / 4))

    def draw_right_menu(self):
        """Draw the right-side menu elements."""
        self.right_menu_surface.fill(settings.MENU_BG_COLOR)
        right_menu_key = self.left_elements[self.left_menu_item].action
        if right_menu_key in self.right_elements:
            content_height = len(self.right_elements[right_menu_key]) * self.ITEM_VERTICAL_SPACING
            self.right_menu_content_surface = pygame.transform.scale(self.right_menu_content_surface, (self.right_menu_surface.get_width(), content_height))
            self.right_menu_content_surface.fill(settings.MENU_BG_COLOR)

            if self.right_menu_status:
                visible_elements = self.right_elements[right_menu_key][self.scroll_offset:self.scroll_offset + self.MAX_VISIBLE_ITEMS]
                for i, (element, _) in enumerate(visible_elements):
                    element.screen = self.right_menu_content_surface
                    element.change_style(i == (self.right_menu_item - self.scroll_offset))
                    element.update()
            else:
                for element, _ in self.right_elements[right_menu_key][:self.MAX_VISIBLE_ITEMS]:
                    element.screen = self.right_menu_content_surface
                    element.change_style(False)
                    element.update()
            if self.right_menu_content_surface.get_height() <= self.right_menu_surface.get_height():
                self.right_menu_surface.blit(self.right_menu_content_surface, (0, (self.right_menu_surface.get_height() - self.right_menu_content_surface.get_height()) / 2 - self.scroll_offset * self.ITEM_VERTICAL_SPACING))
            else:
                self.right_menu_surface.blit(self.right_menu_content_surface, (0, -self.scroll_offset * self.ITEM_VERTICAL_SPACING))
        self.screen.blit(self.right_menu_surface, (self.screen.get_width() / 4, self.screen.get_height() / 4))

    def events(self, event):
        """Handle user input events."""
        if event.type == pygame.KEYDOWN:
            if self.right_menu_status:
                right_menu_key = self.left_elements[self.left_menu_item].action
                if right_menu_key in self.right_elements:
                    num_elements = len(self.right_elements[right_menu_key])
                    if event.key == pygame.K_UP:
                        self.right_menu_item = (self.right_menu_item - 1) % num_elements
                        if self.right_menu_item < self.scroll_offset:
                            self.scroll_offset = self.right_menu_item
                        elif self.right_menu_item >= self.scroll_offset + self.MAX_VISIBLE_ITEMS:
                            self.scroll_offset = self.right_menu_item - self.MAX_VISIBLE_ITEMS + 1

                    elif event.key == pygame.K_DOWN:
                        self.right_menu_item = (self.right_menu_item + 1) % num_elements
                        if self.right_menu_item < self.scroll_offset:
                            self.scroll_offset = self.right_menu_item
                        elif self.right_menu_item >= self.scroll_offset + self.MAX_VISIBLE_ITEMS:
                            self.scroll_offset = self.right_menu_item - self.MAX_VISIBLE_ITEMS + 1

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
                    if left_action_key in self.right_elements and self.main_menu[self.current_menu][left_action_key].get("right_menu", False):
                        self.right_menu_status = True
                        self.right_menu_item = 0
                        self.scroll_offset = 0
                    else:
                        element = self.left_elements[self.left_menu_item]
                        action = element.event(event)
                        return self.handle_action(action)
                elif event.key == pygame.K_ESCAPE:
                    if self.right_menu_status:
                        self.right_menu_status = False
                    elif self.menu_stack:
                        self.current_menu = self.menu_stack.pop()
                        self.left_menu_item = self.menu_item_stack.pop()
                        self.right_menu_item = 0
                        self.right_menu_status = False
                        self.create_elements()
        return True, True

    def handle_action(self, action):
        """Process menu actions based on the selected option."""
        if action == 1:
            return True, False
        elif action == 0:
            return False, True
        elif isinstance(action, str) and action in self.main_menu:
            if self.current_menu != action:
                self.menu_stack.append(self.current_menu)
                self.menu_item_stack.append(self.left_menu_item)
            self.current_menu = action
            self.left_menu_item = 0
            self.right_menu_item = 0
            self.right_menu_status = False
            self.create_elements()
        return True, True
