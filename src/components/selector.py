import pygame
import settings

class Selector:
    def __init__(self, pos, name, options, action, font, bold_font, color, hover_color, rect_hover_color):
        self.x_pos, self.y_pos = pos
        self.action = action
        self.font = font
        self.bold_font = bold_font
        self.color = color
        self.hover_color = hover_color
        self.rect_hover_color = rect_hover_color
        self.name = name.title()
        self.options = [option for option in options]
        self.current_option = self.options.index(getattr(settings, self.action))
        self.max_option_width = 150
        self.update_texts(self.color)
        self.update_rect()

    def update_texts(self, color):
        self.name_text = self.font.render(self.name, True, color)
        self.option_text = self.font.render(str(self.options[self.current_option]).title(), True, color)

        # Center the name text
        self.name_rect = self.name_text.get_rect(topleft=(self.x_pos, self.y_pos))

        # Set the position for the option text
        option_x = self.x_pos + 600  # Fixed x position for the option text
        self.option_rect = pygame.Rect(0, 0, self.max_option_width, self.option_text.get_height())
        self.option_rect.center = (option_x, self.y_pos + self.name_rect.height // 2)

        # Center the option text within the option_rect
        self.option_text_rect = self.option_text.get_rect(center=self.option_rect.center)

    def update_rect(self):
        # Create a rect that includes both text areas plus some padding
        self.rect = pygame.Rect(min(self.name_rect.left, self.option_rect.left) - 20,
                                min(self.name_rect.top, self.option_rect.top) - 10,
                                max(self.name_rect.right, self.option_rect.right) - min(self.name_rect.left, self.option_rect.left) + 40,
                                max(self.name_rect.bottom, self.option_rect.bottom) - min(self.name_rect.top, self.option_rect.top) + 20)
    
    def update(self, screen):
        screen.blit(self.name_text, self.name_rect)
        screen.blit(self.option_text, self.option_text_rect)

    def check_for_input(self, position):
        return self.rect.collidepoint(position)

    def change_style(self, screen):
        self.update_texts(self.hover_color)
        pygame.draw.rect(screen, self.rect_hover_color, self.rect)  # Redraw the rect with hover color
        screen.blit(self.name_text, self.name_rect)
        screen.blit(self.option_text, self.option_text_rect)
        # Draw the horizontal line between the two text elements in hover color
        pygame.draw.line(screen, self.hover_color, 
                         (self.name_rect.right + 10, self.name_rect.centery),
                         (self.option_rect.left - 10, self.option_rect.centery),
                         1)

    def reset_style(self, screen):
        self.update_texts(self.color)
        screen.blit(self.name_text, self.name_rect)
        screen.blit(self.option_text, self.option_text_rect)
        # Draw the horizontal line between the two text elements in default color
        pygame.draw.line(screen, self.color, 
                         (self.name_rect.right + 10, self.name_rect.centery),
                         (self.option_rect.left - 10, self.option_rect.centery),
                         1)

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
        self.update_texts(self.color)
        new_value = self.options[self.current_option]
        setattr(settings, self.action, new_value)
