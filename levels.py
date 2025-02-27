import json
import os
from utils import is_solvable
from maps import MAPS_3X3, MAPS_4X4
from constants import LEVELS_FILE


class LevelManager:
    def __init__(self):
        self.levels_file = LEVELS_FILE

        # Tạo thư mục data nếu chưa tồn tại
        os.makedirs("data", exist_ok=True)

        # Tạo file levels.json với các map mặc định nếu chưa tồn tại
        if not os.path.exists(self.levels_file):
            default_levels = {
                "3x3": MAPS_3X3,
                "4x4": MAPS_4X4
            }
            with open(self.levels_file, 'w') as f:
                json.dump(default_levels, f, indent=2)

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

    def add_level(self, size, board, empty_pos, name):
        """
        Thêm map mới

        Args:
            size: Kích thước bàn cờ (3 hoặc 4)
            board: Trạng thái bàn cờ (list 2D)
            empty_pos: Vị trí ô trống [row, col]
            name: Tên map

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
            "empty_pos": empty_pos
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
                "3x3": MAPS_3X3,
                "4x4": MAPS_4X4
            }

    def _save_levels(self, levels):
        """Lưu dữ liệu map vào file"""
        with open(self.levels_file, 'w') as f:
            json.dump(levels, f, indent=2)