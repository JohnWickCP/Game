import random
import time
from bot import BotSolver
from utils import is_solvable, get_solution_state
from levels import LevelManager
from constants import ANIMATION_DURATION, BOT_MOVE_DELAY


class Game:
    def __init__(self, size=3):
        self.size = size
        self.board = []
        self.empty_pos = (0, 0)
        self.is_solved = False
        self.is_animating = False
        self.animation_start_time = 0
        self.animation_duration = ANIMATION_DURATION  # seconds
        self.animating_tile = None
        self.animating_from = None
        self.animating_to = None

        # Thời gian và số bước
        self.moves = 0
        self.start_time = time.time()
        self.elapsed_time = 0
        self.game_active = False

        # Bot
        self.bot_solver = BotSolver(self)
        self.bot_active = False
        self.bot_moves = []
        self.bot_current_move = 0
        self.bot_move_timer = 0
        self.bot_move_delay = BOT_MOVE_DELAY  # seconds
        self.bot_total_moves = 0

        # Lịch sử nước đi
        self.move_history = []

        # Level manager
        self.level_manager = LevelManager()

        # Thông tin map hiện tại
        self.current_map = None  # None = map ngẫu nhiên

        # Khởi tạo bàn cờ mới
        self.new_game(size)

    def new_game(self, size=None):
        if size is not None:
            self.size = size

        # Khởi tạo bàn cờ theo thứ tự
        self.board = self._create_solved_board()

        # Trộn bàn cờ
        self._shuffle_board()

        # Reset các thuộc tính
        self.is_solved = False
        self.moves = 0
        self.start_time = time.time()
        self.elapsed_time = 0
        self.game_active = True
        self.bot_active = False
        self.bot_moves = []
        self.bot_current_move = 0
        self.bot_total_moves = 0
        self.move_history = []
        self.current_map = None  # Map ngẫu nhiên

    def load_level(self, level_data):
        """Tải map từ dữ liệu level"""
        self.size = len(level_data["board"])
        self.board = level_data["board"]
        self.empty_pos = tuple(level_data["empty_pos"])
        self.current_map = level_data["name"]

        # Reset các thuộc tính
        self.is_solved = False
        self.moves = 0
        self.start_time = time.time()
        self.elapsed_time = 0
        self.game_active = True
        self.bot_active = False
        self.bot_moves = []
        self.bot_current_move = 0
        self.bot_total_moves = 0
        self.move_history = []

        # Khởi tạo lại bot solver với kích thước mới
        self.bot_solver = BotSolver(self)

    def _create_solved_board(self):
        """Tạo bàn cờ đã được giải (theo thứ tự 1,2,3,...,0)"""
        board = []
        counter = 1

        for row in range(self.size):
            board_row = []
            for col in range(self.size):
                if row == self.size - 1 and col == self.size - 1:
                    board_row.append(0)  # Ô trống
                    self.empty_pos = (row, col)
                else:
                    board_row.append(counter)
                    counter += 1
            board.append(board_row)

        return board

    def _shuffle_board(self):
        """Trộn bàn cờ và đảm bảo nó có thể giải được"""
        # Làm phẳng bàn cờ
        flat_board = [tile for row in self.board for tile in row]

        # Trộn cho đến khi tìm được một trạng thái có thể giải
        valid_board = False
        max_attempts = 100
        attempts = 0

        while not valid_board and attempts < max_attempts:
            random.shuffle(flat_board)

            # Tìm vị trí ô trống mới
            empty_index = flat_board.index(0)
            empty_row = empty_index // self.size
            empty_col = empty_index % self.size

            # Kiểm tra trạng thái có thể giải được
            if is_solvable(flat_board, self.size, empty_row):
                valid_board = True

            attempts += 1

        # Nếu không tìm được trạng thái hợp lệ, tạo một trạng thái đơn giản
        if not valid_board:
            self.board = self._create_solved_board()
            # Di chuyển ô trống vài lần để tạo puzzle đơn giản
            for _ in range(20):
                row, col = self.empty_pos
                directions = []

                if row > 0: directions.append((-1, 0))  # lên
                if row < self.size - 1: directions.append((1, 0))  # xuống
                if col > 0: directions.append((0, -1))  # trái
                if col < self.size - 1: directions.append((0, 1))  # phải

                dr, dc = random.choice(directions)
                self._swap_tiles((row, col), (row + dr, col + dc))
            return

        # Cập nhật bàn cờ với danh sách đã trộn
        self.board = []
        for i in range(self.size):
            row_start = i * self.size
            self.board.append(flat_board[row_start:row_start + self.size])

        # Cập nhật vị trí ô trống
        self.empty_pos = (empty_row, empty_col)

    def get_tile_at_position(self, mouse_pos, tile_size, board_x, board_y):
        """Lấy ô tại vị trí chuột"""
        x, y = mouse_pos

        # Kiểm tra xem chuột có nằm trong bàn cờ không
        if (x < board_x or x >= board_x + self.size * tile_size or
                y < board_y or y >= board_y + self.size * tile_size):
            return None

        # Tính vị trí ô
        col = (x - board_x) // tile_size
        row = (y - board_y) // tile_size

        return (row, col)

    def can_move(self, pos):
        """Kiểm tra xem ô tại vị trí pos có thể di chuyển không"""
        if self.is_animating:
            return False

        row, col = pos
        empty_row, empty_col = self.empty_pos

        # Ô có thể di chuyển nếu nó nằm cùng hàng hoặc cùng cột với ô trống
        # và liền kề ô trống
        return ((row == empty_row and abs(col - empty_col) == 1) or
                (col == empty_col and abs(row - empty_row) == 1))

    def move_tile(self, pos):
        """Di chuyển ô tại vị trí pos"""
        if not self.can_move(pos):
            return False

        # Bắt đầu animation
        self.is_animating = True
        self.animation_start_time = time.time()
        self.animating_tile = self.board[pos[0]][pos[1]]
        self.animating_from = pos
        self.animating_to = self.empty_pos

        # Cập nhật bàn cờ ngay lập tức (logic)
        self._swap_tiles(pos, self.empty_pos)

        # Cập nhật số bước và lịch sử
        if not self.bot_active:
            self.moves += 1
            self.move_history.append(pos)
        else:
            self.bot_total_moves += 1

        return True

    def _swap_tiles(self, pos1, pos2):
        """Hoán đổi hai ô"""
        row1, col1 = pos1
        row2, col2 = pos2

        self.board[row1][col1], self.board[row2][col2] = self.board[row2][col2], self.board[row1][col1]

        # Cập nhật vị trí ô trống nếu cần
        if self.board[row1][col1] == 0:
            self.empty_pos = (row1, col1)
        elif self.board[row2][col2] == 0:
            self.empty_pos = (row2, col2)

    def update(self):
        """Cập nhật trạng thái game"""
        current_time = time.time()

        # Cập nhật thời gian trôi qua
        if self.game_active and not self.is_solved:
            self.elapsed_time = current_time - self.start_time

        # Xử lý animation
        if self.is_animating:
            elapsed = current_time - self.animation_start_time
            if elapsed >= self.animation_duration:
                self.is_animating = False

                # Kiểm tra xem game đã được giải chưa
                if not self.is_solved:
                    self.check_solved()

        # Xử lý bot tự động
        if self.bot_active and not self.is_animating and self.bot_moves:
            if current_time - self.bot_move_timer >= self.bot_move_delay:
                if self.bot_current_move < len(self.bot_moves):
                    next_move = self.bot_moves[self.bot_current_move]
                    self.move_tile(next_move)
                    self.bot_current_move += 1
                    self.bot_move_timer = current_time
                else:
                    self.bot_active = False

    def check_solved(self):
        """Kiểm tra xem puzzle đã được giải chưa"""
        solution = get_solution_state(self.size)
        current = [tile for row in self.board for tile in row]

        if current == solution:
            self.is_solved = True
            self.game_active = False

            # Lưu điểm số
            from score import ScoreManager
            score_manager = ScoreManager()
            score_manager.save_score(self.size, self.moves, self.elapsed_time, self.current_map)

            return True
        return False

    def start_bot(self, algorithm="bfs"):
        """Kích hoạt bot giải puzzle"""
        if self.is_solved or self.bot_active:
            return

        # Reset số bước của bot
        self.bot_total_moves = 0

        # Tìm các bước giải bằng thuật toán được chọn
        if algorithm == "hill_climbing":
            self.bot_moves = self.bot_solver.solve_hill_climbing()
        else:  # BFS
            self.bot_moves = self.bot_solver.solve_bfs()

        self.bot_active = True
        self.bot_current_move = 0
        self.bot_move_timer = time.time()

    def get_animation_progress(self):
        """Lấy tiến độ animation hiện tại (0 đến 1)"""
        if not self.is_animating:
            return 1.0

        elapsed = time.time() - self.animation_start_time
        progress = elapsed / self.animation_duration

        return min(progress, 1.0)