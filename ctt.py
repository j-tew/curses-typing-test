# import time
import curses
import curses.ascii
from curses import wrapper
from random import choices

# def timed_test(duration: int = 30) -> None:
#     pass

def get_colors() -> tuple:
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    return curses.color_pair(1), curses.color_pair(2)

def center_text(window, text: str) -> tuple:
    begin_y, begin_x = window.getbegyx()
    win_height, win_width = window.getmaxyx()
    cursor_y = win_height // 2
    cursor_x = win_width // 2 - len(text) // 2
    return cursor_y, cursor_x

def center_win(win_height: int = 13, win_width: int = 80) -> tuple:
    begin_y = (curses.LINES - 1) // 2 - win_height // 2
    begin_x = (curses.COLS - 1) // 2 - win_width // 2
    return win_height, win_width, begin_y, begin_x

def show_menu(stdscr) -> None:
    win = curses.newwin(*center_win())
    win.box()
    stdscr.refresh()
    menu_text = 'Press any key to start...'
    text_y, text_x = center_text(win, menu_text)
    win.addstr(text_y, text_x, menu_text)
    win.refresh()
    stdscr.getch()
    stdscr.clear()

def get_text_sample(length: int = 10) -> str:
    with open('words.txt', 'r') as words:
        wordlist = words.readlines()
        sample_words = [word.strip() for word in choices(wordlist, k=length)]
    return ' '.join(sample_words)

def start_test(stdscr) -> None:
    win = curses.newwin(*center_win())
    win.box()
    text_sample = get_text_sample()
    cursor_y, cursor_x = center_text(win, text_sample)
    home = cursor_x
    end = home + len(text_sample)
    str_loc = [x for x in range(home, end)]
    win.addstr(cursor_y, cursor_x, text_sample)
    stdscr.move(cursor_y, home)
    GREEN, RED = get_colors()
    global errors
    errors = 0
    while (cursor_x := stdscr.getyx()[1]) in str_loc:
        key = stdscr.getkey()
        target_char = text_sample[cursor_x - home]
        match ord(key):
            # ESC
            case 27:
                break
            # BACKSPACE
            case 127 | 8:
                cursor_y, cursor_x = stdscr.getyx()
                cursor_x -= 1 if cursor_x > 0 else 0
                win.addch(cursor_y, cursor_x, text_sample[cursor_x - home])
                win.move(cursor_y, cursor_x)
            # SPACE
            case 32:
                if key == target_char:
                    stdscr.addstr(key)
                else:
                    errors += 1
                    stdscr.addstr(target_char, RED | curses.A_UNDERLINE)
            case _:
                # Alphanumeric and puncuation
                if curses.ascii.isalnum(key) or curses.ascii.ispunct(key):
                    if key == target_char:
                        stdscr.addstr(key, GREEN)
                    else:
                        errors += 1
                        stdscr.addstr(key, RED)
        win.refresh()
    stdscr.clear()

def show_results(stdscr):
    stdscr.addstr(1, 0, f'Errors: {errors}')
    stdscr.refresh()
    stdscr.getkey()


def main(stdscr) -> None:
    curses.use_default_colors()
    # curses.curs_set(0)
    stdscr.clear()
    show_menu(stdscr)
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
