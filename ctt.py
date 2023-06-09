# import time
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

def main(stdscr) -> None:
    stdscr.clear()
    # Colors
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    GREEN = curses.color_pair(1)
    RED = curses.color_pair(2)
    # Hide cursor
    # curses.curs_set(0)
    errors = 0
    window = centered_window()
    menu_text = 'Press any key to start...'
    line, begin, end = centered_text(window, menu_text)
    window.getch()
    text_sample = get_text_sample()
    line, begin, end = centered_text(window, text_sample)
    window.move(line, begin)
    while begin <= (column := window.getyx()[1]) < end:
        key = window.getkey()
        target_char = text_sample[column - begin]
        match ord(key):
        # Throws error if the key falls out of ASCII range
            # BACKSPACE
            case 127 | 8:
                try:
                    prev_char = text_sample[column - 1]
                    one_back = (line, column - 1)
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
                # Alphanumeric and puncuation
                if curses.ascii.isalnum(key) or curses.ascii.ispunct(key):
                    if key == target_char:
                        window.addstr(key, GREEN)
                    else:
                        errors += 1
                        window.addstr(key, RED)
        window.refresh()
    window.clear()
    window.addstr(1, 0, f'Errors: {errors}')
    window.refresh()
    window.getkey()

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
