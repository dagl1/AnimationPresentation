"""
layout.py – Relative layout helpers.

All positioning must go through these helpers.
Never use hardcoded shift(LEFT * 3.2) in component or scene code.
"""

from __future__ import annotations

import numpy as np
from manim import DOWN, LEFT, ORIGIN, RIGHT, UP, Mobject, VGroup


def arrange_above(
    label: Mobject,
    target: Mobject,
    buff: float = 0.3,
) -> Mobject:
    """Centre `label` directly above `target`."""
    label.next_to(target, UP, buff=buff)
    label.align_to(target, direction=ORIGIN)  # centre-align horizontally
    return label


def arrange_beside(
    label: Mobject,
    target: Mobject,
    direction: np.ndarray = RIGHT,
    buff: float = 0.3,
) -> Mobject:
    """Place `label` next to `target` in `direction`."""
    label.next_to(target, direction, buff=buff)
    return label


def stack_vertical(
    items: list[Mobject],
    buff: float = 0.4,
    aligned_edge: np.ndarray = LEFT,
) -> VGroup:
    """Arrange `items` top-to-bottom and return as VGroup."""
    g = VGroup(*items)
    g.arrange(DOWN, buff=buff, aligned_edge=aligned_edge)
    return g


def stack_horizontal(
    items: list[Mobject],
    buff: float = 0.4,
    aligned_edge: np.ndarray = DOWN,
) -> VGroup:
    """Arrange `items` left-to-right and return as VGroup."""
    g = VGroup(*items)
    g.arrange(RIGHT, buff=buff, aligned_edge=aligned_edge)
    return g


def align_tops(mobjects: list[Mobject]) -> None:
    """Align all mobjects to the top of the tallest one."""
    top = max(m.get_top()[1] for m in mobjects)
    for m in mobjects:
        m.align_to(np.array([m.get_x(), top, 0]), UP)


def align_lefts(mobjects: list[Mobject]) -> None:
    """Align all mobjects to the leftmost edge."""
    left = min(m.get_left()[0] for m in mobjects)
    for m in mobjects:
        m.align_to(np.array([left, m.get_y(), 0]), LEFT)


def distribute_evenly(
    items: list[Mobject],
    total_width: float,
    direction: np.ndarray = RIGHT,
) -> None:
    """Spread `items` evenly across `total_width` along `direction`."""
    n = len(items)
    if n < 2:
        return
    step = total_width / (n - 1)
    start = items[0].get_center().copy()
    for i, mob in enumerate(items):
        mob.move_to(start + direction * step * i)
