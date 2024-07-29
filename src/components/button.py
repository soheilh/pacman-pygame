import pygame

class Button:
    def __init__(self, pos, text_input, action, font, color, hover_color, rect_hover_color):
        self.x_pos, self.y_pos = pos
        self.action = action
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.rect_hover_color = rect_hover_color
        self.text_input = text_input.upper()
        self.text = self.font.render(self.text_input, True, self.color)
        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        
    def update(self, screen):
        screen.blit(self.text, self.rect)
    
    def check_for_input(self, position):
        return self.rect.collidepoint(position)
    
    def change_style(self, screen):
        pygame.draw.rect(screen, self.rect_hover_color, self.rect.inflate(20, 10))
        self.text = self.font.render(self.text_input, True, self.hover_color)

    def reset_style(self):
        self.text = self.font.render(self.text_input, True, self.color)

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.check_for_input(event.pos):
            return self.action
        if event.type == pygame.KEYDOWN and event.key in [pygame.K_RIGHT, pygame.K_RETURN]:
            return self.action
