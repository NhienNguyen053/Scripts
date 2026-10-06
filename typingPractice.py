import curses
import time
import random


def load_words(filename="words.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().split()


WORDS = load_words()


def generate_text(word_count = 20):
    return " ".join(random.choice(WORDS) for _ in range(word_count))


def typing_test(stdscr):
    curses.curs_set(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    TEXT = generate_text()

    start_time = None
    typed = []

    correct_total = 0
    total_inputs = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Display target text (wrapped manually)
        for i, ch in enumerate(TEXT):
            row = i // width
            col = i % width
            if row >= height - 3:
                break
            try:
                stdscr.addch(row, col, ch)
            except curses.error:
                pass

        # Display typed text
        for i, ch in enumerate(typed):
            row = (len(TEXT) // width) + 1
            col = i
            if col >= width:
                break

            if i < len(TEXT) and ch == TEXT[i]:
                stdscr.addstr(row, col, ch, curses.color_pair(1))
            else:
                stdscr.addstr(row, col, ch, curses.color_pair(2))

        # Stats
        if start_time:
            elapsed = time.time() - start_time
            wpm = int((correct_total / 5) / (elapsed / 60)) if elapsed > 0 else 0
            acc = (correct_total / total_inputs * 100) if total_inputs else 0
            stdscr.addstr(height - 2, 0, f"WPM: {wpm}  Accuracy: {acc:.2f}%")

        # Cursor
        cursor_x = min(len(typed), width - 1)
        stdscr.move((len(TEXT) // width) + 1, cursor_x)

        stdscr.refresh()
        key = stdscr.get_wch()

        if start_time is None and isinstance(key, str):
            start_time = time.time()

        if key == "\x1b":  # ESC
            return False

        elif key in ("\x7f", "\b", "\x08"):  # backspace
            if typed:
                typed.pop()

        elif isinstance(key, str) and len(typed) < len(TEXT):
            typed.append(key)
            total_inputs += 1

            if key == TEXT[len(typed) - 1]:
                correct_total += 1

        if len(typed) == len(TEXT):
            break

    stdscr.addstr(height - 1, 0, "Done! Press 'y' to continue or 'n' to quit.")
    stdscr.refresh()

    while True:
        choice = stdscr.get_wch()
        if choice in ("y", "Y"):
            return True
        elif choice in ("n", "N"):
            return False


def main(stdscr):
    curses.noecho()

    while True:
        if not typing_test(stdscr):
            break


if __name__ == "__main__":
    curses.wrapper(main)
