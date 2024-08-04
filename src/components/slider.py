import pygame
import settings

class Slider:
    ARROW_SIZE = (20, 20)
    OPTION_WIDTH = 220
    BAR_HEIGHT = 5
    PADDING = 20

    def __init__(self, screen, pos, name, range_values, action, font, font_size, color, hover_color, rect_hover_color):
        self.screen = screen
        self.x_pos, self.y_pos = pos
        self.action = action
        self.font = font
        self.font_size = font_size
        self.color = color
        self.hover_color = hover_color
        self.rect_hover_color = rect_hover_color
        self.name = name.title()
        self.range = range_values
        self.current_value = getattr(settings, self.action)
        self.bar_width = 150

        self.right_arrow, self.right_arrow_hover = self.load_arrows()
        self.left_arrow = pygame.transform.flip(self.right_arrow, True, False)
        self.left_arrow_hover = pygame.transform.flip(self.right_arrow_hover, True, False)

        self.update_texts(self.color)
        self.update_rect()

    def load_arrows(self):
        right_arrow = self.load_and_scale_image("assets/images/ui/right_arrow_white.png", self.ARROW_SIZE)
        right_arrow_hover = self.load_and_scale_image("assets/images/ui/right_arrow_black.png", self.ARROW_SIZE)
        return right_arrow, right_arrow_hover

    def draw_arrows(self, hover=False):
        left_arrow = self.left_arrow_hover if hover else self.left_arrow
        right_arrow = self.right_arrow_hover if hover else self.right_arrow
        self.screen.blit(left_arrow, self.left_arrow_rect)
        self.screen.blit(right_arrow, self.right_arrow_rect)

    def load_and_scale_image(self, path, size):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)

    def update_texts(self, color):
        self.name_text, self.name_rect = self.font.render(self.name, color, size=self.font_size)

    def update_rect(self):
        self.name_rect.midleft = (self.x_pos + self.PADDING, self.y_pos)
        self.option_rect = pygame.Rect(0, 0, self.OPTION_WIDTH, self.name_rect.height)
        self.option_rect.midright = (self.screen.get_width() - self.PADDING, self.y_pos)
        self.bar_rect = pygame.Rect(0, 0, self.bar_width, self.BAR_HEIGHT)
        self.bar_rect.center = self.option_rect.center
        self.knob_rect = pygame.Rect(0, 0, 5, 20)
        self.update_knob_position()
        self.left_arrow_rect = self.left_arrow.get_rect(midleft=(self.option_rect.left, self.option_rect.centery))
        self.right_arrow_rect = self.right_arrow.get_rect(midright=(self.option_rect.right, self.option_rect.centery))
        self.rect = pygame.Rect(
            min(self.name_rect.left, self.left_arrow_rect.left) - self.PADDING,
            self.y_pos - 35,
            max(self.name_rect.right, self.right_arrow_rect.right) - min(self.name_rect.left, self.left_arrow_rect.left) + self.PADDING * 2,
            70
        )

    def update_knob_position(self):
        if self.range:
            position_ratio = (self.current_value - min(self.range)) / (max(self.range) - min(self.range))
            self.knob_rect.centerx = self.bar_rect.left + int(position_ratio * self.bar_width)
            self.knob_rect.centery = self.bar_rect.centery

    def update(self):
        self.screen.blit(self.name_text, self.name_rect)

    def check_for_input(self, position):
        return self.rect.collidepoint(position)

    def change_style(self, hover=False):
        color, rect_color = (self.hover_color, self.rect_hover_color) if hover else (self.color, None)
        self.update_texts(color)
        self.update_rect()
        if rect_color:
            pygame.draw.rect(self.screen, rect_color, self.rect)
        self.draw_arrows(hover)
        pygame.draw.rect(self.screen, color, self.bar_rect)
        pygame.draw.rect(self.screen, color, self.knob_rect)
        self.update()
        pygame.draw.line(
            self.screen, color,
            (self.name_rect.right + 10, self.name_rect.centery),
            (self.option_rect.left - 10, self.option_rect.centery),
            1
        )

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.check_for_input(event.pos):
            self.change_value()
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RIGHT, pygame.K_RETURN]:
                self.change_value(1)
                return self.action
            elif event.key == pygame.K_LEFT:
                self.change_value(-1)
                return self.action

    def change_value(self, direction=1):
        new_value = self.current_value + direction
        if min(self.range) <= new_value <= max(self.range):
            self.current_value = new_value
            setattr(settings, self.action, self.current_value)
            self.update_knob_position()
