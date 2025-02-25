import pygame
import time
from score import ScoreManager
from levels import LevelManager


class Button:
    def __init__(self, screen, text, x, y, width, height, color=(80, 180, 80), hover_color=(100, 200, 100)):
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
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class DropdownMenu:
    def __init__(self, screen, options, x, y, width, height):
        self.screen = screen
        self.options = options
        self.rect = pygame.Rect(x, y, width, height)
        self.dropdown_rect = pygame.Rect(x, y + height, width, height * len(options))
        self.font = pygame.font.SysFont('Arial', 18)
        self.is_open = False
        self.selected_option = options[0] if options else ""

    def draw(self):
        # Vẽ nút chính
        pygame.draw.rect(self.screen, (80, 180, 80), self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 1)  # Viền

        # Vẽ text
        text_surface = self.font.render(self.selected_option, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

        # Vẽ dropdown nếu đang mở
        if self.is_open:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.y + self.rect.height + i * self.rect.height,
                    self.rect.width,
                    self.rect.height
                )

                # Hover effect
                mouse_pos = pygame.mouse.get_pos()
                if option_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, (100, 200, 100), option_rect)
                else:
                    pygame.draw.rect(self.screen, (80, 180, 80), option_rect)

                pygame.draw.rect(self.screen, (0, 0, 0), option_rect, 1)  # Viền

                # Vẽ text
                option_text = self.font.render(option, True, (255, 255, 255))
                option_text_rect = option_text.get_rect(center=option_rect.center)
                self.screen.blit(option_text, option_text_rect)

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.is_open = not self.is_open
            return None

        if self.is_open:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.y + self.rect.height + i * self.rect.height,
                    self.rect.width,
                    self.rect.height
                )

                if option_rect.collidepoint(pos):
                    self.selected_option = option
                    self.is_open = False
                    return option

            # Nếu click ra ngoài, đóng dropdown
            self.is_open = False

        return None


class UI:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.score_manager = ScoreManager()
        self.level_manager = self.game.level_manager

        # Màu sắc
        self.BACKGROUND_COLOR = (240, 240, 240)  # Xám nhạt
        self.TILE_COLOR = (50, 150, 220)  # Xanh dương
        self.TILE_BORDER_COLOR = (30, 100, 180)  # Xanh đậm
        self.TEXT_COLOR = (255, 255, 255)  # Trắng
        self.BUTTON_COLOR = (80, 180, 80)  # Xanh lá
        self.BUTTON_HOVER_COLOR = (100, 200, 100)  # Xanh lá nhạt
        self.SOLVED_COLOR = (255, 215, 0)  # Vàng

        # Font
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 18)
        self.large_font = pygame.font.SysFont('Arial', 36)

        # Kích thước bàn cờ và ô
        self.board_size = 400
        self.board_margin = 50
        self.board_x = (screen.get_width() - self.board_size) // 2
        self.board_y = (screen.get_height() - self.board_size) // 2 - 30

        # Tính kích thước ô dựa vào kích thước bàn cờ và số ô
        self.update_tile_size()

        # Nút
        self.buttons = {
            'new_game_3x3': Button(self.screen, "New 3x3", self.board_x, 30, 100, 40),
            'new_game_4x4': Button(self.screen, "New 4x4", self.board_x + 110, 30, 100, 40),
            'solve_bfs': Button(self.screen, "Solve BFS", self.board_x + 220, 30, 100, 40),
            'solve_hill': Button(self.screen, "Hill Climbing", self.board_x + 330, 30, 140, 40)
        }

        # Dropdown cho map
        self.map_dropdown_3x3 = self._create_map_dropdown(3, self.board_x, 80, 150, 40)
        self.map_dropdown_4x4 = self._create_map_dropdown(4, self.board_x + 160, 80, 150, 40)
        self.current_dropdown = self.map_dropdown_3x3

        # Hình ảnh mẫu cho trạng thái hoàn chỉnh
        self.reference_image_size = 100
        self.reference_image_x = self.board_x + self.board_size + 20
        self.reference_image_y = self.board_y

    def _create_map_dropdown(self, size, x, y, width, height):
        """Tạo dropdown menu cho các map"""
        levels = self.level_manager.get_all_levels(size)
        options = [level["name"] for level in levels]
        return DropdownMenu(self.screen, options, x, y, width, height)

    def update_tile_size(self):
        """Cập nhật kích thước ô dựa trên kích thước bàn cờ và số ô"""
        self.tile_size = self.board_size // self.game.size
        self.tile_margin = 4

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
                        self.current_dropdown = self.map_dropdown_3x3
                    elif name == 'new_game_4x4':
                        self.game.new_game(4)
                        self.update_tile_size()
                        self.current_dropdown = self.map_dropdown_4x4
                    elif name == 'solve_bfs':
                        self.game.start_bot("bfs")
                    elif name == 'solve_hill':
                        self.game.start_bot("hill_climbing")

            # Kiểm tra click vào dropdown
            selected_map_3x3 = self.map_dropdown_3x3.handle_click(mouse_pos)
            if selected_map_3x3:
                level_data = self.level_manager.get_level_by_name(3, selected_map_3x3)
                if level_data:
                    self.game.load_level(level_data)
                    self.update_tile_size()
                    self.current_dropdown = self.map_dropdown_3x3

            selected_map_4x4 = self.map_dropdown_4x4.handle_click(mouse_pos)
            if selected_map_4x4:
                level_data = self.level_manager.get_level_by_name(4, selected_map_4x4)
                if level_data:
                    self.game.load_level(level_data)
                    self.update_tile_size()
                    self.current_dropdown = self.map_dropdown_4x4

    def draw(self):
        """Vẽ toàn bộ giao diện"""
        # Vẽ nền
        self.screen.fill(self.BACKGROUND_COLOR)

        # Vẽ các nút
        for button in self.buttons.values():
            button.draw()

        # Vẽ dropdown
        self.map_dropdown_3x3.draw()
        self.map_dropdown_4x4.draw()

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
                tile_color = self.SOLVED_COLOR if self.game.is_solved else self.TILE_COLOR

                pygame.draw.rect(self.screen, tile_color, tile_rect)
                pygame.draw.rect(self.screen, self.TILE_BORDER_COLOR, tile_rect, 2)

                # Vẽ số trên ô
                text_surface = self.font.render(str(tile_value), True, self.TEXT_COLOR)
                text_rect = text_surface.get_rect(center=tile_rect.center)
                self.screen.blit(text_surface, text_rect)

    def draw_game_info(self):
        """Vẽ thông tin trạng thái game"""
        # Hiển thị số bước
        moves_text = self.small_font.render(f"Moves: {self.game.moves}", True, (0, 0, 0))
        self.screen.blit(moves_text, (self.board_x, self.board_y + self.board_size + 10))

        # Hiển thị thời gian
        minutes = int(self.game.elapsed_time) // 60
        seconds = int(self.game.elapsed_time) % 60
        time_text = self.small_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, (0, 0, 0))
        self.screen.blit(time_text, (self.board_x + 150, self.board_y + self.board_size + 10))

        # Hiển thị số bước của bot nếu bot đang hoạt động hoặc đã hoạt động
        if self.game.bot_total_moves > 0:
            bot_moves_text = self.small_font.render(f"Bot Moves: {self.game.bot_total_moves}", True, (0, 0, 0))
            self.screen.blit(bot_moves_text, (self.board_x + 300, self.board_y + self.board_size + 10))

        # Hiển thị thông báo khi giải xong
        if self.game.is_solved:
            solved_text = self.large_font.render("Puzzle Solved!", True, (0, 150, 0))
            solved_rect = solved_text.get_rect(center=(self.screen.get_width() // 2,
                                                       self.board_y + self.board_size + 45))
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

                    pygame.draw.rect(self.screen, self.TILE_COLOR, tile_rect)
                    pygame.draw.rect(self.screen, self.TILE_BORDER_COLOR, tile_rect, 1)

                    # Vẽ số
                    font_size = 16 if self.game.size == 3 else 12
                    number_font = pygame.font.SysFont('Arial', font_size)
                    text_surface = number_font.render(str(counter), True, self.TEXT_COLOR)
                    text_rect = text_surface.get_rect(center=tile_rect.center)
                    self.screen.blit(text_surface, text_rect)

                    counter += 1

    def draw_high_scores(self):
        """Vẽ danh sách điểm cao"""
        # Lấy danh sách điểm cao
        high_scores = self.score_manager.get_high_scores(self.game.size)

        # Vị trí hiển thị
        x = self.reference_image_x
        y = self.reference_image_y + self.reference_image_size + 20

        # Tiêu đề
        title_text = self.small_font.render(f"High Scores ({self.game.size}x{self.game.size})", True, (0, 0, 0))
        self.screen.blit(title_text, (x, y))

        # Hiển thị tối đa 5 điểm cao
        for i, score in enumerate(high_scores[:5]):
            score_text = self.small_font.render(f"{i + 1}. {score['moves']} moves - {score['time']}s", True, (0, 0, 0))
            self.screen.blit(score_text, (x, y + 25 + i * 20))

    def draw_move_history(self):
        """Vẽ lịch sử nước đi"""
        # Vị trí hiển thị
        x = 20
        y = self.board_y

        # Tiêu đề
        title_text = self.small_font.render("Move History", True, (0, 0, 0))
        self.screen.blit(title_text, (x, y))

        # Hiển thị tối đa 10 nước đi gần nhất
        history = self.game.move_history[-10:] if len(self.game.move_history) > 10 else self.game.move_history

        for i, move in enumerate(history):
            move_text = self.small_font.render(
                f"{len(self.game.move_history) - len(history) + i + 1}. Row {move[0] + 1}, Col {move[1] + 1}", True,
                (0, 0, 0))
            self.screen.blit(move_text, (x, y + 25 + i * 20))