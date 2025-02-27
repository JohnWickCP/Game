from constants import MIN_MOVES_3X3, MIN_MOVES_4X4

def is_solvable(flat_board, size, empty_row):
    """
    Kiểm tra xem bàn cờ có thể giải được không

    Args:
        flat_board: Danh sách 1D chứa các số trên bàn cờ
        size: Kích thước bàn cờ (3 hoặc 4)
        empty_row: Hàng của ô trống (tính từ 0)

    Returns:
        bool: True nếu có thể giải được, False nếu không
    """
    # Tính số đảo ngược (inversion count)
    inversions = 0
    for i in range(len(flat_board)):
        if flat_board[i] == 0:  # Bỏ qua ô trống
            continue

        for j in range(i + 1, len(flat_board)):
            if flat_board[j] == 0:  # Bỏ qua ô trống
                continue

            if flat_board[i] > flat_board[j]:
                inversions += 1

    # Kiểm tra theo quy tắc
    if size % 2 == 1:  # Bàn cờ 3x3
        return inversions % 2 == 0
    else:  # Bàn cờ 4x4
        # Nếu hàng ô trống (tính từ dưới lên) là lẻ,
        # số đảo ngược phải chẵn để có thể giải được
        if (size - empty_row) % 2 == 1:
            return inversions % 2 == 0
        # Nếu hàng ô trống (tính từ dưới lên) là chẵn,
        # số đảo ngược phải lẻ để có thể giải được
        else:
            return inversions % 2 == 1


def get_solution_state(size):
    """
    Tạo trạng thái đã giải của bàn cờ

    Args:
        size: Kích thước bàn cờ (3 hoặc 4)

    Returns:
        list: Danh sách 1D chứa các số theo thứ tự đúng
    """
    solution = []
    for i in range(1, size * size):
        solution.append(i)
    solution.append(0)  # Ô trống ở cuối

    return solution


def get_tile_position(tile, board, size):
    """
    Tìm vị trí của một ô trên bàn cờ

    Args:
        tile: Giá trị của ô cần tìm
        board: Bàn cờ hiện tại (list 2D)
        size: Kích thước bàn cờ

    Returns:
        tuple: (row, col) là vị trí của ô, hoặc None nếu không tìm thấy
    """
    for row in range(size):
        for col in range(size):
            if board[row][col] == tile:
                return (row, col)

    return None


def format_time(seconds):
    """
    Định dạng thời gian từ giây sang phút:giây

    Args:
        seconds: Số giây

    Returns:
        str: Thời gian định dạng "MM:SS"
    """
    minutes = int(seconds) // 60
    secs = int(seconds) % 60

    return f"{minutes:02d}:{secs:02d}"


def calculate_score(moves, time, size):
    """
    Tính điểm dựa trên số bước và thời gian

    Args:
        moves: Số bước đi
        time: Thời gian (giây)
        size: Kích thước bàn cờ

    Returns:
        int: Điểm số
    """
    # Số bước tối thiểu lý thuyết (không thực tế)
    min_moves = {
        3: MIN_MOVES_3X3,  # 3x3
        4: MIN_MOVES_4X4  # 4x4
    }

    # Càng ít bước và thời gian càng tốt
    time_factor = 0.5  # Trọng số của thời gian

    base_score = 10000
    move_penalty = max(0, moves - min_moves[size]) * 10
    time_penalty = time * time_factor

    score = base_score - move_penalty - time_penalty

    return max(0, int(score))