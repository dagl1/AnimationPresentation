"""
animations.py – Composable animation helpers.

Style guide rules encoded here:
  - Prefer Transform() over FadeOut/FadeIn
  - Highlight = yellow glow ONLY (never change object color)
  - Max 3 simultaneous animations per step
  - Slide-out for tables/gene labels
"""
from __future__ import annotations

from manim import (
    Scene, Mobject, VGroup, Animation, AnimationGroup, Succession,
    Transform, FadeIn, FadeOut, Write, GrowArrow, Arrow,
    RIGHT, UP,
)
from utils.styling import HIGHLIGHT_COLOR, GLOW_STROKE_WIDTH, GLOW_OPACITY


# ─── Emphasis ────────────────────────────────────────────────────────────────

def create_glow(obj: Mobject, color: str = HIGHLIGHT_COLOR) -> Mobject:
    """
    Return a glow overlay mobject for `obj`.

    Style guide: ONLY yellow glow – never change the object's own color.
    The caller is responsible for adding/removing this overlay from the scene.

    Example
    -------
        glow = create_glow(arrow)
        scene.play(FadeIn(glow))
        scene.play(FadeOut(glow))
    """
    glow = obj.copy()
    glow.set_stroke(color=color, width=GLOW_STROKE_WIDTH, opacity=GLOW_OPACITY)
    glow.set_fill(opacity=0)
    return glow


def flash_glow(
    scene: Scene,
    obj: Mobject,
    color: str = HIGHLIGHT_COLOR,
    run_time: float = 0.6,
) -> None:
    """Flash a yellow glow on `obj` and remove it. Blocking helper."""
    glow = create_glow(obj, color=color)
    scene.play(FadeIn(glow, run_time=run_time / 2))
    scene.play(FadeOut(glow, run_time=run_time / 2))


# ─── Preferred transitions ───────────────────────────────────────────────────

def morph(src: Mobject, tgt: Mobject, run_time: float = 1.0) -> Transform:
    """
    Preferred morphing transition.
    Always prefer morph() over FadeOut/FadeIn pairs.
    """
    return Transform(src, tgt, run_time=run_time)


def slide_out_right(obj: Mobject, run_time: float = 0.5) -> Animation:
    """
    Slide an object off screen to the right.
    Used for table rows and gene labels exiting.
    """
    target = obj.copy().shift(RIGHT * 15)
    return Transform(obj, target, run_time=run_time)


def slide_in_from_left(obj: Mobject, run_time: float = 0.5) -> Animation:
    """Slide an object in from the left edge of screen."""
    original = obj.get_center().copy()
    obj.shift(RIGHT * -15)
    return obj.animate(run_time=run_time).move_to(original)


# ─── Label / arrow intro ─────────────────────────────────────────────────────

def write_label(label: Mobject, run_time: float = 0.4) -> Write:
    """Animate a label being written (for gene letters, titles, etc.)."""
    return Write(label, run_time=run_time)


def grow_arrow(arrow: Arrow, run_time: float = 0.6) -> GrowArrow:
    """Grow an arrow from its tail to tip."""
    return GrowArrow(arrow, run_time=run_time)


# ─── Batch helpers ───────────────────────────────────────────────────────────

def fade_in_group(group: VGroup, lag_ratio: float = 0.1, run_time: float = 1.0) -> AnimationGroup:
    """Stagger-fade in a VGroup's submobjects."""
    return AnimationGroup(
        *[FadeIn(m) for m in group],
        lag_ratio=lag_ratio,
        run_time=run_time,
    )


def fade_out_group(group: VGroup, lag_ratio: float = 0.05, run_time: float = 0.8) -> AnimationGroup:
    """Stagger-fade out a VGroup's submobjects."""
    return AnimationGroup(
        *[FadeOut(m) for m in group],
        lag_ratio=lag_ratio,
        run_time=run_time,
    )

