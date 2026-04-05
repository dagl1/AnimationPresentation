"""
heart.py – Simple cartoon heart shape.

A smooth classic red cartoon heart, built from a parametric curve.
"""

from __future__ import annotations

import numpy as np
from manim import (
    Polygon,
    VGroup,
)

from utils.styling import (
    DEBUG,
)


class Heart(VGroup):
    """
    Smooth cartoon heart icon.

    Built as a single filled polygon sampled from a heart curve,
    so it reads visually as a proper stylized heart (not blobs + diamond).
    """

    def __init__(
        self,
        size: float = 1.0,
        debug: bool = DEBUG,
        **kwargs,
    ) -> None:
        self.heart_size = size
        self.debug = debug

        super().__init__(**kwargs)
        self._build()

    # ─── Build ───────────────────────────────────────────────────────────────

    def _build(self) -> None:
        """Build a smooth cartoon heart from a parametric curve."""
        s = self.heart_size

        fill_color = "#FF4D6D"
        stroke_color = "#C62828"

        # Classic heart parametric curve.
        # We normalize and scale to keep the component size predictable.
        t_values = np.linspace(0.0, 2.0 * np.pi, 120, endpoint=False)
        points = []
        for t in t_values:
            x = 16.0 * (np.sin(t) ** 3)
            y = (
                13.0 * np.cos(t)
                - 5.0 * np.cos(2.0 * t)
                - 2.0 * np.cos(3.0 * t)
                - np.cos(4.0 * t)
            )
            # Normalize to roughly unit heart and then scale by s
            # (32 and 34 chosen for balanced width/height in scene)
            px = (x / 32.0) * s
            py = (y / 34.0) * s
            points.append(np.array([px, py, 0.0]))

        heart_shape = Polygon(
            *points,
            color=stroke_color,
            fill_color=fill_color,
            fill_opacity=1.0,
            stroke_width=1.8,
        )

        self.add(heart_shape)

    # ─── Public API ──────────────────────────────────────────────────────────

    def get_highlight_region(self) -> "Heart":
        """Return a copy of the heart for highlight/glow effect."""
        copy = Heart(size=self.heart_size, debug=False)
        copy.set_opacity(0.0)
        return copy
