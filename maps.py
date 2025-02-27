# Định nghĩa các map cố định cho game

# Maps cho bàn 3x3
MAPS_3X3 = [
    {
        "name": "Map 1",
        "board": [
            [1, 2, 3],
            [4, 5, 6],
            [7, 0, 8]
        ],
        "empty_pos": [2, 1]
    },
    {
        "name": "Map 2",
        "board": [
            [1, 2, 3],
            [4, 0, 6],
            [7, 5, 8]
        ],
        "empty_pos": [1, 1]
    },
    {
        "name": "Map 3",
        "board": [
            [1, 3, 0],
            [4, 2, 5],
            [7, 8, 6]
        ],
        "empty_pos": [0, 2]
    },
    {
        "name": "Map 4",
        "board": [
            [2, 8, 3],
            [1, 0, 4],
            [7, 6, 5]
        ],
        "empty_pos": [1, 1]
    }
]

# Maps cho bàn 4x4
MAPS_4X4 = [
    {
        "name": "Map 1",
        "board": [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 0, 15]
        ],
        "empty_pos": [3, 2]
    },
    {
        "name": "Map 2",
        "board": [
            [1, 2, 3, 4],
            [5, 6, 0, 8],
            [9, 10, 7, 12],
            [13, 14, 11, 15]
        ],
        "empty_pos": [1, 2]
    },
    {
        "name": "Map 3",
        "board": [
            [5, 1, 3, 4],
            [9, 6, 0, 8],
            [13, 2, 7, 12],
            [14, 10, 11, 15]
        ],
        "empty_pos": [1, 2]
    },
    {
        "name": "Map 4",
        "board": [
            [5, 1, 8, 3],
            [9, 6, 7, 4],
            [13, 2, 0, 12],
            [14, 10, 11, 15]
        ],
        "empty_pos": [2, 2]
    }
]


def get_maps(size):
    """
    Lấy danh sách các map cho kích thước bàn cờ

    Args:
        size: Kích thước bàn cờ (3 hoặc 4)

    Returns:
        list: Danh sách các map
    """
    if size == 3:
        return MAPS_3X3
    elif size == 4:
        return MAPS_4X4
    else:
        return []


def get_map_by_name(size, name):
    """
    Lấy map theo tên

    Args:
        size: Kích thước bàn cờ (3 hoặc 4)
        name: Tên map

    Returns:
        dict: Thông tin map, hoặc None nếu không tìm thấy
    """
    maps = get_maps(size)

    for map_data in maps:
        if map_data["name"] == name:
            return map_data

    return None