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

def menu(ui: curses.window) -> None:
    ui.addstr('Press any key to start...\nPress ESC at any time to exit.')
    ui.refresh()
    ui.getkey()

def get_quote(length: int = 10) -> str:
    with open('words.txt', 'r') as words:
        wordlist = words.readlines()
        sample_words = [word.strip() for word in choices(wordlist, k=length)]
    return ' '.join(sample_words)

def start_test(ui: curses.window) -> None:
    quote = get_quote()
    # Show target string and move cursor to the beginning
    ui.addstr(quote)
    ui.move(0, 0)
    # Get and check characters until the cursor reaches the end
    GREEN, RED = get_colors()
    # Track errors
    errors = 0
    while (cursor_x := ui.getyx()[1]) < len(quote):
        key = ui.getkey()
        target_char = quote[cursor_x]
        match ord(key):
            # Exit on ESC
            case 27:
                break
            # Handle BACKSPACE key
            case 127 | 8:
                cursor_y, cursor_x = ui.getyx()
                cursor_x -= 1 if cursor_x > 0 else 0
                ui.addch(cursor_y, cursor_x, quote[cursor_x])
                ui.move(cursor_y, cursor_x)
            # Handle SPACE character
            case 32:
                if key == target_char:
                    ui.addstr(key)
                else:
                    errors += 1
                    ui.addstr(target_char, RED | curses.A_UNDERLINE)
            case _:
                # Alphanumeric and puncuation characters
                if curses.ascii.isalnum(key) or curses.ascii.ispunct(key):
                    if key == target_char:
                        ui.addstr(key, GREEN)
                    else:
                        errors += 1
                        ui.addstr(key, RED)
        ui.refresh()
    # Show errors after the test
    ui.addstr(1, 0, f'Errors: {errors}')
    ui.refresh()
    ui.getkey()


def main(ui: curses.window) -> None:
    # Fix colors
    curses.use_default_colors()
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
#   - [X] Handle only needed keys
#   - [X] Track cursor position
#   - [X] Handle space character (should print if correct character, but underline in red if incorrect)
#   - [X] Find text samples
#   - [X] Track errors
#   - [ ] Track time and calulate WPM
#   - [ ] Accept args for time duration
#   - [ ] Improve menu
#   - [X] Fix -x cursor
#   - [ ] Handle arrow keys bug
#   - [ ] Handle word wrap

# Future Improvements
#   - Use quotes from quotable.io as samples
#   - UI enhancement
