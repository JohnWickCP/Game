import json
import os
from utils import calculate_score, format_time

class ScoreManager:
    def __init__(self):
        self.scores_file = "data/scores.json"
        
        # Tạo thư mục data nếu chưa tồn tại
        os.makedirs("data", exist_ok=True)
        
        # Tạo file scores.json với cấu trúc mặc định nếu chưa tồn tại
        if not os.path.exists(self.scores_file):
            default_scores = {
                "3x3": [],
                "4x4": []
            }
            with open(self.scores_file, 'w') as f:
                json.dump(default_scores, f)
    
    def save_score(self, size, moves, time_elapsed):
        """
        Lưu điểm số mới
        
        Args:
            size: Kích thước bàn cờ (3 hoặc 4)
            moves: Số bước đi
            time_elapsed: Thời gian hoàn thành (giây)
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
        
        if key not in scores:
            scores[key] = []
        
        scores[key].append(new_score)
        
        # Sắp xếp theo điểm cao đến thấp
        scores[key] = sorted(scores[key], key=lambda x: x["score"], reverse=True)
        
        # Chỉ giữ lại 10 điểm cao nhất
        scores[key] = scores[key][:10]
        
        # Lưu lại
        self._save_scores(scores)
        
        return new_score
    
    def get_high_scores(self, size):
        """
        Lấy danh sách điểm cao
        
        Args:
            size: Kích thước bàn cờ (3 hoặc 4)
            
        Returns:
            list: Danh sách điểm cao
        """
        scores = self._load_scores()
        key = f"{size}x{size}"
        
        if key in scores:
            return scores[key]
        return []
    
    def _load_scores(self):
        """Đọc dữ liệu điểm từ file"""
        try:
            with open(self.scores_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Nếu file không tồn tại hoặc không đọc được, tạo mới
            return {"3x3": [], "4x4": []}
    
    def _save_scores(self, scores):
        """Lưu dữ liệu điểm vào file"""
        with open(self.scores_file, 'w') as f:
            json.dump(scores, f, indent=2)
    
    def _get_current_date(self):
        """Lấy ngày giờ hiện tại dưới dạng chuỗi"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M")