import pygame
import sys
from game_config import *
from game_utils import Button, draw_text, draw_background
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("接粮食小游戏")

        # 初始化按钮
        self.pause_button = Button(
            SCREEN_WIDTH - BUTTON_WIDTH - BUTTON_MARGIN,
            BUTTON_MARGIN,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "暂停"
        )

        self.restart_button = Button(
            SCREEN_WIDTH - BUTTON_WIDTH - BUTTON_MARGIN,
            BUTTON_MARGIN + BUTTON_HEIGHT + BUTTON_MARGIN,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "重新开始"
        )

        # 初始化玩家
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - GROUND_HEIGHT - 60)


        # 游戏状态
        self.is_paused = False
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time_when_paused = 0

        # 游戏主循环控制
        self.running = True
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # 暂停按钮点击
                if self.pause_button.is_clicked(mouse_pos):
                    self.toggle_pause()
                # 重新开始按钮点击
                elif self.restart_button.is_clicked(mouse_pos):
                    self.restart_game()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            # 记录暂停时已流逝的时间
            self.elapsed_time_when_paused = (pygame.time.get_ticks() - self.start_time) // 1000
            self.pause_button.text = "继续"
        else:
            # 恢复暂停时重置开始时间
            self.start_time = pygame.time.get_ticks() - (self.elapsed_time_when_paused * 1000)
            self.pause_button.text = "暂停"

    def restart_game(self):
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time_when_paused = 0
        self.is_paused = False
        self.pause_button.text = "暂停"

    def update(self):
        # 检查游戏是否结束
         # 添加键盘控制逻辑
        if not self.is_paused:
            keys = pygame.key.get_pressed()
            # 左右方向键或A/D键控制移动
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.move(-self.player.speed)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.move(self.player.speed)

        if self.get_remaining_time() <= 0 and not self.is_paused:
            draw_text(self.screen, "游戏结束", SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(2000)
            self.restart_game()

    def get_remaining_time(self):
        if not self.is_paused:
            current_time = pygame.time.get_ticks()
            elapsed_seconds = (current_time - self.start_time) // 1000
            return max(GAME_DURATION - elapsed_seconds, 0)
        else:
            return max(GAME_DURATION - self.elapsed_time_when_paused, 0)

    def draw(self):
        draw_background(self.screen)

        # 绘制倒计时
        remaining_time = self.get_remaining_time()
        draw_text(self.screen, f"剩余时间: {remaining_time}秒", 20, 20)

        # 绘制按钮
        self.pause_button.draw(self.screen)
        self.restart_button.draw(self.screen)

        # 绘制暂停提示
        if self.is_paused:
            # 半透明遮罩
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 128))
            self.screen.blit(s, (0, 0))
            # 暂停文字
            draw_text(self.screen, "游戏已暂停", SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2, 40)

        # 绘制玩家
        self.player.draw(self.screen)
        
        # 保留屏幕刷新
        pygame.display.flip()


    def run(self):
        while self.running:
            self.handle_events()
            mouse_pos = pygame.mouse.get_pos()
            self.pause_button.check_hover(mouse_pos)
            self.restart_button.check_hover(mouse_pos)

            self.update()
            self.draw()

            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()