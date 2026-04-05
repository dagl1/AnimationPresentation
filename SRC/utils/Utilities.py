from itertools import combinations

from manim import *


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
        print(
            f"Warning: min_width ({min_width}) is smaller than the largest word length ({max_word_length})."
        )
        min_width = max_word_length

    lines = []
    current_line = []
    current_length = 0

    for word in words:
        word_length = len(word)
        if (
            current_length + word_length + len(current_line) > min_width
        ):  # Add len(current_line) for spaces
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
        amount_of_lines=None,
        width_total=None,
        add_question_mark=True,
        with_box=True,
        color=WHITE,
        opacity=1,
        font="Arial",
        should_center=False,
        font_size=20,
        scale=1,
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
            font=font,
            font_size=font_size,
            color=color,
            opacity=opacity,
            should_center=should_center,
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


class ModifiableTable:
    @staticmethod
    def create_table_with_removable_objects(
        data: list[list] or dict,
        removable_keys: list[str],
        fontsize: int = 28,
        x_buff: float = 0.3,
        y_buff: float = 0.5,
        header_row_present: bool = True,
        scale: float = 1,
    ):
        amount_of_columns = len(list(data.values())[0]) + 1
        amount_of_rows = len(data)
        max_x = 0
        max_y = 0
        shift_dict = {}
        for i in range(amount_of_columns):
            for j in range(amount_of_rows):
                if i == 0:
                    value = list(data.keys())[j]
                else:
                    value = str(list(data.values())[j][i - 1])
                max_x = max(max_x, Text(value, font_size=fontsize).get_width())
                max_y = max(max_y, Text(value, font_size=fontsize).get_height())
        x_size = max_x + x_buff
        y_size = max_y + y_buff
        table = VGroup()
        removeable_objects = VGroup()
        align = LEFT
        for i in range(amount_of_columns):
            column = VGroup()
            to_remove_counter = 0
            for j in range(amount_of_rows):
                if i == 0:
                    value = list(data.keys())[j]
                else:
                    value = str(list(data.values())[j][i - 1])
                text = Text(value, alignment="center", font_size=fontsize)
                cell_bg = Rectangle(
                    width=x_size,
                    height=y_size,
                    fill_color=WHITE,
                    fill_opacity=0.0,
                    stroke_width=1,
                )
                text.move_to(cell_bg.get_center())
                cell = VGroup(cell_bg, text)
                column.add(cell)
                if list(data.keys())[j] in removable_keys:
                    removeable_objects.add(cell)
                    to_remove_counter += 1
                else:
                    str_i_j = str(i) + str(j)
                    shift_dict[str_i_j] = (cell, i, j, to_remove_counter * y_size)

            column.arrange(DOWN, buff=0, aligned_edge=align)
            table.add(column)
        table.arrange(RIGHT, buff=0)
        table.move_to(ORIGIN)
        table.scale(scale)

        return table, removeable_objects, shift_dict

    @classmethod
    def get_text_to_indicate(cls, text_to_find, reaction_table, text_to_indicate):
        for obj in reaction_table:
            if isinstance(obj, VGroup):
                cls.get_text_to_indicate(text_to_find, obj, text_to_indicate)
            elif isinstance(obj, Text):
                if obj.get_text() in text_to_find:
                    text_to_indicate.append(obj)

        return text_to_indicate
