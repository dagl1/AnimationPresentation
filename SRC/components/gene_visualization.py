"""
gene_visualization.py – Helpers for visualizing genes and gene binding in Scene 2.

Provides:
    - GeneHighlight: wraps gene text with yellow glow
    - GeneBindingAnimation: animates two genes binding into a complex
    - ColoredGeneLabel: gene text with expression direction indicator (up/down arrows)
"""

from __future__ import annotations

from typing import Optional, Union

import numpy as np
from manim import (
    AnimationGroup,
    FadeIn,
    FadeOut,
    Group,
    Text,
    Transform,
    VGroup,
    Circle,
    Line,
    RIGHT,
    LEFT,
    UP,
    DOWN,
    ORIGIN,
)

from components.base import BaseComponent
from utils.styling import (
    DEBUG,
    FONT_SIZE_GENE_LABEL,
    GENE_COLOR,
    HIGHLIGHT_COLOR,
    UP_ARROW_COLOR,
    DOWN_ARROW_COLOR,
    GLOW_STROKE_WIDTH,
    GLOW_OPACITY,
    STROKE_DEFAULT,
)


class GeneHighlight(BaseComponent):
    """
    Visual wrapper: gene text with yellow glow emphasis.

    Used to highlight a single gene when it's being discussed.

    Parameters
    ----------
    gene : str
        Gene name (typically single letter like "A", "B", etc.).
    position : tuple, optional
        (x, y) position in scene.
    debug : bool

    Example
    -------
        highlight = GeneHighlight("A", position=(0, 1))
        self.add(highlight)
        self.play(highlight.animate_glow())
    """

    def __init__(
        self,
        gene: str,
        position: Union[tuple, np.ndarray] = None,
        debug: bool = DEBUG,
        **kwargs,
    ) -> None:
        self.gene = gene
        self.position = position if position is not None else ORIGIN
        self.gene_text: Optional[Text] = None
        self.glow_circle: Optional[Circle] = None

        super().__init__(debug=debug, **kwargs)
        self._build()
        if debug:
            self._add_debug_overlays()

    def _build(self) -> None:
        """Create gene text and glow background."""
        pos3 = self._coerce_point3(self.position)

        # Gene label
        self.gene_text = Text(
            self.gene,
            font_size=FONT_SIZE_GENE_LABEL,
            color=GENE_COLOR,
        )
        self.gene_text.move_to(pos3)
        self.add(self.gene_text)

        # Optional glow circle (initially hidden)
        self.glow_circle = Circle(
            radius=0.4,
            stroke_color=HIGHLIGHT_COLOR,
            stroke_width=GLOW_STROKE_WIDTH,
            stroke_opacity=0,
            fill_opacity=0,
        )
        self.glow_circle.move_to(pos3)
        self.add(self.glow_circle)

    def animate_glow(self, run_time: float = 0.5) -> AnimationGroup:
        """
        Animate the glow appearing around the gene.

        Returns
        -------
        AnimationGroup
            Animation sequence.
        """
        if not self.glow_circle:
            return AnimationGroup()

        return self.glow_circle.animate(run_time=run_time).set_stroke(opacity=GLOW_OPACITY)

    def remove_glow(self, run_time: float = 0.5) -> AnimationGroup:
        """Fade out the glow."""
        if not self.glow_circle:
            return AnimationGroup()

        return self.glow_circle.animate(run_time=run_time).set_stroke(opacity=0)


class GeneBindingAnimation:
    """
    Helper class: animate two gene molecules binding into a complex.

    This is NOT a component; it's a utility that returns animation sequences
    to be played in a scene.

    Usage
    -----
        binder = GeneBindingAnimation()
        anim = binder.create_and_animate_binding(
            gene_a_pos=(-2, 0),
            gene_b_pos=(2, 0),
            bind_pos=(0, 0),
            scene=self,
        )
        self.play(anim)
    """

    @staticmethod
    def create_and_animate_binding(
        gene_a: str,
        gene_b: str,
        gene_a_pos: tuple,
        gene_b_pos: tuple,
        bind_pos: tuple,
        run_time: float = 1.0,
    ) -> AnimationGroup:
        """
        Return animation sequence for binding two genes.

        The actual gene VGroups must be created and added to scene
        externally; this method only creates the animation group.

        Parameters
        ----------
        gene_a, gene_b : str
            Gene names.
        gene_a_pos, gene_b_pos : tuple
            Starting positions.
        bind_pos : tuple
            Position where binding occurs.
        run_time : float
            Duration in seconds.

        Returns
        -------
        AnimationGroup
            Animation(s) to move and bind the genes.
        """
        # Create gene labels
        text_a = Text(gene_a, font_size=FONT_SIZE_GENE_LABEL, color=GENE_COLOR)
        text_a.move_to(gene_a_pos)

        text_b = Text(gene_b, font_size=FONT_SIZE_GENE_LABEL, color=GENE_COLOR)
        text_b.move_to(gene_b_pos)

        # Move both toward binding position, then transform to complex label
        group_a = Group(text_a)
        group_b = Group(text_b)

        animations = []
        # Animate approach
        animations.append(group_a.animate(run_time=run_time * 0.6).move_to(bind_pos))
        animations.append(group_b.animate(run_time=run_time * 0.6).move_to(bind_pos))

        return AnimationGroup(*animations, lag_ratio=0.0)


class ColoredGeneLabel(BaseComponent):
    """
    Gene label with expression direction indicator.

    Shows a gene letter with an arrow indicating expression level:
    - UP arrow (↑) in orange → high expression
    - DOWN arrow (↓) in purple → low expression

    Parameters
    ----------
    gene : str
        Gene name.
    expression_direction : str
        "up" or "down".
    position : tuple, optional
        Scene position.
    debug : bool

    Example
    -------
        label = ColoredGeneLabel("A", "up", position=(0, 1))
        self.add(label)
    """

    def __init__(
        self,
        gene: str,
        expression_direction: str = "up",  # "up" or "down"
        position: Union[tuple, np.ndarray] = None,
        debug: bool = DEBUG,
        **kwargs,
    ) -> None:
        self.gene = gene
        self.direction = expression_direction.lower()
        self.position = position if position is not None else ORIGIN
        self.gene_text: Optional[Text] = None
        self.arrow: Optional[Text] = None

        if self.direction not in ("up", "down"):
            raise ValueError(
                f"expression_direction must be 'up' or 'down', got {self.direction}"
            )

        super().__init__(debug=debug, **kwargs)
        self._build()
        if debug:
            self._add_debug_overlays()

    def _build(self) -> None:
        """Create gene text and expression arrow."""
        # Gene label
        self.gene_text = Text(
            self.gene,
            font_size=FONT_SIZE_GENE_LABEL,
            color=GENE_COLOR,
        )

        # Expression direction arrow
        arrow_char = "↑" if self.direction == "up" else "↓"
        arrow_color = UP_ARROW_COLOR if self.direction == "up" else DOWN_ARROW_COLOR

        self.arrow = Text(
            arrow_char,
            font_size=FONT_SIZE_GENE_LABEL - 4,
            color=arrow_color,
        )

        # Arrange: gene on left, arrow on right
        group = VGroup(self.gene_text, self.arrow)
        group.arrange(RIGHT, buff=0.2)
        group.move_to(self._coerce_point3(self.position))

        self.add(group)
