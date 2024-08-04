import pygame
import pygame.freetype

class Button:
    def __init__(self, screen, pos, text_input, action, font, bold_font, font_size, color, hover_color, rect_hover_color):
        self.screen = screen
        self.x_pos, self.y_pos = pos
        self.action = action
        self.font = font
        self.bold_font = bold_font
        self.font_size = font_size
        self.color = color
        self.hover_color = hover_color
        self.rect_hover_color = rect_hover_color
        self.text_input = text_input.upper()
        self.update_text(self.font, self.color)

    def update_text(self, font, color):
        self.text, self.rect = font.render(self.text_input, color, size=self.font_size)
        self.rect.topleft = (self.x_pos, self.y_pos)

    def update(self):
        self.screen.blit(self.text, self.rect)
    
    def check_for_input(self, position):
        return self.rect.collidepoint(position)
    
    def change_style(self, hover=False):
        font, color, rect_color = (self.bold_font, self.hover_color, self.rect_hover_color) if hover else (self.font, self.color, None)
        self.update_text(font, color)
        if rect_color:
            pygame.draw.rect(self.screen, rect_color, self.rect.inflate(20, 20))

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.check_for_input(event.pos):
            return self.action
        if event.type == pygame.KEYDOWN and event.key in [pygame.K_RIGHT, pygame.K_RETURN]:
            return self.action
