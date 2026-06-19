import curses
import time
import random
import json


def load_lyrics(filename="lyrics.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


LYRICS = load_lyrics()


def generate_text():
    chosen = random.choice(LYRICS)
    if isinstance(chosen.get("lyric"), list):
        return "\n".join(chosen["lyric"])
    return ""


def typing_test(stdscr):
    curses.curs_set(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    TEXT = generate_text().replace("\r\n", "\n")

    start_time = None
    typed = []

    correct_total = 0      # never decreases (for WPM)
    total_inputs = 0       # never decreases (for accuracy)
    wrong_total = 0

    while True:
        stdscr.clear()

        height, width = stdscr.getmaxyx()

        # Display lyrics with line breaks
        lines = TEXT.splitlines()
        for i, line in enumerate(lines):
            if i >= height - 3:
                break
            try:
                stdscr.addstr(i, 0, line[: width - 1])
            except curses.error:
                pass

        # Typed line (bottom)
        visible_typed = typed[: width - 1]

        for i, ch in enumerate(visible_typed):
            if i < len(TEXT) and ch == TEXT[i]:
                stdscr.addstr(height - 3, i, ch, curses.color_pair(1))
            else:
                stdscr.addstr(height - 3, i, ch, curses.color_pair(2))

        # Stats
        if start_time:
            elapsed = time.time() - start_time
            wpm = int((correct_total / 5) / (elapsed / 60)) if elapsed > 0 else 0
            acc = (correct_total / total_inputs * 100) if total_inputs else 0

            stdscr.addstr(height - 2, 0, f"WPM: {wpm}  Accuracy: {acc:.2f}%")

        # Cursor
        cursor_x = min(len(visible_typed), width - 1)
        stdscr.move(height - 3, cursor_x)

        stdscr.refresh()

        key = stdscr.get_wch()

        if start_time is None and isinstance(key, str):
            start_time = time.time()

        if key == "\x1b":  # ESC
            return False

        elif key in ("\n", "\r", curses.KEY_ENTER):
            if len(typed) < len(TEXT):
                typed.append("\n")
                total_inputs += 1

                if TEXT[len(typed) - 1] == "\n":
                    correct_total += 1
                else:
                    wrong_total += 1

        elif key in ("\x7f", "\b", "\x08"):  # backspace
            if typed:
                typed.pop()  # DO NOT modify stats

        elif isinstance(key, str) and len(typed) < len(TEXT):
            typed.append(key)
            total_inputs += 1

            if key == TEXT[len(typed) - 1]:
                correct_total += 1
            else:
                wrong_total += 1

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