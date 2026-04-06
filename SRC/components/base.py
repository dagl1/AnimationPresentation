"""
base.py – BaseComponent: root class for all reusable animation components.

Every component must:
  1. Inherit from BaseComponent
  2. Call super().__init__() *before* building (so VGroup is initialised)
  3. Implement _build() to construct its internal sub-objects
  4. Use relative positioning only (next_to / align_to / arrange)
  5. Optionally call _add_debug_overlays() at the end of __init__
"""

from __future__ import annotations

import numpy as np
from manim import DOWN, RIGHT, UP, Circle, Dot, Mobject, SurroundingRectangle, Text, VGroup

from utils.styling import (
    DEBUG,
    DEBUG_ANCHOR_COLOR,
    DEBUG_BOX_COLOR,
    DEBUG_FONT_SIZE,
)


class BaseComponent(VGroup):
    """
    Root VGroup for all reusable Manim components.

    Parameters
    ----------
    debug : bool
        When True, renders bounding boxes, anchor dots, and class-name labels
        over every direct child object.
        Toggle the global default via ``utils.styling.DEBUG``.
    """

    def __init__(self, debug: bool = DEBUG, **kwargs) -> None:
        super().__init__(**kwargs)
        self.debug = debug
        self._debug_overlays: VGroup = VGroup()

    # ─── Abstract interface ──────────────────────────────────────────────────

    def _build(self) -> None:
        """
        Construct all child mobjects and add them with self.add().
        Must be called at the end of each subclass __init__.
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement _build()")

    @staticmethod
    def _coerce_point3(point: object) -> np.ndarray:
        """Convert (x, y) or (x, y, z) style inputs to a 3D numpy point."""
        arr = np.array(point, dtype=float).flatten()
        if arr.size == 2:
            return np.array([arr[0], arr[1], 0.0], dtype=float)
        if arr.size == 3:
            return np.array([arr[0], arr[1], arr[2]], dtype=float)
        raise ValueError(f"Expected 2D/3D point, got shape {arr.shape}")

    # ─── Debug overlay ───────────────────────────────────────────────────────

    def _add_debug_overlays(self) -> None:
        """
        Overlay bounding boxes, anchor dots, and type-name labels on each
        direct child.  Called automatically when ``debug=True``.
        """
        if not self.debug:
            return

        for obj in list(self.submobjects):
            if obj is self._debug_overlays:
                continue

            # Bounding box in RED
            box = SurroundingRectangle(
                obj,
                color=DEBUG_BOX_COLOR,
                buff=0.04,
                stroke_width=1,
            )

            # Anchor dot in GREEN
            dot = Dot(obj.get_center(), color=DEBUG_ANCHOR_COLOR, radius=0.05)

            # Class-name label
            label = Text(
                obj.__class__.__name__,
                font_size=DEBUG_FONT_SIZE,
                color=DEBUG_ANCHOR_COLOR,
            ).next_to(box, UP, buff=0.04)

            self._debug_overlays.add(box, dot, label)

        self.add(self._debug_overlays)

    def get_debug_overlays(self) -> VGroup:
        """Return the VGroup that holds all debug overlay objects."""
        return self._debug_overlays

    # ─── Fluent positioning helpers ─────────────────────────────────────────

    def place_next_to(
        self,
        target: Mobject,
        direction: np.ndarray = RIGHT,
        buff: float = 0.5,
    ) -> "BaseComponent":
        """next_to() wrapper that returns self for chaining."""
        self.next_to(target, direction, buff=buff)
        return self

    def place_aligned(
        self,
        target: Mobject,
        edge: np.ndarray = UP,
    ) -> "BaseComponent":
        """align_to() wrapper that returns self for chaining."""
        self.align_to(target, edge)
        return self

    def place_at_center(self) -> "BaseComponent":
        """Move this component to the scene origin."""
        self.move_to(np.array([0.0, 0.0, 0.0]))
        return self
