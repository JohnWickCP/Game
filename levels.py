import json
import os
from utils import is_solvable


class LevelManager:
    def __init__(self):
        self.levels_file = "data/levels.json"

        # Tạo thư mục data nếu chưa tồn tại
        os.makedirs("data", exist_ok=True)

        # Tạo file levels.json với các map mặc định nếu chưa tồn tại
        if not os.path.exists(self.levels_file):
            default_levels = {
                "3x3": self._create_default_3x3_levels(),
                "4x4": self._create_default_4x4_levels()
            }
            with open(self.levels_file, 'w') as f:
                json.dump(default_levels, f, indent=2)

    def _create_default_3x3_levels(self):
        """Tạo các map mặc định cho bàn cờ 3x3"""
        return [
            {
                "name": "Dễ 1",
                "board": [
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 0, 8]
                ],
                "empty_pos": [2, 1],
                "difficulty": "Dễ"
            },
            {
                "name": "Dễ 2",
                "board": [
                    [1, 2, 3],
                    [4, 0, 6],
                    [7, 5, 8]
                ],
                "empty_pos": [1, 1],
                "difficulty": "Dễ"
            },
            {
                "name": "Trung bình 1",
                "board": [
                    [1, 2, 3],
                    [4, 5, 0],
                    [7, 8, 6]
                ],
                "empty_pos": [1, 2],
                "difficulty": "Trung bình"
            },
            {
                "name": "Trung bình 2",
                "board": [
                    [1, 3, 0],
                    [4, 2, 5],
                    [7, 8, 6]
                ],
                "empty_pos": [0, 2],
                "difficulty": "Trung bình"
            },
            {
                "name": "Khó 1",
                "board": [
                    [2, 8, 3],
                    [1, 0, 4],
                    [7, 6, 5]
                ],
                "empty_pos": [1, 1],
                "difficulty": "Khó"
            },
            {
                "name": "Khó 2",
                "board": [
                    [2, 8, 3],
                    [7, 5, 4],
                    [1, 0, 6]
                ],
                "empty_pos": [2, 1],
                "difficulty": "Khó"
            }
        ]

    def _create_default_4x4_levels(self):
        """Tạo các map mặc định cho bàn cờ 4x4"""
        return [
            {
                "name": "Dễ 1",
                "board": [
                    [1, 2, 3, 4],
                    [5, 6, 7, 8],
                    [9, 10, 11, 12],
                    [13, 14, 0, 15]
                ],
                "empty_pos": [3, 2],
                "difficulty": "Dễ"
            },
            {
                "name": "Dễ 2",
                "board": [
                    [1, 2, 3, 4],
                    [5, 6, 7, 8],
                    [9, 10, 0, 11],
                    [13, 14, 15, 12]
                ],
                "empty_pos": [2, 2],
                "difficulty": "Dễ"
            },
            {
                "name": "Trung bình 1",
                "board": [
                    [1, 2, 3, 4],
                    [5, 6, 0, 8],
                    [9, 10, 7, 12],
                    [13, 14, 11, 15]
                ],
                "empty_pos": [1, 2],
                "difficulty": "Trung bình"
            },
            {
                "name": "Trung bình 2",
                "board": [
                    [1, 2, 3, 4],
                    [5, 0, 7, 8],
                    [9, 6, 10, 11],
                    [13, 14, 15, 12]
                ],
                "empty_pos": [1, 1],
                "difficulty": "Trung bình"
            },
            {
                "name": "Khó 1",
                "board": [
                    [5, 1, 8, 3],
                    [9, 6, 7, 4],
                    [13, 2, 0, 12],
                    [14, 10, 11, 15]
                ],
                "empty_pos": [2, 2],
                "difficulty": "Khó"
            },
            {
                "name": "Khó 2",
                "board": [
                    [5, 1, 3, 4],
                    [9, 6, 8, 0],
                    [13, 2, 7, 12],
                    [14, 10, 11, 15]
                ],
                "empty_pos": [1, 3],
                "difficulty": "Khó"
            }
        ]

    def get_all_levels(self, size):
        """
        Lấy tất cả các map cho kích thước bàn cờ

        Args:
            size: Kích thước bàn cờ (3 hoặc 4)

        Returns:
            list: Danh sách các map
        """
        levels = self._load_levels()
        key = f"{size}x{size}"

        if key in levels:
            return levels[key]
        return []

    def get_level_by_name(self, size, name):
        """
        Lấy map theo tên

        Args:
            size: Kích thước bàn cờ (3 hoặc 4)
            name: Tên map

        Returns:
            dict: Thông tin map, hoặc None nếu không tìm thấy
        """
        levels = self.get_all_levels(size)

        for level in levels:
            if level["name"] == name:
                return level

        return None

    def get_levels_by_difficulty(self, size, difficulty):
        """
        Lấy danh sách map theo độ khó

        Args:
            size: Kích thước bàn cờ (3 hoặc 4)
            difficulty: Độ khó ("Dễ", "Trung bình", "Khó")

        Returns:
            list: Danh sách các map có độ khó tương ứng
        """
        levels = self.get_all_levels(size)
        return [level for level in levels if level["difficulty"] == difficulty]

    def add_level(self, size, board, empty_pos, name, difficulty):
        """
        Thêm map mới

        Args:
            size: Kích thước bàn cờ (3 hoặc 4)
            board: Trạng thái bàn cờ (list 2D)
            empty_pos: Vị trí ô trống [row, col]
            name: Tên map
            difficulty: Độ khó ("Dễ", "Trung bình", "Khó")

        Returns:
            bool: True nếu thêm thành công, False nếu không
        """
        # Kiểm tra bàn cờ có hợp lệ không
        flat_board = [tile for row in board for tile in row]
        if not is_solvable(flat_board, size, empty_pos[0]):
            return False

        levels = self._load_levels()
        key = f"{size}x{size}"

        if key not in levels:
            levels[key] = []

        # Kiểm tra xem tên đã tồn tại chưa
        for level in levels[key]:
            if level["name"] == name:
                return False

        # Thêm map mới
        new_level = {
            "name": name,
            "board": board,
            "empty_pos": empty_pos,
            "difficulty": difficulty
        }

        levels[key].append(new_level)
        self._save_levels(levels)

        return True

    def _load_levels(self):
        """Đọc dữ liệu map từ file"""
        try:
            with open(self.levels_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Nếu file không tồn tại hoặc không đọc được, tạo mới
            return {
                "3x3": self._create_default_3x3_levels(),
                "4x4": self._create_default_4x4_levels()
            }

    def _save_levels(self, levels):
        """Lưu dữ liệu map vào file"""
        with open(self.levels_file, 'w') as f:
            json.dump(levels, f, indent=2)