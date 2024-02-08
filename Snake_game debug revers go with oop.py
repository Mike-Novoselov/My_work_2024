import pygame
import sys
import random


class GameConfig:
    """Константы для игры"""
    WIDTH, HEIGHT = 800, 600
    BLOCK_SIZE = 10
    WALL_BLOCK = 3
    GAME_ICON = "pngegg.png"
    GAME_TITLE = "Snake game by Mike Novoselov"
    INITIAL_GAME_SPEED = 10
    SPEED_CHANGE = 1.1
    INITIAL_SNAKE_LENGTH = 3
    INITIAL_APPLES = 3
    SIZE_X = WIDTH // BLOCK_SIZE - WALL_BLOCK * 2
    SIZE_Y = HEIGHT // BLOCK_SIZE - WALL_BLOCK * 2
    BACKGROUND_COLOR = (0, 0, 0)
    SNAKE_RADIUS = BLOCK_SIZE // 5
    SNAKE_COLOR = (31, 191, 31)
    APPLE_RADIUS = BLOCK_SIZE // 2
    APPLE_COLOR = (191, 31, 31)
    WALL_COLOR = (31, 31, 31)
    TEXT_COLOR = (255, 255, 255)
    FONT_SIZE = int(WALL_BLOCK * BLOCK_SIZE * 0.75)


class SnakeGame:
    def __init__(self):
        self.screen, self.clock = self.initialize_pygame()
        self.game_state = self.initialize_game_state()

    def run(self):
        while self.game_state["program_running"]:
            self.clock.tick(self.game_state["game_speed"])
            events = self.get_events()
            # print(events)
            self.update_game_state(events)
            self.update_screen()

        self.perform_shutdown()

    def initialize_pygame(self):
        pygame.init()
        screen = pygame.display.set_mode((GameConfig.WIDTH, GameConfig.HEIGHT))
        icon = pygame.image.load(GameConfig.GAME_ICON)
        pygame.display.set_icon(icon)
        pygame.display.set_caption(GameConfig.GAME_TITLE)
        clock = pygame.time.Clock()
        return screen, clock

    def initialize_game_state(self):
        return {
            "program_running": True,
            "game_running": False,
            "game_paused": False,
            "game_speed": GameConfig.INITIAL_GAME_SPEED,
            "score": 0,
            "snake": [],
            "apples": [],
            "direction": (1, 0)
        }

    def get_events(self):
        events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events.append("quit")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    events.append("up")
                elif event.key == pygame.K_DOWN:
                    events.append("down")
                elif event.key == pygame.K_LEFT:
                    events.append("left")
                elif event.key == pygame.K_RIGHT:
                    events.append("right")
                elif event.key == pygame.K_SPACE:
                    events.append("space")
                elif event.key == pygame.K_RETURN:
                    events.append("enter")
                elif event.key == pygame.K_ESCAPE:
                    events.append("escape")
        # print(events)
        return events

    def update_game_state(self, events):
        self.check_key_presses(events)
        if self.game_state["game_running"] and not self.game_state["game_paused"]:
            self.move_snake()
            self.check_collisions()
            self.check_apple_consumption()

    def check_key_presses(self, events):
        print(events)
        current_direction = self.game_state["direction"]
        opposite_direction = (-current_direction[0], -current_direction[1])

        if "quit" in events:
            self.game_state["program_running"] = False
        elif not self.game_state["game_running"]:
            if "escape" in events:
                self.game_state["program_running"] = False
            elif "enter" in events:
                self.initialize_new_game()
        elif self.game_state["game_paused"]:
            if "escape" in events:
                self.game_state["game_running"] = False
            elif "space" in events:
                self.game_state["game_paused"] = False
        else:
            if "escape" in events or "space" in events:
                self.game_state["game_paused"] = True
            if "up" in events and opposite_direction != (0, -1):
                self.game_state["direction"] = (0, -1)
            if "down" in events and opposite_direction != (0, 1):
                self.game_state["direction"] = (0, 1)
            if "left" in events and opposite_direction != (-1, 0):
                self.game_state["direction"] = (-1, 0)
            if "right" in events and opposite_direction != (1, 0):
                self.game_state["direction"] = (1, 0)

    def move_snake(self):
        head_x, head_y = self.game_state["snake"][0]
        new_head = (head_x + self.game_state["direction"][0], head_y + self.game_state["direction"][1])
        self.game_state["snake"].insert(0, new_head)

    def check_collisions(self):
            head_x, head_y = self.game_state["snake"][0]
            if (head_x < 0 or head_y < 0 or
                    head_x >= GameConfig.SIZE_X or head_y >= GameConfig.SIZE_Y or
                    len(self.game_state["snake"]) != len(set(self.game_state["snake"]))):
                self.game_state["game_running"] = False

    def check_apple_consumption(self):
            head = self.game_state["snake"][0]
            if head in self.game_state["apples"]:
                self.game_state["apples"].remove(head)
                self.place_apples(1)
                self.game_state["score"] += 1
                self.game_state["game_speed"] = round(self.game_state["game_speed"] * GameConfig.SPEED_CHANGE)
            else:
                self.game_state["snake"].pop()

    def initialize_new_game(self):
        self.game_state["snake"] = [(GameConfig.SIZE_X // 2, GameConfig.SIZE_Y // 2)]

        for i in range(1, GameConfig.INITIAL_SNAKE_LENGTH):
            self.game_state["snake"].append((GameConfig.SIZE_X // 2 - i, GameConfig.SIZE_Y // 2))

        self.game_state["apples"] = []
        self.place_apples(GameConfig.INITIAL_APPLES)
        self.game_state["direction"] = (1, 0)
        self.game_state["game_paused"] = False
        self.game_state["score"] = 0
        self.game_state["game_speed"] = GameConfig.INITIAL_GAME_SPEED
        self.game_state["game_running"] = True


    def place_apples(self, apples):
            for _ in range(apples):
                x = random.randint(0, GameConfig.SIZE_X - 1)
                y = random.randint(0, GameConfig.SIZE_Y - 1)
                while (x, y) in self.game_state["apples"] or (x, y) in self.game_state["snake"]:
                    x = random.randint(0, GameConfig.SIZE_X - 1)
                    y = random.randint(0, GameConfig.SIZE_Y - 1)
                self.game_state["apples"].append((x, y))

    def update_screen(self):
            self.screen.fill(GameConfig.BACKGROUND_COLOR)

            if not self.game_state["game_running"]:
                self.print_new_game_message()
            elif self.game_state["game_paused"]:
                self.print_game_paused_message()
            else:
                self.draw_apples()
                self.draw_snake()

            self.draw_walls()
            self.print_score()

            pygame.display.flip()

    def print_new_game_message(self):
        font = pygame.font.SysFont("Courier New", GameConfig.FONT_SIZE, bold=True)
        text1 = font.render("Press ENTER to start new game", True, GameConfig.TEXT_COLOR)
        text2 = font.render("Press ESCAPE to quit", True, GameConfig.TEXT_COLOR)
        text_rect1 = text1.get_rect(center=(GameConfig.WIDTH // 2,
                                            GameConfig.HEIGHT // 2 - GameConfig.FONT_SIZE // 2))
        text_rect2 = text2.get_rect(center=(GameConfig.WIDTH // 2,
                                            GameConfig.HEIGHT // 2 + GameConfig.FONT_SIZE // 2))
        self.screen.blit(text1, text_rect1)
        self.screen.blit(text2, text_rect2)

    def print_game_paused_message(self):
        font = pygame.font.SysFont("Courier New", GameConfig.FONT_SIZE, bold=True)
        text1 = font.render("Game Paused", True, GameConfig.TEXT_COLOR)
        text2 = font.render("Press SPACE to continue", True, GameConfig.TEXT_COLOR)
        text_rect1 = text1.get_rect(center=(GameConfig.WIDTH // 2,
                                            GameConfig.HEIGHT // 2 - GameConfig.FONT_SIZE // 2))
        text_rect2 = text2.get_rect(center=(GameConfig.WIDTH // 2,
                                            GameConfig.HEIGHT // 2 + GameConfig.FONT_SIZE // 2))
        self.screen.blit(text1, text_rect1)
        self.screen.blit(text2, text_rect2)

    def draw_apples(self):
        for apple in self.game_state["apples"]:
            x = apple[0] * GameConfig.BLOCK_SIZE + GameConfig.WALL_BLOCK * GameConfig.BLOCK_SIZE
            y = apple[1] * GameConfig.BLOCK_SIZE + GameConfig.WALL_BLOCK * GameConfig.BLOCK_SIZE
            pygame.draw.circle(self.screen, GameConfig.APPLE_COLOR,
                               (x + GameConfig.BLOCK_SIZE // 2, y + GameConfig.BLOCK_SIZE // 2),
                               GameConfig.APPLE_RADIUS)

    def draw_snake(self):
        for segment in self.game_state["snake"]:
            x = segment[0] * GameConfig.BLOCK_SIZE + GameConfig.WALL_BLOCK * GameConfig.BLOCK_SIZE
            y = segment[1] * GameConfig.BLOCK_SIZE + GameConfig.WALL_BLOCK * GameConfig.BLOCK_SIZE
            pygame.draw.rect(self.screen, GameConfig.SNAKE_COLOR,
                             pygame.Rect(x, y, GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE))

    def draw_walls(self):
        wall_thickness = GameConfig.WALL_BLOCK * GameConfig.BLOCK_SIZE
        pygame.draw.rect(self.screen, GameConfig.WALL_COLOR, pygame.Rect(0, 0, GameConfig.WIDTH, wall_thickness))
        pygame.draw.rect(self.screen, GameConfig.WALL_COLOR, pygame.Rect(0, 0, wall_thickness, GameConfig.HEIGHT))
        pygame.draw.rect(self.screen, GameConfig.WALL_COLOR,
                         pygame.Rect(0, GameConfig.HEIGHT - wall_thickness, GameConfig.WIDTH, wall_thickness))
        pygame.draw.rect(self.screen, GameConfig.WALL_COLOR,
                         pygame.Rect(GameConfig.WIDTH - wall_thickness, 0, wall_thickness, GameConfig.HEIGHT))

    def print_score(self):  #
        wall_size = GameConfig.WALL_BLOCK * GameConfig.BLOCK_SIZE
        font = pygame.font.SysFont("Courier New", GameConfig.FONT_SIZE, bold=True)
        score_text = f"Score: {self.game_state['score']}"
        text = font.render(score_text, True, GameConfig.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.midleft = (wall_size, wall_size // 2)
        self.screen.blit(text, text_rect)

    def perform_shutdown(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
