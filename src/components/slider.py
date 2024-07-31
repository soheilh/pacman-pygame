import pygame
import settings

class Slider:
    RIGHT_ARROW_PATH = "assets/images/ui/right_arrow_white.png"
    RIGHT_ARROW_HOVER_PATH = "assets/images/ui/right_arrow_black.png"
    ARROW_SIZE = (20, 20)

    def __init__(self, screen, pos, padding, name, range_values, action, font, font_size, color, hover_color, rect_hover_color):
        self.screen = screen
        self.x_pos, self.y_pos = pos
        self.padding = padding
        self.action = action
        self.font = font
        self.font_size = font_size
        self.color = color
        self.hover_color = hover_color
        self.rect_hover_color = rect_hover_color
        self.name = name.title()
        self.range = range_values
        self.current_value = getattr(settings, self.action)
        self.option_width = 220
        self.bar_width = 150
        self.bar_height = 5

        self.right_arrow = self.load_and_scale_image(self.RIGHT_ARROW_PATH, self.ARROW_SIZE)
        self.left_arrow = pygame.transform.flip(self.right_arrow, True, False)
        self.right_arrow_hover = self.load_and_scale_image(self.RIGHT_ARROW_HOVER_PATH, self.ARROW_SIZE)
        self.left_arrow_hover = pygame.transform.flip(self.right_arrow_hover, True, False)

        self.update_texts(self.color)
        self.update_rect()

    def load_and_scale_image(self, path, size):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)

    def update_texts(self, color):
        self.name_text, self.name_rect = self.font.render(self.name, color, size=self.font_size)

    def update_rect(self):
        self.name_rect.topleft = (self.x_pos + self.padding, self.y_pos)
        self.option_rect = pygame.Rect(0, 0, self.option_width, self.name_rect.height)
        self.option_rect.topright = (self.screen.get_width() - self.padding, self.y_pos)
        self.bar_rect = pygame.Rect(0, 0, self.bar_width, self.bar_height)
        self.bar_rect.center = self.option_rect.center
        self.knob_rect = pygame.Rect(0, 0, 5, 20)
        self.update_knob_position()
        self.left_arrow_rect = self.left_arrow.get_rect(midleft=(self.option_rect.left, self.option_rect.centery))
        self.right_arrow_rect = self.right_arrow.get_rect(midright=(self.option_rect.right, self.option_rect.centery))

        self.rect = pygame.Rect(
            min(self.name_rect.left, self.option_rect.left) - 20,
            min(self.name_rect.top, self.option_rect.top) - 10,
            max(self.name_rect.right, self.option_rect.right) - min(self.name_rect.left, self.option_rect.left) + 40,
            max(self.name_rect.bottom, self.option_rect.bottom) - min(self.name_rect.top, self.option_rect.top) + 20
        )

    def update_knob_position(self):
        if self.range:
            position_ratio = (self.current_value - min(self.range)) / (max(self.range) - min(self.range))
            self.knob_rect.centerx = self.bar_rect.left + int(position_ratio * self.bar_width)
            self.knob_rect.centery = self.bar_rect.centery

    def update(self):
        self.screen.blit(self.name_text, self.name_rect)

    def draw_arrows(self):
        self.screen.blit(self.left_arrow, self.left_arrow_rect)
        self.screen.blit(self.right_arrow, self.right_arrow_rect)

    def draw_hover_arrows(self):
        self.screen.blit(self.left_arrow_hover, self.left_arrow_rect)
        self.screen.blit(self.right_arrow_hover, self.right_arrow_rect)

    def check_for_input(self, position):
        return self.rect.collidepoint(position)

    def change_style(self):
        self.update_texts(self.hover_color)
        self.update_rect()
        pygame.draw.rect(self.screen, self.rect_hover_color, self.rect)
        self.draw_hover_arrows()
        pygame.draw.rect(self.screen, self.hover_color, self.bar_rect)
        pygame.draw.rect(self.screen, self.hover_color, self.knob_rect)
        pygame.draw.line(
            self.screen, self.hover_color,
            (self.name_rect.right + 10, self.name_rect.centery),
            (self.option_rect.left - 10, self.option_rect.centery),
            1
        )

    def reset_style(self):
        self.update_texts(self.color)
        self.update_rect()
        self.draw_arrows()
        pygame.draw.rect(self.screen, self.color, self.bar_rect)
        pygame.draw.rect(self.screen, self.color, self.knob_rect)
        pygame.draw.line(
            self.screen, self.color,
            (self.name_rect.right + 10, self.name_rect.centery),
            (self.option_rect.left - 10, self.option_rect.centery),
            1
        )

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.set_value(1)
            elif event.key == pygame.K_LEFT:
                self.set_value(-1)

    def set_value(self, direction):
        new_value = min(max(self.current_value + direction, min(self.range)), max(self.range))
        self.current_value = new_value
        self.update_knob_position()
        setattr(settings, self.action, self.current_value)
