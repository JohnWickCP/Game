import heapq
import time

def _convert_path_to_moves(path):
    """Chuyển đổi path thành danh sách các vị trí di chuyển"""
    # Trong trường hợp này, path đã là danh sách các vị trí di chuyển
    return path


class BotSolver:
    def __init__(self, game):
        self.game = game
        self.size = game.size
        self.solution_state = self._generate_solution_state()

    def _generate_solution_state(self):
        """Tạo trạng thái đích cho puzzle"""
        solution = []
        for i in range(self.size):
            for j in range(self.size):
                if i == self.size - 1 and j == self.size - 1:
                    solution.append(0)  # Ô trống ở cuối
                else:
                    solution.append(i * self.size + j + 1)
        return solution

    def solve_best_first_search(self):
        """Giải puzzle bằng thuật toán Best First Search"""
        print("Starting Best First Search solver...")
        start_time = time.time()

        # Chuyển đổi bàn cờ từ 2D sang mảng 1D
        start_state = []
        for row in self.game.board:
            for tile in row:
                start_state.append(tile)

        # Priority queue cho Best First Search (sử dụng heapq)
        # (heuristic, state, path)
        start_heuristic = self._manhattan_distance(start_state)
        open_set = [(start_heuristic, start_state, [])]
        heapq.heapify(open_set)

        # Đánh dấu các trạng thái đã thăm
        visited = {tuple(start_state)}

        max_iterations = 10000  # Giới hạn số lần lặp
        iterations = 0

        while open_set and iterations < max_iterations:
            iterations += 1

            # Lấy trạng thái có heuristic nhỏ nhất
            _, state, path = heapq.heappop(open_set)

            # Kiểm tra nếu đã tìm được giải pháp
            if self._is_goal_state(state):
                print(
                    f"Best First Search found solution in {iterations} iterations and {time.time() - start_time:.2f} seconds")
                print(f"Solution length: {len(path)} steps")
                return _convert_path_to_moves(path)

            # Tạo các trạng thái tiếp theo
            empty_index = state.index(0)
            empty_row, empty_col = empty_index // self.size, empty_index % self.size

            # Xét 4 hướng di chuyển: lên, xuống, trái, phải
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for dr, dc in directions:
                new_row, new_col = empty_row + dr, empty_col + dc

                # Kiểm tra nếu vị trí mới nằm trong bàn cờ
                if 0 <= new_row < self.size and 0 <= new_col < self.size:
                    # Tạo trạng thái mới
                    new_state = state.copy()

                    # Tính chỉ số trong mảng 1D
                    new_index = new_row * self.size + new_col

                    # Hoán đổi ô trống với ô mới
                    new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]

                    # Lưu vị trí ô di chuyển (row, col)
                    move_pos = (new_row, new_col)

                    # Nếu trạng thái mới chưa được thăm
                    if tuple(new_state) not in visited:
                        visited.add(tuple(new_state))
                        # Tính giá trị heuristic mới
                        new_heuristic = self._manhattan_distance(new_state)
                        # Thêm vào priority queue
                        heapq.heappush(open_set, (new_heuristic, new_state, path + [move_pos]))

        print(f"Best First Search failed to find solution after {iterations} iterations")
        # Nếu không tìm được giải pháp, trả về danh sách rỗng
        return []

    def solve_hill_climbing(self):
        """Giải puzzle bằng thuật toán Hill Climbing"""
        print("Starting Hill Climbing solver...")
        start_time = time.time()

        # Chuyển đổi bàn cờ từ 2D sang mảng 1D
        start_state = []
        for row in self.game.board:
            for tile in row:
                start_state.append(tile)

        current_state = start_state
        current_cost = self._manhattan_distance(current_state)

        path = []  # Lưu các vị trí di chuyển
        visited = {tuple(current_state)}

        max_iterations = 1000  # Giới hạn số lần lặp
        iterations = 0

        while iterations < max_iterations:
            iterations += 1

            if self._is_goal_state(current_state):
                print(
                    f"Hill Climbing found solution in {iterations} iterations and {time.time() - start_time:.2f} seconds")
                print(f"Solution length: {len(path)} steps")
                return path

            # Tìm trạng thái kế tiếp tốt nhất
            empty_index = current_state.index(0)
            empty_row, empty_col = empty_index // self.size, empty_index % self.size

            # Xét 4 hướng di chuyển: lên, xuống, trái, phải
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            best_state = None
            best_cost = current_cost
            best_move = None

            for dr, dc in directions:
                new_row, new_col = empty_row + dr, empty_col + dc

                # Kiểm tra nếu vị trí mới nằm trong bàn cờ
                if 0 <= new_row < self.size and 0 <= new_col < self.size:
                    # Tạo trạng thái mới
                    new_state = current_state.copy()

                    # Tính chỉ số trong mảng 1D
                    new_index = new_row * self.size + new_col

                    # Hoán đổi ô trống với ô mới
                    new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]

                    # Nếu trạng thái mới chưa được thăm
                    if tuple(new_state) not in visited:
                        new_cost = self._manhattan_distance(new_state)
                        if new_cost < best_cost:
                            best_cost = new_cost
                            best_state = new_state
                            best_move = (new_row, new_col)

            # Nếu không tìm được trạng thái tốt hơn
            if best_state is None:
                print(f"Hill Climbing stuck at local minimum after {iterations} iterations")
                return path

            # Cập nhật trạng thái hiện tại
            current_state = best_state
            current_cost = best_cost
            visited.add(tuple(current_state))
            path.append(best_move)

        print(f"Hill Climbing did not find solution after {iterations} iterations")
        return path

    def _is_goal_state(self, state):
        """Kiểm tra xem trạng thái hiện tại có phải là trạng thái đích không"""
        for i in range(len(state)):
            if state[i] != self.solution_state[i]:
                return False
        return True

    def _manhattan_distance(self, state):
        """Tính khoảng cách Manhattan giữa trạng thái hiện tại và trạng thái đích"""
        distance = 0

        for i in range(len(state)):
            if state[i] == 0:  # Bỏ qua ô trống
                continue

            # Vị trí hiện tại
            curr_row, curr_col = i // self.size, i % self.size

            # Vị trí đích (trong solution_state, số 1 ở vị trí 0, số 2 ở vị trí 1, ...)
            target_pos = state[i] - 1
            target_row, target_col = target_pos // self.size, target_pos % self.size

            # Cộng khoảng cách Manhattan
            distance += abs(curr_row - target_row) + abs(curr_col - target_col)

        return distance