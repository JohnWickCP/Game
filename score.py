import json
import os
from utils import calculate_score, format_time
from constants import DATA_DIRECTORY, SCORES_FILE, MAX_HIGH_SCORES, MAX_HIGH_SCORES_PER_MAP


class ScoreManager:
    def __init__(self):
        self.scores_file = SCORES_FILE

        # Tạo thư mục data nếu chưa tồn tại
        os.makedirs(DATA_DIRECTORY, exist_ok=True)

        # Tạo file scores.json với cấu trúc mặc định nếu chưa tồn tại
        if not os.path.exists(self.scores_file):
            default_scores = {
                "3x3": {
                    "random": [],  # Điểm cho map ngẫu nhiên
                    "maps": {}  # Điểm cho các map cụ thể
                },
                "4x4": {
                    "random": [],  # Điểm cho map ngẫu nhiên
                    "maps": {}  # Điểm cho các map cụ thể
                }
            }
            with open(self.scores_file, 'w') as f:
                json.dump(default_scores, f)

    def save_score(self, size, moves, time_elapsed, map_name=None):
        """
        Lưu điểm số mới

        Args:
            size: Kích thước bàn cờ (3 hoặc 4)
            moves: Số bước đi
            time_elapsed: Thời gian hoàn thành (giây)
            map_name: Tên map cụ thể (None nếu là map ngẫu nhiên)

        Returns:
            dict: Thông tin điểm số vừa lưu
        """
        # Tính điểm
        score = calculate_score(moves, time_elapsed, size)

        # Đọc dữ liệu điểm hiện tại
        scores = self._load_scores()

        # Thêm điểm mới
        key = f"{size}x{size}"

        new_score = {
            "moves": moves,
            "time": int(time_elapsed),
            "time_formatted": format_time(time_elapsed),
            "score": score,
            "date": self._get_current_date()
        }

        # Đảm bảo key tồn tại và có cấu trúc đúng
        if key not in scores:
            scores[key] = {
                "random": [],
                "maps": {}
            }
        # Đảm bảo cấu trúc dữ liệu là đúng
        elif not isinstance(scores[key], dict):
            scores[key] = {
                "random": [],
                "maps": {}
            }
        # Đảm bảo các khóa con tồn tại
        else:
            if "random" not in scores[key]:
                scores[key]["random"] = []
            if "maps" not in scores[key]:
                scores[key]["maps"] = {}

        if map_name is None:
            # Map ngẫu nhiên
            scores[key]["random"].append(new_score)
            # Sắp xếp theo điểm cao đến thấp
            scores[key]["random"] = sorted(scores[key]["random"], key=lambda x: x["score"], reverse=True)
            # Chỉ giữ lại một số điểm cao nhất
            scores[key]["random"] = scores[key]["random"][:MAX_HIGH_SCORES]
        else:
            # Map cụ thể
            if map_name not in scores[key]["maps"]:
                scores[key]["maps"][map_name] = []

            scores[key]["maps"][map_name].append(new_score)
            # Sắp xếp theo điểm cao đến thấp
            scores[key]["maps"][map_name] = sorted(scores[key]["maps"][map_name], key=lambda x: x["score"],
                                                   reverse=True)
            # Chỉ giữ lại một số điểm cao nhất cho mỗi map
            scores[key]["maps"][map_name] = scores[key]["maps"][map_name][:MAX_HIGH_SCORES_PER_MAP]

        # Lưu lại
        self._save_scores(scores)

        return new_score

    def get_high_scores(self, size, map_name=None):
        """
        Lấy danh sách điểm cao

        Args:
            size: Kích thước bàn cờ (3 hoặc 4)
            map_name: Tên map cụ thể (None nếu là map ngẫu nhiên)

        Returns:
            list: Danh sách điểm cao
        """
        scores = self._load_scores()
        key = f"{size}x{size}"

        if key not in scores:
            return []

        # Kiểm tra xem có phải là dictionary không
        if not isinstance(scores[key], dict):
            return []

        if map_name is None:
            # Map ngẫu nhiên
            if "random" not in scores[key]:
                return []
            return scores[key]["random"]
        else:
            # Map cụ thể
            if "maps" not in scores[key]:
                return []
            if map_name not in scores[key]["maps"]:
                return []
            return scores[key]["maps"][map_name]

    def get_best_score_for_map(self, size, map_name):
        """
        Lấy điểm cao nhất cho một map cụ thể

        Args:
            size: Kích thước bàn cờ (3 hoặc 4)
            map_name: Tên map

        Returns:
            dict: Thông tin điểm cao nhất, hoặc None nếu không có
        """
        high_scores = self.get_high_scores(size, map_name)
        if high_scores and len(high_scores) > 0:
            return high_scores[0]
        return None

    def _load_scores(self):
        """Đọc dữ liệu điểm từ file"""
        try:
            with open(self.scores_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Nếu file không tồn tại hoặc không đọc được, tạo mới
            return {
                "3x3": {"random": [], "maps": {}},
                "4x4": {"random": [], "maps": {}}
            }

    def _save_scores(self, scores):
        """Lưu dữ liệu điểm vào file"""
        with open(self.scores_file, 'w') as f:
            json.dump(scores, f, indent=2)

    def _get_current_date(self):
        """Lấy ngày giờ hiện tại dưới dạng chuỗi"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M")