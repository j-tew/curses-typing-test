import time
import curses
import curses.ascii
from curses import wrapper
from random import choices
from typing import Any

CursesWindow = Any

# def timed_test(duration: int = 30) -> None:
#     pass

def get_colors() -> tuple:
    """
    Get the color pairs for green and red text

    Returns
        A tuple containing the color pairs for green and red text
            (GREEN, RED)
    """
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.curs_set(0)
    return curses.color_pair(1), curses.color_pair(2)


def show_menu(stdscr: CursesWindow) -> None:
    """
    Render a simple menu that is centered on the screen and wait for keypress
    """
    menu_text = 'Press any key to start...'
    line, begin = centered(stdscr, menu_text)
    stdscr.clear()
    stdscr.addstr(line, begin, menu_text)
    stdscr.refresh()
    stdscr.getch()


def centered(stdscr: CursesWindow, text: str) -> tuple:
    """
    Get the coordinates needed to center a text string on the screen
    
    Parameters
        stdscr: CursesWindow
            The curses window object
        text: str
            The text to be rendered in the center of the screen
    
    Returns
        A tuple containing the line number and beginning positions of the string
    """
    win_height, win_width = stdscr.getmaxyx()
    line = win_height // 2
    begin = win_width // 2 - len(text) // 2
    return line, begin


def get_text_sample(count: int = 10) -> str:
    """
    Get a number of words from the wordlist to and return a space separated string

    Parameters
        count: int, Optional
            The number of words desired in the string

    Returns
        A space separated string
    """
    with open('words.txt', 'r') as words:
        wordlist = words.readlines()
        sample_words = [word.strip() for word in choices(wordlist, k=count)]
    return ' '.join(sample_words)


def calc_wpm(start_time: int, end_time: int, text_length: int) -> int:
    """
    Calculate the words per minute of the test
    
    Parameters
        start_time: int
            The start time in nanoseconds
        end_time: int
            The end time in nanoseconds
        text_length: int
            The length of the string

    Returns
        The number of words typed per minute during the test
    """
    elapsed = ((end_time - start_time) / 1e9) / 60
    wpm = int((text_length / elapsed) / 5)
    return wpm


def run_test(stdscr: CursesWindow, text: str) -> tuple:
    """
    Run the typing test

    Parameters
        stdscr: CursesWindow
            The curses window object
        text: str
            The text sample to be used for the test
    """
    GREEN, RED = get_colors()
    line, begin = centered(stdscr, text)
    stdscr.clear()
    stdscr.addstr(line, begin, text)
    stdscr.move(line, begin)
    start = time.time_ns()
    errors = 0
    while begin <= (column := stdscr.getyx()[1]) < len(text) + begin:
        key = stdscr.getkey()
        target_char = text[column - begin]
        match ord(key):
            # BACKSPACE
            case 127 | 8:
                try:
                    if column > begin:
                        prev_char = text[column - begin - 1]
                        one_back = (line, column - 1)
                    else:
                        prev_char = text[0]
                        one_back = (line, begin)
                    stdscr.addch(*one_back, prev_char)
                    stdscr.move(*one_back)
                except IndexError:
                    stdscr.move(line, begin)
            # SPACE
            case 32:
                if target_char == ' ':
                    stdscr.move(line, column + 1)
                else:
                    errors += 1
                    stdscr.addstr(key, RED | curses.A_UNDERLINE)
            case _:
                if curses.ascii.isalnum(key) or curses.ascii.ispunct(key):
                    if key == target_char:
                        stdscr.addstr(key, GREEN)
                    else:
                        errors += 1
                        stdscr.addstr(key, RED)
        stdscr.refresh()
    end = time.time_ns()
    wpm = calc_wpm(start, end, len(text))
    return wpm, errors


def show_results(stdscr: CursesWindow, wpm: int, errors: int) -> None:
    """
    Print the results of the test centered on the screen and wait for keypress

    Parameters
        stdscr: CursesWindow
            The curses window object
        wpm: int
            The words per minute from the test
        errors: int
            The count of errors from the test
    """
    stdscr.clear()
    results_message = f'WPM: {wpm} Errors: {errors}'
    line, begin = centered(stdscr, results_message)
    stdscr.addstr(line, begin, results_message)
    stdscr.refresh()
    stdscr.getkey()

def main(stdscr: CursesWindow) -> None:
    curses.use_default_colors()
    show_menu(stdscr)
    text = get_text_sample()
    wpm, errors = run_test(stdscr, text)
    show_results(stdscr, wpm, errors)


if __name__ == '__main__':
    wrapper(main)
