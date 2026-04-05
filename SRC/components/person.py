"""
person.py – Stylistic person silhouette with heart.

A minimalist human figure for biological context visualization.
"""

from __future__ import annotations

from manim import (
    Circle,
    DOWN,
    Ellipse,
    Line,
    Polygon,
    VGroup,
)

from components.base import BaseComponent
from utils.styling import (
    DEBUG,
    METABOLITE_COLOR,
    NODE_STROKE_WIDTH,
)


class Person(BaseComponent):
    """
    Stylistic person silhouette.

    Composed of:
    - Head (circle)
    - Body (ellipse)
    - Arms (lines)
    - Legs (lines)
    """

    def __init__(
        self,
        size: float = 3.0,
        debug: bool = DEBUG,
        **kwargs,
    ) -> None:
        self.person_size = size
        self.scale_factor = size / 3.0  # Normalize to size 3.0

        # Named sub-groups
        self.head: Circle = Circle()
        self.body: Ellipse = Ellipse()
        self.arms: VGroup = VGroup()
        self.legs: VGroup = VGroup()

        super().__init__(debug=debug, **kwargs)
        self._build()
        if debug:
            self._add_debug_overlays()

    # ─── Build ───────────────────────────────────────────────────────────────

    def _build(self) -> None:
        # Head: circle at top
        head_radius = 0.35 * self.scale_factor
        self.head = Circle(
            radius=head_radius,
            color=METABOLITE_COLOR,
            fill_opacity=0.0,
            stroke_width=NODE_STROKE_WIDTH,
        )
        self.head.shift([0, self.person_size * 0.35, 0])

        # Body: vertical ellipse below head
        body_width = 0.45 * self.scale_factor
        body_height = 0.8 * self.scale_factor
        self.body = Ellipse(
            width=body_width,
            height=body_height,
            color=METABOLITE_COLOR,
            fill_opacity=0.0,
            stroke_width=NODE_STROKE_WIDTH,
        )
        self.body.next_to(self.head, DOWN, buff=body_height * 0.1)

        # Arms: two lines extending from shoulders
        shoulder_y = self.body.get_top()[1] - body_height * 0.1
        arm_length = 0.5 * self.scale_factor
        left_arm = Line(
            start=[body_width * 0.3, shoulder_y, 0],
            end=[body_width * 0.3 + arm_length, shoulder_y, 0],
            color=METABOLITE_COLOR,
            stroke_width=NODE_STROKE_WIDTH,
        )
        right_arm = Line(
            start=[-body_width * 0.3, shoulder_y, 0],
            end=[-body_width * 0.3 - arm_length, shoulder_y, 0],
            color=METABOLITE_COLOR,
            stroke_width=NODE_STROKE_WIDTH,
        )
        self.arms.add(left_arm, right_arm)

        # Legs: two lines extending down from bottom of body
        legs_start_y = self.body.get_bottom()[1]
        leg_length = 0.6 * self.scale_factor
        left_leg = Line(
            start=[body_width * 0.15, legs_start_y, 0],
            end=[body_width * 0.15, legs_start_y - leg_length, 0],
            color=METABOLITE_COLOR,
            stroke_width=NODE_STROKE_WIDTH,
        )
        right_leg = Line(
            start=[-body_width * 0.15, legs_start_y, 0],
            end=[-body_width * 0.15, legs_start_y - leg_length, 0],
            color=METABOLITE_COLOR,
            stroke_width=NODE_STROKE_WIDTH,
        )
        self.legs.add(left_leg, right_leg)

        # Add all parts to the group
        self.add(self.head, self.body, self.arms, self.legs)

    # ─── Public API ──────────────────────────────────────────────────────────

    def get_heart_position(self) -> tuple[float, float, float]:
        """
        Return the center position where a heart should be placed
        inside the person's body.
        """
        return self.body.get_center()

    # ─── Internal helpers ────────────────────────────────────────────────────

    def _add_debug_overlays(self) -> None:
        """Add bounding boxes and labels for debugging."""
        super()._add_debug_overlays()
        # Additional debug info if needed
