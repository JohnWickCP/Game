import pygame
import sys
from game import Game
from ui import UI
from constants import WIDTH, HEIGHT, FPS

def main():
    # Khởi tạo pygame
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Sliding Puzzle Game")

    # Cấu hình cơ bản - Tăng kích thước màn hình

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()


    # Khởi tạo các thành phần game
    game = Game()
    ui = UI(screen, game)

    # Vòng lặp chính
    running = True
    while running:
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Xử lý các sự kiện chuột và phím
            ui.handle_event(event)

        # Cập nhật trạng thái game
        game.update()

        # Vẽ giao diện
        screen.fill((240, 240, 240))  # Màu nền
        ui.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()