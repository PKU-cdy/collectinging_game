import pygame
from game_config import *

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hover = False
        self.font = pygame.font.SysFont("SimHei", 30)

    def draw(self, screen):
        # 根据悬停状态选择颜色
        color = BUTTON_HOVER if self.hover else BUTTON_NORMAL
        pygame.draw.rect(screen, color, self.rect)

        # 绘制文字
        text_surface = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


def draw_text(screen, text, x, y, font_size=30):
    font = pygame.font.SysFont("SimHei", font_size)
    text_surface = font.render(text, True, TEXT_COLOR)
    screen.blit(text_surface, (x, y))


def draw_background(screen):
    screen.fill(SKY_COLOR)
    # 绘制地面
    pygame.draw.rect(
        screen,
        GROUND_COLOR,
        (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
    )