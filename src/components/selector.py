import pygame

class Selector:
    def __init__(self, pos, name, options, action, font, color, hover_color, rect_hover_color):
        self.x_pos, self.y_pos = pos
        self.action = action
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.rect_hover_color = rect_hover_color
        self.name = name
        self.options = [str(option) for option in options]
        self.current_option = 0
        self.update_texts()

    def update_texts(self):
        self.name_text = self.font.render(self.name, True, self.color)
        self.name_rect = self.name_text.get_rect(center=(self.x_pos - 150, self.y_pos))
        self.option_text = self.font.render(self.options[self.current_option], True, self.color)
        self.option_rect = self.option_text.get_rect(center=(self.x_pos + 150, self.y_pos))

    def update(self, screen):
        screen.blit(self.name_text, self.name_rect)
        screen.blit(self.option_text, self.option_rect)

    def check_for_input(self, position):
        return self.name_rect.collidepoint(position) or self.option_rect.collidepoint(position)

    def change_style(self, screen):
        pygame.draw.rect(screen, self.rect_hover_color, self.name_rect.inflate(20, 10))
        self.name_text = self.font.render(self.name, True, self.hover_color)

    def reset_style(self):
        self.name_text = self.font.render(self.name, True, self.color)

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.check_for_input(event.pos):
            self.change_option()
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RIGHT, pygame.K_RETURN]:
                self.change_option(1)
            elif event.key == pygame.K_LEFT:
                self.change_option(-1)

    def change_option(self, direction=1):
        self.current_option = (self.current_option + direction) % len(self.options)
        self.update_texts()
