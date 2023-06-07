# import time
import curses
import curses.ascii
from curses import wrapper
from random import choices
from typing import Any

Window = Any

# def timed_test(duration: int = 30) -> None:
#     pass

def get_colors() -> tuple:
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    return curses.color_pair(1), curses.color_pair(2)

def centered_window(win_height: int = 13, win_width: int = 80) -> Window:
    begin_y = (curses.LINES - 1) // 2 - win_height // 2
    begin_x = (curses.COLS - 1) // 2 - win_width // 2
    window = curses.newwin(win_height, win_width, begin_y, begin_x)
    window.box()
    return window

def centered_text(window: Window, text: str) -> tuple:
    win_height, win_width = window.getmaxyx()
    cursor_y = win_height // 2
    cursor_x = win_width // 2 - len(text) // 2
    window.addstr(cursor_y, cursor_x, text)
    window.refresh()
    return cursor_y, cursor_x

def show_menu() -> None:
    win = centered_window()
    win.box()
    menu_text = 'Press any key to start...'
    text_y, text_x = centered_text(win, menu_text)
    win.addstr(text_y, text_x, menu_text)
    win.getch()

def get_text_sample(length: int = 10) -> str:
    with open('words.txt', 'r') as words:
        wordlist = words.readlines()
        sample_words = [word.strip() for word in choices(wordlist, k=length)]
    return ' '.join(sample_words)

def start_test(stdscr) -> None:
    global errors
    errors = 0
    window = centered_window()
    stdscr.refresh()
    GREEN, RED = get_colors()
    text_sample = get_text_sample()
    cursor_y, cursor_x = centered_text(window, text_sample)
    window.move(cursor_y, cursor_x)
    for i, char in enumerate(text_sample):
        cursor = window.getyx()
        key = window.getkey()
        match ord(key):
        # Throws error if the key falls out of ASCII range
            # BACKSPACE
            case 127 | 8:
                try:
                    prev_char = text_sample[i - 1]
                    window.move(cursor_y, cursor[1] - 1)
                    window.addch(prev_char)
                except IndexError:
                    window.move(cursor_y, cursor_x)
            # SPACE
            case 32:
                if char == ' ':
                    window.move(cursor_y, cursor_x + 1)
                else:
                    errors += 1
                    window.addstr(char, RED | curses.A_UNDERLINE)
            case _:
                # Alphanumeric and puncuation
                if curses.ascii.isalnum(key) or curses.ascii.ispunct(key):
                    if key == char:
                        window.addstr(key, GREEN)
                    else:
                        errors += 1
                        window.addstr(key, RED)
        window.refresh()
    stdscr.clear()

def show_results(stdscr):
    stdscr.addstr(1, 0, f'Errors: {errors}')
    stdscr.refresh()
    stdscr.getkey()


def main(stdscr) -> None:
    curses.use_default_colors()
    # curses.curs_set(0)
    stdscr.clear()
    show_menu()
    start_test(stdscr)
    show_results(stdscr)

if __name__ == '__main__':
    wrapper(main)

# TODO:
#   - [X] Center the text
#   - [X] Write characters on the same line
#   - [X] Make inputs overwite with color
#   - [X] Handle only needed keys
#   - [X] Track cursor position
#   - [X] Handle space character (should print if correct character, but underline in red if incorrect)
#   - [X] Find text samples
#   - [X] Track errors
#   - [ ] Track time and calulate WPM
#   - [X] Fix -x cursor
#   - [ ] Handle arrow keys bug (ord() fails on multicharacter string)
#   - [ ] Create text window and implement word wrap
#   - [ ] Improve str_loc workaround

# Future Improvements
#   - Use text_sample from quotable.io as samples
#   - Accept args for time duration
#   - Menu/UI enhancement
#       - Make surrent word stay center with a scrolling pad
#       - Option selection in menu
