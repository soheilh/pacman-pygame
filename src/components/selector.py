import pygame
import settings

class Selector:
    ARROW_SIZE = (20, 20)
    MAX_OPTION_WIDTH = 220
    PADDING = 20

    def __init__(self, screen, pos, name, options, action, font, font_size, color, hover_color, rect_hover_color):
        self.screen = screen
        self.x_pos, self.y_pos = pos
        self.action = action
        self.font = font
        self.font_size = font_size
        self.color = color
        self.hover_color = hover_color
        self.rect_hover_color = rect_hover_color
        self.name = name.title()
        self.options = options
        self.current_option = self.options.index(getattr(settings, self.action))

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
        self.option_text, self.option_text_rect = self.font.render(str(self.options[self.current_option]).title(), color, size=self.font_size)

    def update_rect(self):
        self.name_rect.midleft = (self.x_pos + self.PADDING, self.y_pos)
        self.option_rect = pygame.Rect(0, 0, self.MAX_OPTION_WIDTH, self.option_text.get_height())
        self.option_rect.midright = (self.screen.get_width() - self.PADDING, self.y_pos)
        self.option_text_rect.center = self.option_rect.center
        self.left_arrow_rect = self.left_arrow.get_rect(midleft=(self.option_rect.left, self.option_rect.centery))
        self.right_arrow_rect = self.right_arrow.get_rect(midright=(self.option_rect.right, self.option_rect.centery))
        self.rect = pygame.Rect(
            min(self.name_rect.left, self.left_arrow_rect.left) - self.PADDING,
            self.y_pos - 35,
            max(self.name_rect.right, self.right_arrow_rect.right) - min(self.name_rect.left, self.left_arrow_rect.left) + self.PADDING * 2,
            70
        )

    def update(self):
        self.screen.blit(self.name_text, self.name_rect)
        self.screen.blit(self.option_text, self.option_text_rect)

    def check_for_input(self, position):
        return self.rect.collidepoint(position)

    def change_style(self, hover=False):
        color = self.hover_color if hover else self.color
        rect_color = self.rect_hover_color if hover else None
        self.update_texts(color)
        self.update_rect()
        if rect_color:
            pygame.draw.rect(self.screen, rect_color, self.rect)
        self.draw_arrows(hover)
        self.update()
        pygame.draw.line(
            self.screen, color,
            (self.name_rect.right + 10, self.name_rect.centery),
            (self.option_rect.left - 10, self.option_rect.centery),
            1
        )

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.check_for_input(event.pos):
            self.change_option()
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RIGHT, pygame.K_RETURN]:
                self.change_option(1)
            elif event.key == pygame.K_LEFT:
                self.change_option(-1)

    def change_option(self, direction=1):
        self.current_option = (self.current_option + direction) % len(self.options)
        self.update_texts(self.color)
        setattr(settings, self.action, self.options[self.current_option])
