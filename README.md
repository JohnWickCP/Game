# Sliding Puzzle Game

## Giới thiệu
Sliding Puzzle Game là một trò chơi xếp hình trượt được phát triển bằng Python và Pygame. Người chơi sẽ di chuyển các ô để sắp xếp chúng theo thứ tự từ 1 đến n (với n là tổng số ô - 1), với một ô trống ở vị trí cuối cùng.

## Tính năng
- Hỗ trợ hai kích thước bàn chơi: 3x3 và 4x4
- 4 map có sẵn cho mỗi kích thước bàn chơi
- Tạo bàn chơi ngẫu nhiên có thể giải được
- Hiệu ứng animation khi di chuyển ô
- Hai thuật toán giải tự động: BFS (Breadth-First Search) và Hill Climbing
- Hệ thống lưu và hiển thị điểm cao
- Theo dõi lịch sử nước đi
- Hình ảnh tham khảo trạng thái hoàn thành

## Cài đặt
1. Đảm bảo Python đã được cài đặt (phiên bản 3.6 trở lên)
2. Cài đặt thư viện Pygame:
   ```
   pip install pygame
   ```
3. Tải xuống toàn bộ mã nguồn
4. Chạy file `main.py` để bắt đầu trò chơi:
   ```
   python main.py
   ```

## Cách chơi
1. Sử dụng chuột để di chuyển các ô kề với ô trống
2. Sắp xếp các số theo thứ tự từ 1 đến n
3. Hoàn thành bàn chơi khi tất cả các số đều nằm đúng vị trí

## Giao diện
- **New 3x3/4x4**: Bắt đầu trò chơi mới với kích thước bàn tương ứng
- **Maps 3x3/4x4**: Danh sách các map có sẵn để chọn
- **Solve BFS**: Giải tự động bằng thuật toán BFS
- **Hill Climbing**: Giải tự động bằng thuật toán Hill Climbing
- **Reference**: Hiển thị trạng thái hoàn thành của bàn chơi
- **High Scores**: Hiển thị điểm cao nhất
- **Move History**: Hiển thị lịch sử các nước đi

## Cấu trúc dự án
- `main.py`: Điểm khởi chạy chương trình
- `game.py`: Quản lý logic chính của trò chơi
- `ui.py`: Xử lý giao diện người dùng
- `bot.py`: Chứa các thuật toán giải tự động
- `levels.py`: Quản lý các màn chơi
- `maps.py`: Chứa các map cố định
- `score.py`: Quản lý điểm số
- `utils.py`: Các hàm tiện ích
- `constants.py`: Các hằng số được sử dụng trong game
- `data/`: Thư mục chứa dữ liệu (điểm số, màn chơi)

## Thuật toán
### BFS (Breadth-First Search)
Thuật toán tìm kiếm theo chiều rộng để tìm lời giải ngắn nhất. BFS đảm bảo tìm được lời giải tối ưu (ít bước nhất) nhưng có thể chậm với bàn chơi 4x4.

### Hill Climbing
Thuật toán tìm kiếm cục bộ sử dụng hàm heuristic (khoảng cách Manhattan) để dẫn đường tìm lời giải. Hill Climbing nhanh hơn BFS nhưng không đảm bảo tìm được lời giải tối ưu.

## Tính toán điểm số
Điểm số được tính dựa trên:
- Số bước di chuyển
- Thời gian hoàn thành
- Kích thước bàn chơi

Công thức tính điểm:
```
điểm = điểm_cơ_bản - (số_bước - số_bước_tối_thiểu) * 10 - thời_gian * 0.5
```

## Phát triển dự án
Để phát triển thêm, bạn có thể:
1. Thêm các kích thước bàn chơi mới (5x5, 6x6...)
2. Thêm các thuật toán giải tự động khác (A*, IDA*)
3. Thêm tính năng undo/redo
4. Thêm tùy chọn hình ảnh thay vì số
5. Thêm âm thanh và hiệu ứng
6. Phát triển chế độ chơi nhiều người

## Giấy phép
Dự án này được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.
