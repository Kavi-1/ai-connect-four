"""Simple Pygame GUI for Connect Four (human X vs AI O).

Usage: python3 gui_pygame.py

Requires: pygame (pip install pygame)
"""
import sys
import threading
import pygame
from connect4.board import Board
from connect4.ai_player import AIPlayer


CELL_SIZE = 100
RADIUS = CELL_SIZE // 2 - 6
FPS = 30

COLORS = {
    'bg': (28, 170, 156),
    'board': (0, 0, 0),
    'X': (200, 30, 30),
    'O': (240, 240, 60),
    'text': (255, 255, 255)
}


def draw_board(screen, board):
    h = board.height
    w = board.width
    # draw background
    screen.fill(COLORS['bg'])
    # draw grid
    for r in range(h):
        for c in range(w):
            x = c * CELL_SIZE + CELL_SIZE // 2
            y = r * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.rect(screen, COLORS['board'], (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            slot = board.slots[r][c]
            if slot == 'X':
                pygame.draw.circle(screen, COLORS['X'], (x, y), RADIUS)
            elif slot == 'O':
                pygame.draw.circle(screen, COLORS['O'], (x, y), RADIUS)
            else:
                pygame.draw.circle(screen, (230, 230, 230), (x, y), RADIUS)


def main():
    pygame.init()
    WIDTH = 7
    HEIGHT = 6
    size = (WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Connect Four - Human (X) vs AI (O)')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 20)
    # start menu state
    menu_running = True
    mode = 0  # 0: Human vs AI, 1: Human vs Human, 2: AI vs AI
    lookahead = 1
    algos = ['MINIMAX', 'ALPHABETA']
    algo_idx = 0

    base_y = 40

    menu_btn_rects = []
    menu_plus_rect = None
    menu_minus_rect = None
    
    menu_alg_btn_rects = []
    menu_start_rect = None

    def draw_menu():
        """Minimal centered menu: title, compact mode buttons, small controls, Start.

        This computes exact pygame.Rects for interactive elements and stores them
        in outer-scope variables so the event loop can test collisions against
        the same geometry (prevents mismatch and overlap issues).
        """
        nonlocal menu_btn_rects, menu_plus_rect, menu_minus_rect, menu_alg_btn_rects, menu_start_rect

        screen.fill(COLORS['bg'])
        cx = screen.get_width() // 2
        y = base_y

        # title
        title = font.render('Connect Four', True, COLORS['text'])
        screen.blit(title, (cx - title.get_width() // 2, y))
        y += 56

        mode_labels = ['Human vs AI', 'Human vs Human', 'AI vs AI']
        btns = []
        spacing = 18
        total_w = sum([small_font.size(m)[0] + 28 for m in mode_labels]) + spacing * (len(mode_labels) - 1)
        start_x = cx - total_w // 2
        x = start_x
        for i, m in enumerate(mode_labels):
            w = small_font.size(m)[0] + 28
            rect = pygame.Rect(x, y, w, 34)
            color = (90, 180, 90) if i == mode else (80, 80, 110)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            txt = small_font.render(m, True, COLORS['text'])
            screen.blit(txt, (rect.x + (w - txt.get_width()) // 2, rect.y + 6))
            btns.append(rect)
            x += w + spacing
        menu_btn_rects = btns

        y += 60

        la_label = small_font.render('Lookahead', True, (220, 220, 220))
        la_x = cx - 60
        screen.blit(la_label, (la_x, y))
        plus_rect = pygame.Rect(la_x + 110, y, 28, 28)
        minus_rect = pygame.Rect(plus_rect.x + 36, y, 28, 28)
        pygame.draw.rect(screen, (120, 120, 120), plus_rect, border_radius=6)
        pygame.draw.rect(screen, (120, 120, 120), minus_rect, border_radius=6)
        screen.blit(small_font.render('+', True, COLORS['text']), (plus_rect.x + 6, plus_rect.y + 2))
        screen.blit(small_font.render('-', True, COLORS['text']), (minus_rect.x + 8, minus_rect.y + 2))
        val = small_font.render(str(lookahead), True, COLORS['text'])
        screen.blit(val, (la_x + 70, y + 2))
        menu_plus_rect = plus_rect
        menu_minus_rect = minus_rect

        y += 48
        alg_labels = algos
        spacing = 18
        total_w = sum([small_font.size(a)[0] + 28 for a in alg_labels]) + spacing * (len(alg_labels) - 1)
        start_x = cx - total_w // 2
        x = start_x
        alg_btns = []
        for i, a in enumerate(alg_labels):
            w = small_font.size(a)[0] + 28
            rect = pygame.Rect(x, y, w, 34)
            color = (90, 120, 200) if i == algo_idx else (80, 80, 110)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            txt = small_font.render(a, True, COLORS['text'])
            screen.blit(txt, (rect.x + (w - txt.get_width()) // 2, rect.y + 6))
            alg_btns.append(rect)
            x += w + spacing
        menu_alg_btn_rects = alg_btns

        y += 64
        start_rect = pygame.Rect(cx - 68, y, 136, 40)
        pygame.draw.rect(screen, (60, 130, 60), start_rect, border_radius=8)
        start_txt = small_font.render('Start', True, COLORS['text'])
        screen.blit(start_txt, (start_rect.x + (start_rect.width - start_txt.get_width()) // 2,
                                start_rect.y + (start_rect.height - start_txt.get_height()) // 2))
        menu_start_rect = start_rect

        pygame.display.flip()

    while True:
        while menu_running:
            draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    for i, r in enumerate(menu_btn_rects):
                        if r.collidepoint(mx, my):
                            mode = i

                    if menu_plus_rect and menu_plus_rect.collidepoint(mx, my):
                        lookahead = max(0, lookahead + 1)
                    if menu_minus_rect and menu_minus_rect.collidepoint(mx, my):
                        lookahead = max(0, lookahead - 1)

                    for i, r in enumerate(menu_alg_btn_rects):
                        if r.collidepoint(mx, my):
                            algo_idx = i

                    if menu_start_rect and menu_start_rect.collidepoint(mx, my):
                        menu_running = False

        b = Board(HEIGHT, WIDTH)
        ai_X = None
        ai_O = None
        if mode == 0:
            # Human X, AI O
            ai_O = AIPlayer('O', 'RANDOM', lookahead, algos[algo_idx])
        elif mode == 1:
            # Human X, Human O
            pass
        else:
            # AI X, AI O
            ai_X = AIPlayer('X', 'RANDOM', lookahead, algos[algo_idx])
            ai_O = AIPlayer('O', 'RANDOM', lookahead, algos[algo_idx])

        current = 'X'
        running = True
        message = ''
        ai_thinking = False

        # helper to run AI move in background and update shared state
        def start_ai_move(ai_player, checker, next_player):
            def worker():
                nonlocal ai_thinking, current, message
                try:
                    ai_thinking = True
                    col = ai_player.next_move(b)
                    if 0 <= col < b.width and b.can_add_to(col):
                        b.add_checker(checker, col)
                        if b.is_win_for(checker):
                            message = f'{checker} wins!'
                        elif b.is_full():
                            message = "It's a tie!"
                except Exception as e:
                    message = 'AI error: ' + str(e)
                finally:
                    ai_thinking = False
                    current = next_player

            threading.Thread(target=worker, daemon=True).start()

        overlay_play_rect = None
        overlay_quit_rect = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if message != '':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        if overlay_play_rect and overlay_play_rect.collidepoint(mx, my):
                            # Play Again: break to outer loop to show menu again
                            running = False
                            break
                        if overlay_quit_rect and overlay_quit_rect.collidepoint(mx, my):
                            pygame.quit()
                            sys.exit()
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN and message == '':
                    x, y = pygame.mouse.get_pos()
                    col = x // CELL_SIZE
                    if current == 'X' and ai_X is None:
                        if 0 <= col < b.width and b.can_add_to(col):
                            b.add_checker('X', col)
                            if b.is_win_for('X'):
                                message = 'X wins!'
                            elif b.is_full():
                                message = "It's a tie!"
                            else:
                                current = 'O'
                    elif current == 'O' and ai_O is None:
                        if 0 <= col < b.width and b.can_add_to(col):
                            b.add_checker('O', col)
                            if b.is_win_for('O'):
                                message = 'O wins!'
                            elif b.is_full():
                                message = "It's a tie!"
                            else:
                                current = 'X'

            # AI move handling 
            if message == '' and not ai_thinking:
                if current == 'X' and ai_X is not None:
                    start_ai_move(ai_X, 'X', 'O')
                elif current == 'O' and ai_O is not None:
                    start_ai_move(ai_O, 'O', 'X')

            # draw board
            draw_board(screen, b)

            status = ''
            if ai_thinking:
                status = f'AI thinking ({current})...'
            else:
                status = f"{current}'s turn"

            text = font.render(status, True, COLORS['text'])
            screen.blit(text, (10, 10))

            # game end overlay
            if message != '':
                overlay_surf = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                overlay_surf.fill((0, 0, 0, 120))
                screen.blit(overlay_surf, (0, 0))

                # panel
                pw, ph = 420, 180
                px = screen.get_width() // 2 - pw // 2
                py = screen.get_height() // 2 - ph // 2
                panel_rect = pygame.Rect(px, py, pw, ph)
                pygame.draw.rect(screen, (245, 245, 245), panel_rect, border_radius=12)

                big = font.render(message, True, (20, 20, 20))
                screen.blit(big, (px + (pw - big.get_width()) // 2, py + 24))

                overlay_play_rect = pygame.Rect(px + 44, py + ph - 64, 140, 44)
                pygame.draw.rect(screen, (60, 140, 70), overlay_play_rect, border_radius=8)
                ptxt = small_font.render('Play Again', True, (255, 255, 255))
                screen.blit(ptxt, (overlay_play_rect.x + (overlay_play_rect.width - ptxt.get_width()) // 2,
                                    overlay_play_rect.y + (overlay_play_rect.height - ptxt.get_height()) // 2))

                overlay_quit_rect = pygame.Rect(px + pw - 44 - 140, py + ph - 64, 140, 44)
                pygame.draw.rect(screen, (180, 60, 60), overlay_quit_rect, border_radius=8)
                qtxt = small_font.render('Quit', True, (255, 255, 255))
                screen.blit(qtxt, (overlay_quit_rect.x + (overlay_quit_rect.width - qtxt.get_width()) // 2,
                                    overlay_quit_rect.y + (overlay_quit_rect.height - qtxt.get_height()) // 2))

            pygame.display.flip()
            clock.tick(FPS)

        menu_running = True


if __name__ == '__main__':
    main()
