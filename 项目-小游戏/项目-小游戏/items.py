import pygame
import random
from game_config import ITEM_FALL_SPEED_RANGE, ITEM_SPAWN_INTERVAL_RANGE, ITEM_SPAWN_X_RANGE

# 道具类型常量 - 便于未来扩展
ITEM_TYPES = {
    'BOMB': 1,
    'FOOD': 2,
    # 预留未来道具类型
    # 'clock': 3,
}

class Item:
    def __init__(self, item_type, x, y):
        # 基础属性
        self.item_type = item_type
        self.x = x
        self.y = y
        self.size = 30  # 道具碰撞体积
        self.speed = random.randint(*ITEM_FALL_SPEED_RANGE)  # 道具下落速度
        self.active = True  # 道具活动状态
        self.spawn_time = pygame.time.get_ticks()  # 生成时间
        self.lifetime = random.randint(5000, 8000)  # 生存时间(ms)

    def update(self):
        """更新道具状态"""
        # 移动逻辑
        self.y += self.speed
        
        # 生命周期检查
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.active = False

    def check_collision(self, player):
        """检测与玩家的碰撞(矩形碰撞检测)"""
        # 创建玩家碰撞矩形
        player_rect = pygame.Rect(
            player.x - player.width//2,
            player.y - player.height//2,
            player.width,
            player.height
        )
        
        # 创建道具碰撞矩形
        item_rect = pygame.Rect(
            self.x - self.size//2,
            self.y - self.size//2,
            self.size,
            self.size
        )
        
        return player_rect.colliderect(item_rect)

    def on_collect(self, player):
        """处理道具收集逻辑(基类实现基础功能，子类重写实现具体效果)"""
        self.active = False  # 收集后设置为非活动状态
        # 可以在这里添加通用收集逻辑，如分数增加等
        # player.score += 10

    def draw(self, screen):
        """绘制道具(基类实现默认外观，子类重写实现特定外观)"""
        # 默认绘制一个白色圆形
        pygame.draw.circle(
            screen,
            (255, 255, 255),  # 白色
            (self.x, self.y),
            self.size//2
        )
        # 绘制道具类型标识
        font = pygame.font.Font(None, 16)
        type_text = font.render(str(self.item_type), True, (0, 0, 0))
        text_rect = type_text.get_rect(center=(self.x, self.y))
        screen.blit(type_text, text_rect)


class ItemManager:
    """道具管理器 - 处理道具生成、更新和生命周期管理"""
    def __init__(self, screen_height=600):
        self.items = []
        self.spawn_timer = 0
        self.screen_height = screen_height
        self.last_spawn_time = pygame.time.get_ticks()
        # 初始化生成间隔
        self._reset_spawn_interval()  # 替换直接赋值

    def _reset_spawn_interval(self):
        """重置道具生成间隔（提取重复逻辑为独立方法）"""
        self.spawn_interval = random.randint(*ITEM_SPAWN_INTERVAL_RANGE)

    def update(self, player):
        """更新所有道具状态并处理生成逻辑"""
        current_time = pygame.time.get_ticks()
        self._handle_spawning(current_time)
        self._update_items(player)
        self._cleanup_inactive_items()

    def _handle_spawning(self, current_time):
        """处理道具生成逻辑"""
        if current_time - self.last_spawn_time > self.spawn_interval:
            # 随机生成一个基础道具
            new_item = Item(
                item_type=random.choice(list(ITEM_TYPES.values())),
                x=random.randint(ITEM_SPAWN_X_RANGE),  # 使用配置的X轴范围
                y=0  # Y轴固定在屏幕顶部
            )
            self.items.append(new_item)
            # 重置生成计时器和下次生成间隔
            self.last_spawn_time = current_time
            self._reset_spawn_interval()  # 替换直接赋值

    def _update_items(self, player):
        """更新所有道具位置并检测碰撞"""
        for item in self.items:
            if item.active:
                item.update()
                # 检测与玩家碰撞
                if item.check_collision(player):
                    item.on_collect(player)
                # 检测是否落地
                if item.y >= self.screen_height - item.size//2:
                    item.active = False

    def _cleanup_inactive_items(self):
        """移除所有非活动道具"""
        self.items = [item for item in self.items if item.active]

    def draw(self, screen):
        """绘制所有活动道具"""
        for item in self.items:
            if item.active:
                item.draw(screen)
