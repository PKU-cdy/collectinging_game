import pygame
import sys
from game_config import *
from game_utils import draw_background, draw_world_elements
from ui_manager import UIManager
from game_state import GameState

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("接粮食小游戏")
        self.clock = pygame.time.Clock()
        self.running = True

        # 初始化模块
        self.state = GameState()
        self.ui = UIManager(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.ui.handle_click(pygame.mouse.get_pos(), self.state):
                    self.running = False
            elif event.type == pygame.KEYDOWN:
                # P键暂停/恢复游戏
                if event.key == pygame.K_p:
                    self.state.is_paused = not self.state.is_paused
        

    def run(self):
        while self.running:
            # 事件处理
            self.handle_events()
            
            # 获取鼠标位置并更新按钮悬停状态
            mouse_pos = pygame.mouse.get_pos()
            self.ui.buttons['pause'].check_hover(mouse_pos)
            self.ui.buttons['restart'].check_hover(mouse_pos)
            
            # 游戏状态更新
            self.state.update()
            
            # 绘制逻辑（严格按照从下到上的层级顺序）
            draw_background(self.screen)          # 1. 背景
            draw_world_elements(self.screen, self.state.grain_bin_rect)  # 2. 世界元素
            self.state.player.draw(self.screen)    # 3. 玩家
            self.ui.draw_all(self.state)           # 4. UI元素
            
            # 刷新屏幕
            pygame.display.flip()
            
            # 控制帧率
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()