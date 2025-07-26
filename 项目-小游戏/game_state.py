import pygame
from game_config import GAME_DURATION, SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT
from player import Player

class GameState:
    def __init__(self):
        self.is_paused = False
        self.game_over = False
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time_when_paused = 0
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - GROUND_HEIGHT - 60)

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.elapsed_time_when_paused = (pygame.time.get_ticks() - self.start_time) // 1000
        else:
            self.start_time = pygame.time.get_ticks() - (self.elapsed_time_when_paused * 1000)

    def restart(self):
        self.__init__()  # 重置所有状态

    def update(self):
        if not self.is_paused and not self.game_over:
            # 玩家移动逻辑
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.move(-self.player.speed)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.move(self.player.speed)

        # 检查游戏结束
        if self.get_remaining_time() <= 0 and not self.is_paused:
            self.game_over = True

    def get_remaining_time(self):
        if not self.is_paused:
            elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
            return max(GAME_DURATION - elapsed, 0)
        return max(GAME_DURATION - self.elapsed_time_when_paused, 0)