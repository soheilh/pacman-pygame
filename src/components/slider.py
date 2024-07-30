import pygame
import settings

class Slider:
    def __init__(self, pos, name, options, action, font, bold_font, color, hover_color, rect_hover_color):
        self.x_pos, self.y_pos = pos
        self.action = action
        self.font = font
        self.bold_font = bold_font
        self.color = color
        self.hover_color = hover_color
        self.rect_hover_color = rect_hover_color
        self.name = name.title()
        self.range = options
        self.current_value = getattr(settings, self.action)
        self.bar_width = 150
        self.bar_height = 5
        self.update_texts(self.color)
        self.update_rect()

    def update_texts(self, color):
        self.name_text = self.font.render(self.name, True, color)
        self.name_rect = self.name_text.get_rect(topleft=(self.x_pos, self.y_pos))

    def update_rect(self):
        self.bar_rect = pygame.Rect(0, 0, self.bar_width, self.bar_height)
        self.bar_rect.center = (self.x_pos + 600, self.y_pos + self.name_rect.height / 2)
        self.knob_rect = pygame.Rect(0, 0, 5, 20)
        self.update_knob_position()

        # Create a rect that includes the name text and the slider bar with some padding
        self.rect = pygame.Rect(min(self.name_rect.left, self.bar_rect.left) - 20,
                                min(self.name_rect.top, self.bar_rect.top) - 10,
                                max(self.name_rect.right, self.bar_rect.right) - min(self.name_rect.left, self.bar_rect.left) + 40,
                                max(self.name_rect.bottom, self.bar_rect.bottom) - min(self.name_rect.top, self.bar_rect.top) + 20)

    def update_knob_position(self):
        if self.range:  # Ensure the range is not empty to avoid division by zero
            position_ratio = (self.current_value - min(self.range)) / (max(self.range) - min(self.range))
            self.knob_rect.centerx = self.bar_rect.left + int(position_ratio * self.bar_width)
            self.knob_rect.centery = self.bar_rect.centery

    def update(self, screen):
        screen.blit(self.name_text, self.name_rect)

    def check_for_input(self, position):
        return self.rect.collidepoint(position)

    def change_style(self, screen):
        self.update_texts(self.hover_color)
        pygame.draw.rect(screen, self.rect_hover_color, self.rect)  # Highlight the rect on hover
        screen.blit(self.name_text, self.name_rect)
        pygame.draw.rect(screen, self.hover_color, self.bar_rect)
        pygame.draw.rect(screen, self.hover_color, self.knob_rect)
        # Draw the horizontal line between the two text elements in hover color
        pygame.draw.line(screen, self.hover_color, 
                         (self.name_rect.right + 10, self.name_rect.centery),
                         (self.bar_rect.left - 10, self.bar_rect.centery),
                         1)

    def reset_style(self, screen):
        self.update_texts(self.color)
        screen.blit(self.name_text, self.name_rect)
        pygame.draw.rect(screen, self.color, self.bar_rect)
        pygame.draw.rect(screen, self.color, self.knob_rect)
        # Draw the horizontal line between the two text elements in default color
        pygame.draw.line(screen, self.color, 
                         (self.name_rect.right + 10, self.name_rect.centery),
                         (self.bar_rect.left - 10, self.bar_rect.centery),
                         1)

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
