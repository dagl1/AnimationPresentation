"""
heart.py – Stylistic heart shape.

A minimalist heart for biological context visualization.
"""

from __future__ import annotations

import numpy as np
from manim import (
    Bezier,
    ParametricFunction,
    VGroup,
)

from components.base import BaseComponent
from utils.styling import (
    DEBUG,
    METABOLITE_COLOR,
    NODE_STROKE_WIDTH,
)


class Heart(BaseComponent):
    """
    Stylistic heart shape using parametric curves.

    Draws a smooth heart shape using Bezier curves.
    """

    def __init__(
        self,
        height: float = 1.0,
        debug: bool = DEBUG,
        **kwargs,
    ) -> None:
        self.height = height
        self.scale_factor = height / 2.0  # Normalize to height 2.0

        super().__init__(debug=debug, **kwargs)
        self._build()
        if debug:
            self._add_debug_overlays()

    # ─── Build ───────────────────────────────────────────────────────────────

    def _build(self) -> None:
        """Build heart shape using parametric function."""
        # Heart parametric function
        # x(t) = 16 sin³(t)
        # y(t) = 13 cos(t) - 5 cos(2t) - 2 cos(3t) - cos(4t)
        # Normalized to fit in a reasonable size

        def heart_curve(t):
            """Parametric heart curve."""
            x = 16 * np.sin(t) ** 3
            y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
            # Normalize to fit height
            return np.array([x / 32 * self.scale_factor, y / 32 * self.scale_factor, 0])

        # Create the heart using parametric function
        heart = ParametricFunction(
            heart_curve,
            t_range=[0, 2 * np.pi, 0.01],
            color=METABOLITE_COLOR,
            stroke_width=NODE_STROKE_WIDTH,
        )

        self.add(heart)

    # ─── Internal helpers ────────────────────────────────────────────────────

    def _add_debug_overlays(self) -> None:
        """Add bounding boxes and labels for debugging."""
        super()._add_debug_overlays()
