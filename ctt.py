import time
import curses
import curses.ascii
from curses import wrapper
from random import choices
from typing import Any

Window = Any

# def timed_test(duration: int = 30) -> None:
#     pass

def centered_window(win_height: int = 13, win_width: int = 80) -> Window:
    begin_y = (curses.LINES - 1) // 2 - win_height // 2
    begin_x = (curses.COLS - 1) // 2 - win_width // 2
    window = curses.newwin(win_height, win_width, begin_y, begin_x)
    window.box()
    return window

def centered_text(window: Window, text: str) -> tuple:
    win_height, win_width = window.getmaxyx()
    line = win_height // 2
    end = len(text)
    begin = win_width // 2 - end // 2
    window.addstr(line, begin, text)
    window.refresh()
    return line, begin, end

def get_text_sample(length: int = 10) -> str:
    with open('words.txt', 'r') as words:
        wordlist = words.readlines()
        sample_words = [word.strip() for word in choices(wordlist, k=length)]
    return ' '.join(sample_words)

def calc_wpm(start: int, end: int, text: str):
    elapsed = ((end - start) / 1e9) / 60
    wpm = int((len(text) / elapsed) / 5)
    return wpm

def main(stdscr) -> None:
    stdscr.clear()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    GREEN = curses.color_pair(1)
    RED = curses.color_pair(2)
    curses.curs_set(0)
    errors = 0
    window = centered_window()
    menu_text = 'Press any key to start...'
    line, begin, end = centered_text(window, menu_text)
    window.getch()
    text_sample = get_text_sample()
    line, begin, end = centered_text(window, text_sample)
    window.move(line, begin)
    start = time.time_ns()
    while begin <= (column := window.getyx()[1]) < end + begin:
        key = window.getkey()
        target_char = text_sample[column - begin]
        match ord(key):
            # BACKSPACE (possible as function)
            case 127 | 8:
                try:
                    if column > begin:
                        prev_char = text_sample[column - begin - 1]
                        one_back = (line, column - 1)
                    else:
                        prev_char = text_sample[0]
                        one_back = (line, begin)
                    window.addch(*one_back, prev_char)
                    window.move(*one_back)
                except IndexError:
                    window.move(line, begin)
            # SPACE
            case 32:
                if target_char == ' ':
                    window.move(line, column + 1)
                else:
                    errors += 1
                    window.addstr(key, RED | curses.A_UNDERLINE)
            case _:
                if curses.ascii.isalnum(key) or curses.ascii.ispunct(key):
                    if key == target_char:
                        window.addstr(key, GREEN)
                    else:
                        errors += 1
                        window.addstr(key, RED)
        window.refresh()
    end = time.time_ns()
    wpm = calc_wpm(start, end, text_sample)
    window.clear()

    error_message = f'Errors: {errors}'
    line, begin, end = centered_text(window, error_message)
    next_line = line + 1
    window.addstr(line, begin, error_message)

    wpm_message = f'WPM: {wpm}'
    line, begin, end = centered_text(window, error_message)
    window.addstr(next_line, begin, wpm_message)
    window.refresh()
    window.getkey()

if __name__ == '__main__':
    wrapper(main)

