# Các hằng số cho game

# Màu sắc
BACKGROUND_COLOR = (240, 240, 240)  # Xám nhạt
TILE_COLOR = (50, 150, 220)  # Xanh dương
TILE_BORDER_COLOR = (30, 100, 180)  # Xanh đậm
TEXT_COLOR = (255, 255, 255)  # Trắng
BUTTON_COLOR = (80, 180, 80)  # Xanh lá
BUTTON_HOVER_COLOR = (100, 200, 100)  # Xanh lá nhạt
SOLVED_COLOR = (255, 215, 0)  # Vàng

# Cấu hình game
ANIMATION_DURATION = 0.2  # Thời gian animation (giây)
BOT_MOVE_DELAY = 0.5  # Thời gian delay giữa các bước của bot (giây)
MAX_HIGH_SCORES = 10  # Số lượng điểm cao tối đa được lưu cho mỗi loại bàn
MAX_HIGH_SCORES_PER_MAP = 5  # Số lượng điểm cao tối đa được lưu cho mỗi map

#Kich thuoc man hinh
WIDTH, HEIGHT = 1000, 700  # Tăng kích thước từ 800x600 lên 1000x700
FPS = 60

# Độ khó
MIN_MOVES_3X3 = 20  # Số bước tối thiểu lý thuyết cho bàn 3x3
MIN_MOVES_4X4 = 50  # Số bước tối thiểu lý thuyết cho bàn 4x4

# Cấu hình UI
BOARD_SIZE = 400  # Kích thước tối đa của bàn chơi
TILE_MARGIN = 4  # Khoảng cách giữa các ô
BUTTON_WIDTH = 100  # Chiều rộng nút
BUTTON_HEIGHT = 40  # Chiều cao nút
BUTTON_SPACING = 10  # Khoảng cách giữa các nút
DROPDOWN_WIDTH = 150  # Chiều rộng dropdown
DROPDOWN_HEIGHT = 40  # Chiều cao dropdown
DROPDOWN_SPACING = 60  # Khoảng cách giữa các dropdown

# Đường dẫn file
DATA_DIRECTORY = "data"
LEVELS_FILE = "data/levels.json"
SCORES_FILE = "data/scores.json"