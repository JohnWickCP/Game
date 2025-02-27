import pygame
import time
from score import ScoreManager
from constants import *


class Button:
    def __init__(self, screen, text, x, y, width, height, color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR):
        self.screen = screen
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont('Arial', 18)

    def draw(self):
        # Kiểm tra chuột có đang hover không
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.color

        # Vẽ nút
        pygame.draw.rect(self.screen, current_color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 1)  # Viền

        # Vẽ text
        text_surface = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class UI:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.score_manager = ScoreManager()
        self.level_manager = self.game.level_manager

        # Lấy kích thước màn hình
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Font
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 18)
        self.large_font = pygame.font.SysFont('Arial', 36)

        # Bố trí UI
        self.setup_layout()

        # Tạo các thành phần UI
        self.create_buttons()

    def setup_layout(self):
        """Thiết lập bố cục giao diện"""
        # Kích thước và vị trí bàn cờ
        self.board_size = min(BOARD_SIZE, self.screen_width * 0.5)  # Giới hạn kích thước bàn cờ
        self.board_x = (self.screen_width - self.board_size) // 2  # Đặt bàn cờ ở giữa
        self.board_y = (self.screen_height - self.board_size) // 2

        # Tính kích thước ô dựa vào kích thước bàn cờ và số ô
        self.update_tile_size()

        # Vị trí khu vực điều khiển (bên trái)
        self.control_area_width = 200
        self.control_area_x = 20
        self.control_area_y = 20

        # Vị trí khu vực thông tin (bên phải) - Di chuyển sang phải hơn
        self.info_area_width = 200
        self.info_area_x = self.screen_width - self.info_area_width - 10
        self.info_area_y = 20

        # Vị trí khu vực điểm cao
        self.score_area_x = self.info_area_x
        self.score_area_y = self.screen_height // 2

        # Hình ảnh mẫu - Di chuyển sang phải hơn
        self.reference_image_size = min(120, self.info_area_width - 10)
        self.reference_image_x = self.screen_width - self.reference_image_size - 20
        self.reference_image_y = self.info_area_y + 30

    def create_buttons(self):
        """Tạo các nút điều khiển"""
        # Nút chọn kích thước bàn cờ
        self.buttons = {
            'new_game_3x3': Button(
                self.screen,
                "New 3x3",
                self.control_area_x,
                self.control_area_y,
                BUTTON_WIDTH,
                BUTTON_HEIGHT
            ),
            'new_game_4x4': Button(
                self.screen,
                "New 4x4",
                self.control_area_x + BUTTON_WIDTH + BUTTON_SPACING,
                self.control_area_y,
                BUTTON_WIDTH,
                BUTTON_HEIGHT
            ),
            'solve_bfs': Button(
                self.screen,
                "Solve BFS",
                self.board_x,
                self.board_y + self.board_size + 20,
                BUTTON_WIDTH,
                BUTTON_HEIGHT
            ),
            'solve_hill': Button(
                self.screen,
                "Hill Climbing",
                self.board_x + BUTTON_WIDTH + BUTTON_SPACING,
                self.board_y + self.board_size + 20,
                BUTTON_WIDTH + 40,
                BUTTON_HEIGHT
            )
        }

        # Tạo nút chọn map 3x3
        levels_3x3 = self.level_manager.get_all_levels(3)
        map_3x3_y = self.control_area_y + 100

        self.map_buttons_3x3 = {}
        for i, level in enumerate(levels_3x3[:4]):  # Giới hạn chỉ 4 map
            self.map_buttons_3x3[f"map_3x3_{i}"] = Button(
                self.screen,
                f"Map {i + 1}",  # Đổi tên thành Map 1, Map 2, ...
                self.control_area_x,
                map_3x3_y + i * (BUTTON_HEIGHT + 10),
                BUTTON_WIDTH + 50,
                BUTTON_HEIGHT
            )

        # Tạo nút chọn map 4x4
        levels_4x4 = self.level_manager.get_all_levels(4)
        map_4x4_y = map_3x3_y + 4 * (BUTTON_HEIGHT + 10) + 50  # Chỉ có 4 map 3x3

        self.map_buttons_4x4 = {}
        for i, level in enumerate(levels_4x4[:4]):  # Giới hạn chỉ 4 map
            self.map_buttons_4x4[f"map_4x4_{i}"] = Button(
                self.screen,
                f"Map {i + 1}",  # Đổi tên thành Map 1, Map 2, ...
                self.control_area_x,
                map_4x4_y + i * (BUTTON_HEIGHT + 10),
                BUTTON_WIDTH + 50,
                BUTTON_HEIGHT
            )

    def update_tile_size(self):
        """Cập nhật kích thước ô dựa trên kích thước bàn cờ và số ô"""
        self.tile_size = self.board_size // self.game.size
        self.tile_margin = TILE_MARGIN

    def handle_event(self, event):
        """Xử lý sự kiện"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            # Kiểm tra click vào ô
            tile_pos = self.game.get_tile_at_position(mouse_pos, self.tile_size, self.board_x, self.board_y)
            if tile_pos is not None and self.game.can_move(tile_pos):
                self.game.move_tile(tile_pos)

            # Kiểm tra click vào nút
            for name, button in self.buttons.items():
                if button.is_clicked(mouse_pos):
                    if name == 'new_game_3x3':
                        self.game.new_game(3)
                        self.update_tile_size()
                    elif name == 'new_game_4x4':
                        self.game.new_game(4)
                        self.update_tile_size()
                    elif name == 'solve_bfs':
                        self.game.start_bot("bfs")
                    elif name == 'solve_hill':
                        self.game.start_bot("hill_climbing")

            # Kiểm tra click vào nút map 3x3
            for name, button in self.map_buttons_3x3.items():
                if button.is_clicked(mouse_pos):
                    index = int(name.split('_')[-1])
                    levels = self.level_manager.get_all_levels(3)
                    if index < len(levels):
                        self.game.load_level(levels[index])
                        self.update_tile_size()

            # Kiểm tra click vào nút map 4x4
            for name, button in self.map_buttons_4x4.items():
                if button.is_clicked(mouse_pos):
                    index = int(name.split('_')[-1])
                    levels = self.level_manager.get_all_levels(4)
                    if index < len(levels):
                        self.game.load_level(levels[index])
                        self.update_tile_size()

    def draw(self):
        """Vẽ toàn bộ giao diện"""
        # Vẽ nền
        self.screen.fill(BACKGROUND_COLOR)

        # Vẽ các nút chính
        for button in self.buttons.values():
            button.draw()

        # Vẽ tiêu đề và các nút để chọn map
        self.draw_map_selectors()

        # Vẽ bàn cờ
        self.draw_board()

        # Vẽ thông tin trạng thái game
        self.draw_game_info()

        # Vẽ hình ảnh mẫu
        self.draw_reference_image()

        # Vẽ danh sách điểm cao
        self.draw_high_scores()

        # Vẽ lịch sử nước đi
        self.draw_move_history()

    def draw_map_selectors(self):
        """Vẽ danh sách chọn map"""
        # Vẽ tiêu đề cho phần map 3x3
        title_3x3_y = self.control_area_y + 100
        title_3x3 = self.font.render("Maps 3x3", True, (0, 0, 0))
        self.screen.blit(title_3x3, (self.control_area_x, title_3x3_y - 40))

        # Vẽ các nút map 3x3
        for button in self.map_buttons_3x3.values():
            button.draw()

        # Vẽ tiêu đề cho phần map 4x4
        map_4x4_y = title_3x3_y + 4 * (BUTTON_HEIGHT + 10) + 50  # Chỉ có 4 map 3x3
        title_4x4 = self.font.render("Maps 4x4", True, (0, 0, 0))
        self.screen.blit(title_4x4, (self.control_area_x, map_4x4_y - 40))

        # Vẽ các nút map 4x4
        for button in self.map_buttons_4x4.values():
            button.draw()

        # Vẽ map hiện tại
        current_map_text = "Current Map: "
        if self.game.current_map:
            current_map_text += self.game.current_map
        else:
            current_map_text += "Random"

        current_map_surface = self.small_font.render(current_map_text, True, (0, 0, 0))
        self.screen.blit(current_map_surface, (self.board_x, self.board_y - 30))

    def draw_board(self):
        """Vẽ bàn cờ"""
        # Vẽ nền cho bàn cờ
        pygame.draw.rect(self.screen, (200, 200, 200),
                         (self.board_x, self.board_y, self.board_size, self.board_size))

        for row in range(self.game.size):
            for col in range(self.game.size):
                tile_value = self.game.board[row][col]

                # Bỏ qua ô trống
                if tile_value == 0:
                    continue

                # Vị trí vẽ ô
                x = self.board_x + col * self.tile_size
                y = self.board_y + row * self.tile_size

                # Xử lý animation
                if (self.game.is_animating and
                        self.game.animating_tile == tile_value):
                    # Tính vị trí animation
                    progress = self.game.get_animation_progress()
                    from_row, from_col = self.game.animating_from
                    to_row, to_col = self.game.animating_to

                    # Tính vị trí hiện tại dựa vào tiến độ animation
                    x = self.board_x + (from_col + (to_col - from_col) * progress) * self.tile_size
                    y = self.board_y + (from_row + (to_row - from_row) * progress) * self.tile_size

                # Vẽ ô
                tile_rect = pygame.Rect(x + self.tile_margin, y + self.tile_margin,
                                        self.tile_size - 2 * self.tile_margin,
                                        self.tile_size - 2 * self.tile_margin)

                # Màu ô dựa vào trạng thái giải
                tile_color = SOLVED_COLOR if self.game.is_solved else TILE_COLOR

                pygame.draw.rect(self.screen, tile_color, tile_rect)
                pygame.draw.rect(self.screen, TILE_BORDER_COLOR, tile_rect, 2)

                # Vẽ số trên ô
                text_surface = self.font.render(str(tile_value), True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=tile_rect.center)
                self.screen.blit(text_surface, text_rect)

    def draw_game_info(self):
        """Vẽ thông tin trạng thái game"""
        info_x = self.board_x
        info_y = self.board_y + self.board_size + 60

        # Hiển thị số bước
        moves_text = self.small_font.render(f"Moves: {self.game.moves}", True, (0, 0, 0))
        self.screen.blit(moves_text, (info_x, info_y))

        # Hiển thị thời gian
        minutes = int(self.game.elapsed_time) // 60
        seconds = int(self.game.elapsed_time) % 60
        time_text = self.small_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, (0, 0, 0))
        self.screen.blit(time_text, (info_x + 150, info_y))

        # Hiển thị số bước của bot nếu bot đang hoạt động hoặc đã hoạt động
        if self.game.bot_total_moves > 0:
            bot_moves_text = self.small_font.render(f"Bot Moves: {self.game.bot_total_moves}", True, (0, 0, 0))
            self.screen.blit(bot_moves_text, (info_x + 300, info_y))

        # Hiển thị thông báo khi giải xong
        if self.game.is_solved:
            solved_text = self.large_font.render("Puzzle Solved!", True, (0, 150, 0))
            solved_rect = solved_text.get_rect(center=(self.screen_width // 2, info_y + 40))
            self.screen.blit(solved_text, solved_rect)

    def draw_reference_image(self):
        """Vẽ hình ảnh mẫu để tham khảo trạng thái hoàn chỉnh"""
        # Vẽ nền cho hình ảnh mẫu
        pygame.draw.rect(self.screen, (200, 200, 200),
                         (self.reference_image_x, self.reference_image_y,
                          self.reference_image_size, self.reference_image_size))

        # Tiêu đề
        title_text = self.small_font.render("Reference", True, (0, 0, 0))
        title_rect = title_text.get_rect(midtop=(self.reference_image_x + self.reference_image_size // 2,
                                                 self.reference_image_y - 25))
        self.screen.blit(title_text, title_rect)

        # Vẽ hình ảnh mẫu - phiên bản thu nhỏ của bàn cờ đã giải
        tile_size = self.reference_image_size // self.game.size
        margin = 2

        counter = 1
        for row in range(self.game.size):
            for col in range(self.game.size):
                if row == self.game.size - 1 and col == self.game.size - 1:
                    # Ô trống
                    pass
                else:
                    # Vẽ ô
                    x = self.reference_image_x + col * tile_size
                    y = self.reference_image_y + row * tile_size

                    tile_rect = pygame.Rect(x + margin, y + margin,
                                            tile_size - 2 * margin,
                                            tile_size - 2 * margin)

                    pygame.draw.rect(self.screen, TILE_COLOR, tile_rect)
                    pygame.draw.rect(self.screen, TILE_BORDER_COLOR, tile_rect, 1)

                    # Vẽ số
                    font_size = 16 if self.game.size == 3 else 12
                    number_font = pygame.font.SysFont('Arial', font_size)
                    text_surface = number_font.render(str(counter), True, TEXT_COLOR)
                    text_rect = text_surface.get_rect(center=tile_rect.center)
                    self.screen.blit(text_surface, text_rect)

                    counter += 1

    def draw_high_scores(self):
        """Vẽ danh sách điểm cao"""
        # Vị trí hiển thị
        score_x = self.info_area_x
        score_y = self.reference_image_y + self.reference_image_size + 30

        # Lấy danh sách điểm cao
        if self.game.current_map:
            # Điểm cao cho map cụ thể
            high_scores = self.score_manager.get_high_scores(self.game.size, self.game.current_map)
            title = f"High Scores for {self.game.current_map}"
        else:
            # Điểm cao cho map ngẫu nhiên
            high_scores = self.score_manager.get_high_scores(self.game.size)
            title = f"High Scores ({self.game.size}x{self.game.size})"

        # Tiêu đề
        title_text = self.small_font.render(title, True, (0, 0, 0))
        self.screen.blit(title_text, (score_x, score_y))

        # Hiển thị tối đa 5 điểm cao
        if high_scores:
            for i, score in enumerate(high_scores[:5]):
                score_text = self.small_font.render(f"{i + 1}. {score['moves']} moves - {score['time']}s", True,
                                                    (0, 0, 0))
                self.screen.blit(score_text, (score_x, score_y + 25 + i * 20))
        else:
            no_scores_text = self.small_font.render("No high scores yet", True, (0, 0, 0))
            self.screen.blit(no_scores_text, (score_x, score_y + 25))

    def draw_move_history(self):
        """Vẽ lịch sử nước đi"""
        # Vị trí hiển thị
        history_x = self.info_area_x
        history_y = self.reference_image_y + self.reference_image_size + 150

        # Tiêu đề
        title_text = self.small_font.render("Move History", True, (0, 0, 0))
        self.screen.blit(title_text, (history_x, history_y))

        # Hiển thị tối đa 10 nước đi gần nhất
        history = self.game.move_history[-10:] if len(self.game.move_history) > 10 else self.game.move_history

        if history:
            for i, move in enumerate(history):
                move_text = self.small_font.render(
                    f"{len(self.game.move_history) - len(history) + i + 1}. Row {move[0] + 1}, Col {move[1] + 1}", True,
                    (0, 0, 0))
                self.screen.blit(move_text, (history_x, history_y + 25 + i * 20))
        else:
            no_moves_text = self.small_font.render("No moves yet", True, (0, 0, 0))
            self.screen.blit(no_moves_text, (history_x, history_y + 25))