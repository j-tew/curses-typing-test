# import time
import curses
import curses.ascii
from curses import wrapper

# def timed_test(duration: int = 30) -> None:
#     pass

def menu(ui):
    ui.addstr('Welcome to Tymer typing test!\n')
    ui.addstr('Press any key to start...')
    ui.refresh()

def start_test(ui):
    test_str = 'Horn went "Beep", engine purred. Friendliest sounds you ever heard.'
    ui.addstr(test_str)
    ui.move(0, 0)
    while ui.getyx()[1] < len(test_str):
        key = ui.getkey()
        cursor_y, cursor_x = ui.getyx()
        target_char = test_str[cursor_x]
        match ord(key):
            case 27:
                break
            case 127 | 8:
                cursor_x -= 1
                ui.addch(cursor_y, cursor_x, test_str[cursor_x])
                ui.move(cursor_y, cursor_x)
            case _:
                if key == target_char:
                    ui.addstr(key, curses.color_pair(1))
                else:
                    ui.addstr(key, curses.color_pair(2))
        ui.refresh()


def main(ui):
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.curs_set(0)
    ui.clear()
    menu(ui)
    ui.getkey()
    ui.clear()
    start_test(ui)

if __name__ == '__main__':
    wrapper(main)

# TODO:
#   - [ ] Center the text
#   - [X] Write characters on the same line
#   - [X] Make inputs overwite with color
#   - [ ] Handle only needed keys
#   - [X] Track cursor position
#   - [ ] Handle space character (shouldn't print or move cursor unless space is the correct target_char)
#   - [ ] Find text samples

