import pygame
import sys
import random
import json
import os

pygame.init()

# Cấu hình kích thước bàn chơi
CELL_SIZE = 26
GRID_WIDTH = 24
GRID_HEIGHT = 20
TOP_PANEL = 64

WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT + TOP_PANEL

# Bảng màu
BG_COLOR = (20, 24, 33)
BOARD_BG = (26, 31, 44)
GRID_LINE_COLOR = (33, 40, 56)
PANEL_COLOR = (15, 18, 26)

SNAKE_HEAD_COLOR = (46, 204, 113)
SNAKE_BODY_COLOR = (39, 174, 96)
FOOD_COLOR = (231, 76, 60)
FOOD_GLOW = (231, 76, 60, 60)

TEXT_COLOR = (240, 243, 246)
TEXT_MUTED = (140, 150, 165)
ACCENT_COLOR = (241, 196, 15)
BUTTON_COLOR = (38, 46, 64)
BUTTON_HOVER = (52, 63, 87)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rắn Săn Mồi - Snake Master")
clock = pygame.time.Clock()

# Tự động nạp font hệ thống hỗ trợ Tiếng Việt
def get_vietnamese_font(size, bold=False):
    candidate_fonts = ["segoeui", "arial", "tahoma", "dejavusans", "roboto", "helvetica"]
    for font_name in candidate_fonts:
        matched = pygame.font.match_font(font_name, bold=bold)
        if matched:
            return pygame.font.Font(matched, size)
    return pygame.font.SysFont("sans-serif", size, bold=bold)

font_sm = get_vietnamese_font(18)
font_md = get_vietnamese_font(24)
font_lg = get_vietnamese_font(32, bold=True)
font_xl = get_vietnamese_font(48, bold=True)

# Quản lý bảng xếp hạng tách biệt theo từng độ khó
LEADERBOARD_FILE = "snake_leaderboard.json"

DEFAULT_LEADERBOARD = {
    "CHẬM": [0, 0, 0, 0, 0],
    "VỪA": [0, 0, 0, 0, 0],
    "NHANH": [0, 0, 0, 0, 0]
}

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for key in DEFAULT_LEADERBOARD:
                    if key not in data:
                        data[key] = [0, 0, 0, 0, 0]
                return data
        except Exception:
            pass
    return DEFAULT_LEADERBOARD.copy()

def save_leaderboard(data):
    try:
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

class SnakeGame:
    def __init__(self):
        self.leaderboard = load_leaderboard()
        self.state = "HOME"  # HOME, PLAYING, GAME_OVER
        
        # Cấu hình thời gian di chuyển giữa 2 ô (tính theo mili-giây, số càng nhỏ càng nhanh)
        self.speeds_preset = {
            "CHẬM": 140,   # ~7 ô/giây
            "VỪA": 85,     # ~12 ô/giây
            "NHANH": 55    # ~18 ô/giây
        }
        self.selected_difficulty = "VỪA"
        self.move_interval = self.speeds_preset[self.selected_difficulty]
        self.last_move_time = 0
        self.direction_queue = []
        self.reset()

    def reset(self):
        mid_x = GRID_WIDTH // 2
        mid_y = GRID_HEIGHT // 2
        self.snake = [
            (mid_x, mid_y),
            (mid_x - 1, mid_y),
            (mid_x - 2, mid_y)
        ]
        self.direction = (1, 0)
        self.direction_queue = []
        self.score = 0
        self.move_interval = self.speeds_preset[self.selected_difficulty]
        self.food = self.spawn_food()
        self.last_move_time = pygame.time.get_ticks()

    def spawn_food(self):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in self.snake:
                return pos

    def add_input_direction(self, new_dir):
        # Xác định hướng tham chiếu để không quay ngược 180 độ
        ref_dir = self.direction_queue[-1] if self.direction_queue else self.direction
        if (new_dir[0] != -ref_dir[0] or new_dir[0] == 0) and \
           (new_dir[1] != -ref_dir[1] or new_dir[1] == 0):
            if len(self.direction_queue) < 2:  # Đệm tối đa 2 lệnh bấm
                self.direction_queue.append(new_dir)

    def update(self):
        if self.state != "PLAYING":
            return

        current_time = pygame.time.get_ticks()
        # Chỉ cập nhật vị trí rắn khi đủ chu kỳ mili-giây quy định
        if current_time - self.last_move_time < self.move_interval:
            return

        self.last_move_time = current_time

        # Lấy hướng tiếp theo từ hàng đợi nếu có
        if self.direction_queue:
            self.direction = self.direction_queue.pop(0)

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Va chạm biên hoặc cắn vào thân
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT) or new_head in self.snake:
            self.state = "GAME_OVER"
            # Cập nhật riêng cho bảng xếp hạng của chế độ hiện tại
            mode_lb = self.leaderboard[self.selected_difficulty]
            mode_lb.append(self.score)
            self.leaderboard[self.selected_difficulty] = sorted(list(set(mode_lb)), reverse=True)[:5]
            save_leaderboard(self.leaderboard)
            return

        self.snake.insert(0, new_head)

        # Xử lý ăn mồi
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def draw_home(self):
        screen.fill(BG_COLOR)

        title = font_xl.render("RẮN SĂN MỒI", True, SNAKE_HEAD_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

        sub = font_md.render("Chọn cấp độ (Phím 1, 2, 3 hoặc Click):", True, TEXT_COLOR)
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 105))

        # Hiển thị 3 nút tốc độ
        diffs = [("1. Chậm", "CHẬM"), ("2. Vừa", "VỪA"), ("3. Nhanh", "NHANH")]
        mouse_pos = pygame.mouse.get_pos()
        self.btn_rects = []

        start_x = WIDTH // 2 - 270
        for i, (label, mode) in enumerate(diffs):
            rect = pygame.Rect(start_x + i * 185, 145, 170, 46)
            self.btn_rects.append((rect, mode))
            is_active = (self.selected_difficulty == mode)
            is_hover = rect.collidepoint(mouse_pos)

            btn_bg = BUTTON_HOVER if (is_hover or is_active) else BUTTON_COLOR
            pygame.draw.rect(screen, btn_bg, rect, border_radius=8)
            if is_active:
                pygame.draw.rect(screen, ACCENT_COLOR, rect, 2, border_radius=8)

            txt = font_md.render(label, True, ACCENT_COLOR if is_active else TEXT_COLOR)
            screen.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))

        # Khung bảng xếp hạng riêng biệt theo mức độ đang chọn
        lb_box = pygame.Rect(WIDTH // 2 - 180, 215, 360, 240)
        pygame.draw.rect(screen, PANEL_COLOR, lb_box, border_radius=12)
        pygame.draw.rect(screen, GRID_LINE_COLOR, lb_box, 1, border_radius=12)

        lb_title = font_md.render(f"TOP 5 - MỨC {self.selected_difficulty}", True, ACCENT_COLOR)
        screen.blit(lb_title, (lb_box.centerx - lb_title.get_width() // 2, lb_box.y + 15))

        scores = self.leaderboard.get(self.selected_difficulty, [0, 0, 0, 0, 0])
        for idx, sc in enumerate(scores[:5]):
            rank_str = f"Hạng {idx + 1}"
            rank_color = ACCENT_COLOR if idx == 0 else TEXT_MUTED
            rank_txt = font_sm.render(rank_str, True, rank_color)
            sc_txt = font_sm.render(f"{sc} điểm", True, TEXT_COLOR)
            
            y_pos = lb_box.y + 55 + idx * 34
            screen.blit(rank_txt, (lb_box.x + 35, y_pos))
            screen.blit(sc_txt, (lb_box.right - sc_txt.get_width() - 35, y_pos))
            
            if idx < 4:
                pygame.draw.line(screen, (28, 34, 46), (lb_box.x + 25, y_pos + 26), (lb_box.right - 25, y_pos + 26), 1)

        hint = font_sm.render("Nhấn SPACE hoặc ENTER để Bắt đầu chơi", True, SNAKE_HEAD_COLOR)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 45))

    def draw_playing(self):
        screen.fill(BG_COLOR)

        board_rect = pygame.Rect(0, TOP_PANEL, WIDTH, HEIGHT - TOP_PANEL)
        pygame.draw.rect(screen, BOARD_BG, board_rect)

        # Thanh thông số bên trên
        pygame.draw.rect(screen, PANEL_COLOR, (0, 0, WIDTH, TOP_PANEL))
        pygame.draw.line(screen, GRID_LINE_COLOR, (0, TOP_PANEL), (WIDTH, TOP_PANEL), 2)

        score_txt = font_md.render(f"Điểm: {self.score}", True, ACCENT_COLOR)
        screen.blit(score_txt, (20, 18))

        mode_txt = font_sm.render(f"Chế độ: {self.selected_difficulty}", True, TEXT_MUTED)
        screen.blit(mode_txt, (WIDTH // 2 - mode_txt.get_width() // 2, 22))

        high_score = self.leaderboard[self.selected_difficulty][0]
        high_txt = font_md.render(f"Kỷ lục: {max(high_score, self.score)}", True, TEXT_COLOR)
        screen.blit(high_txt, (WIDTH - high_txt.get_width() - 20, 18))

        # Đường lưới
        for x in range(GRID_WIDTH + 1):
            px = x * CELL_SIZE
            pygame.draw.line(screen, GRID_LINE_COLOR, (px, TOP_PANEL), (px, HEIGHT), 1)
        for y in range(GRID_HEIGHT + 1):
            py = TOP_PANEL + y * CELL_SIZE
            pygame.draw.line(screen, GRID_LINE_COLOR, (0, py), (WIDTH, py), 1)

        # Vẽ mồi ăn
        fx, fy = self.food
        cx = fx * CELL_SIZE + CELL_SIZE // 2
        cy = TOP_PANEL + fy * CELL_SIZE + CELL_SIZE // 2

        glow_surf = pygame.Surface((CELL_SIZE * 2, CELL_SIZE * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, FOOD_GLOW, (CELL_SIZE, CELL_SIZE), CELL_SIZE // 1.5)
        screen.blit(glow_surf, (cx - CELL_SIZE, cy - CELL_SIZE))
        pygame.draw.circle(screen, FOOD_COLOR, (cx, cy), CELL_SIZE // 2 - 2)

        # Vẽ rắn
        for i, (sx, sy) in enumerate(self.snake):
            rect = pygame.Rect(
                sx * CELL_SIZE + 2,
                TOP_PANEL + sy * CELL_SIZE + 2,
                CELL_SIZE - 4,
                CELL_SIZE - 4
            )
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR
            pygame.draw.rect(screen, color, rect, border_radius=6)

            if i == 0:
                eye_r = 2
                dx, dy = self.direction
                if dx == 1:
                    e1, e2 = (rect.right - 5, rect.top + 6), (rect.right - 5, rect.bottom - 6)
                elif dx == -1:
                    e1, e2 = (rect.left + 5, rect.top + 6), (rect.left + 5, rect.bottom - 6)
                elif dy == -1:
                    e1, e2 = (rect.left + 6, rect.top + 5), (rect.right - 6, rect.top + 5)
                else:
                    e1, e2 = (rect.left + 6, rect.bottom - 5), (rect.right - 6, rect.bottom - 5)

                pygame.draw.circle(screen, (20, 20, 20), e1, eye_r)
                pygame.draw.circle(screen, (20, 20, 20), e2, eye_r)

        # Màn Game Over
        if self.state == "GAME_OVER":
            overlay = pygame.Surface((WIDTH, HEIGHT - TOP_PANEL), pygame.SRCALPHA)
            overlay.fill((10, 12, 16, 215))
            screen.blit(overlay, (0, TOP_PANEL))

            go_title = font_xl.render("GAME OVER", True, (231, 76, 60))
            score_summary = font_md.render(f"Điểm đạt được: {self.score}", True, ACCENT_COLOR)
            replay_sub = font_sm.render("SPACE: Chơi lại | ESC: Về Menu chính", True, TEXT_COLOR)

            cy_box = TOP_PANEL + (HEIGHT - TOP_PANEL) // 2
            screen.blit(go_title, (WIDTH // 2 - go_title.get_width() // 2, cy_box - 70))
            screen.blit(score_summary, (WIDTH // 2 - score_summary.get_width() // 2, cy_box - 15))
            screen.blit(replay_sub, (WIDTH // 2 - replay_sub.get_width() // 2, cy_box + 35))

    def draw(self):
        if self.state == "HOME":
            self.draw_home()
        else:
            self.draw_playing()
        pygame.display.flip()

def main():
    game = SnakeGame()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game.state == "HOME":
                    for rect, mode in game.btn_rects:
                        if rect.collidepoint(event.pos):
                            game.selected_difficulty = mode

            elif event.type == pygame.KEYDOWN:
                if game.state == "HOME":
                    if event.key in (pygame.K_1, pygame.K_KP1):
                        game.selected_difficulty = "CHẬM"
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        game.selected_difficulty = "VỪA"
                    elif event.key in (pygame.K_3, pygame.K_KP3):
                        game.selected_difficulty = "NHANH"
                    elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        game.reset()
                        game.state = "PLAYING"

                elif game.state == "GAME_OVER":
                    if event.key == pygame.K_SPACE:
                        game.reset()
                        game.state = "PLAYING"
                    elif event.key == pygame.K_ESCAPE:
                        game.state = "HOME"

                elif game.state == "PLAYING":
                    if event.key in (pygame.K_UP, pygame.K_w):
                        game.add_input_direction((0, -1))
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        game.add_input_direction((0, 1))
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        game.add_input_direction((-1, 0))
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        game.add_input_direction((1, 0))
                    elif event.key == pygame.K_ESCAPE:
                        game.state = "HOME"

        game.update()
        game.draw()
        # Chạy cố định ở 60 FPS để xử lý sự kiện tức thời, không bị khựng phím
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()