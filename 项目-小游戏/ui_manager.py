import pygame
from game_config import *
from game_utils import Button, draw_text

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = {
            'pause': Button(SCREEN_WIDTH - BUTTON_WIDTH - BUTTON_MARGIN, BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT, "暂停"),
            'restart': Button(SCREEN_WIDTH - BUTTON_WIDTH - BUTTON_MARGIN, BUTTON_MARGIN*2 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, "重新开始"),
            'quit': Button(SCREEN_WIDTH//2 - BUTTON_WIDTH - 20, SCREEN_HEIGHT//2 + 50, BUTTON_WIDTH, BUTTON_HEIGHT, "退出游戏"),
            'replay': Button(SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT//2 + 50, BUTTON_WIDTH, BUTTON_HEIGHT, "重新开始")
        }

    def draw_all(self, game_state):
        #根据游戏状态决定按钮字样
        self.buttons['pause'].text = "继续" if game_state.is_paused else "暂停"

        # 绘制暂停界面
        if game_state.is_paused:
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 128))
            self.screen.blit(s, (0, 0))
            draw_text(self.screen, "游戏已暂停", SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2, 40)

        # 绘制结算界面
        if game_state.game_over:
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            self.screen.blit(s, (0, 0))
            draw_text(self.screen, "游戏结束", SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 - 50, 40)
            draw_text(self.screen, f"最终得分: {game_state.score}", SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2, 30)
            self.buttons['quit'].draw(self.screen)
            self.buttons['replay'].draw(self.screen)

        # 添加中央积分显示
        draw_text(
            self.screen,
            f"积分: {game_state.score}",
            SCREEN_WIDTH // 2,
            20,
            36  # 仅保留font_size参数
        )

        # 按钮绘制到最后，确保在所有界面之上
        self.buttons['pause'].draw(self.screen)
        self.buttons['restart'].draw(self.screen)
        # 添加倒计时显示
        draw_text(self.screen, f"剩余时间: {game_state.get_remaining_time()}秒", 20, 20)



    def handle_click(self, mouse_pos, game_state):
        if self.buttons['pause'].is_clicked(mouse_pos):
            game_state.toggle_pause()
        elif self.buttons['restart'].is_clicked(mouse_pos):
            game_state.restart()
        elif game_state.game_over:
            if self.buttons['quit'].is_clicked(mouse_pos):
                return False  # 退出游戏
            elif self.buttons['replay'].is_clicked(mouse_pos):
                game_state.restart()
        return True