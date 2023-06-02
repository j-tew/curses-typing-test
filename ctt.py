# import time
import curses
import curses.ascii
from curses import wrapper

# def timed_test(duration: int = 30) -> None:
#     pass

def get_colors() -> tuple:
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    return curses.color_pair(1), curses.color_pair(2)

def menu(ui: curses.window) -> None:
    ui.addstr('Press any key to start...\nPress ESC at any time to exit.')
    ui.refresh()
    ui.getkey()

def start_test(ui: curses.window) -> None:
    test_str = 'Horn went "Beep", engine purred. Friendliest sounds you ever heard.'
    # Show target string and move cursor to the beginning
    ui.addstr(test_str)
    ui.move(0, 0)
    # Get and check characters until the cursor reaches the end
    GREEN, RED = get_colors()
    while (cursor_x := ui.getyx()[1]) < len(test_str):
        key = ui.getkey()
        target_char = test_str[cursor_x]
        match ord(key):
            # Exit on ESC
            case 27:
                break
            # Handle BACKSPACE key
            case 127 | 8:
                cursor_y, cursor_x = ui.getyx()
                cursor_x -= 1
                ui.addch(cursor_y, cursor_x, test_str[cursor_x])
                ui.move(cursor_y, cursor_x)
            # Handle SPACE character
            case 32:
                if key == target_char:
                    ui.addstr(key)
                else:
                    ui.addstr(target_char, RED | curses.A_UNDERLINE)
            # All other characters (should only accept alphanumeric and punctuation)
            case _:
                if key == target_char:
                    ui.addstr(key, GREEN)
                else:
                    ui.addstr(key, RED)
        ui.refresh()


def main(ui: curses.window) -> None:

    # Hide cursor
    curses.curs_set(0)

    # Show start screen
    ui.clear()
    menu(ui)

    # Start the test
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
#   - [ ] Handle space character (should print if correct character, but underline in red if incorrect)
#   - [ ] Find text samples
#   - [ ] Track errors
#   - [ ] Track time
#   - [ ] Accept args for time duration
#   - [ ] Improve menu

