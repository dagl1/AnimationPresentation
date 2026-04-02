from manimlib import *
from itertools import combinations

def measure_width(line):
    """Function to measure the width of a line."""
    return len(line)  # Replace with an actual width measurement function if needed

def split_text_by_breaks(text, breaks):
    """Split the text into lines based on the indices of breaks."""
    words = text.split()
    lines = []
    start = 0
    for break_index in breaks:
        lines.append(" ".join(words[start:break_index]))
        start = break_index
    lines.append(" ".join(words[start:]))
    return lines

def find_optimal_line_breaks(text, num_lines):
    """Find the line breaks that minimize the total/max width."""
    words = text.split()
    min_width = float("inf")
    best_breaks = None

    for breaks in combinations(range(1, len(words)), num_lines - 1):
        lines = split_text_by_breaks(text, breaks)
        widths = [measure_width(line) for line in lines]
        max_width = max(widths)  # Minimize the maximum width
        if max_width < min_width:
            min_width = max_width
            best_breaks = breaks

    optimal_lines = split_text_by_breaks(text, best_breaks)
    return optimal_lines, min_width


def split_text_by_width(text, min_width):
    """Split text into lines such that no line exceeds min_width."""
    words = text.split()
    max_word_length = max(len(word) for word in words)

    if min_width < max_word_length:
        print(f"Warning: min_width ({min_width}) is smaller than the largest word length ({max_word_length}).")
        min_width = max_word_length

    lines = []
    current_line = []
    current_length = 0

    for word in words:
        word_length = len(word)
        if current_length + word_length + len(current_line) > min_width:  # Add len(current_line) for spaces
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = word_length
        else:
            current_line.append(word)
            current_length += word_length

    # Add the last line
    if current_line:
        lines.append(" ".join(current_line))

    return lines

class Utilities:
    @staticmethod
    def create_text(
            text,
            amount_of_lines = None,
            width_total = None,
            add_question_mark = True,
            with_box = True,
            color = WHITE,
            opacity = 1,
            font = "Arial",
            should_center = False,
            font_size = 20,
            scale = 1
    ):
        if "\n" in text:
            pass
        elif amount_of_lines is not None:
            optimal_lines, min_width = find_optimal_line_breaks(text, amount_of_lines)
            text = "\n".join(optimal_lines)
        elif width_total is not None:
            text = split_text_by_width(text, width_total)

        text_ = Text(
            text,
            font = font,
            font_size = font_size,
            color = color,
            opacity = opacity,
            should_center = should_center
        ).scale(scale)
        if add_question_mark:
            question_mark = Text("?").scale(scale)
            group = VGroup(text_, question_mark).arrange(RIGHT)
        else:
            group = text_
        if with_box:
            box = SurroundingRectangle(group, color=BLUE)
            group = VGroup(group, box)
        return group
