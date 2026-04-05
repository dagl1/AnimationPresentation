"""
scene_01_biological_context.py – Scene 1: Biological context introduction.

Shows person with heart to introduce metabolic modeling.
"""

from __future__ import annotations

import os
import sys

# Make src/ importable when manim executes this file directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manim import ORIGIN, LEFT, RIGHT, FadeIn, Scene, config

from components.heart import Heart
from components.person import Person
from utils.styling import DEBUG

INTERACTIVE_REVIEW = os.getenv("MANIM_INTERACTIVE_REVIEW", "1") == "1"


def _is_opengl_renderer() -> bool:
    renderer = getattr(config, "renderer", "")
    renderer_name = getattr(renderer, "value", renderer)
    return str(renderer_name).strip().lower() == "opengl"


def _hold_for_review(scene: Scene) -> None:
    """Keep the OpenGL window open for manual review."""
    if not (INTERACTIVE_REVIEW and _is_opengl_renderer()):
        return

    try:
        scene.interactive_embed()
    except ModuleNotFoundError:
        # interactive_embed requires IPython; keep the window alive as fallback.
        print("[review] IPython not installed; falling back to timed hold.")
        scene.wait(3600)


class BiologicalContextDebug(Scene):
    """Visual test of Person and Heart components."""

    def construct(self) -> None:
        # Create person on the left
        person = Person(size=3.0, debug=DEBUG)
        person.move_to(LEFT * 2.5)

        # Create heart positioned in top-right of person's chest
        heart = Heart(size=0.16, debug=DEBUG)

        # Position heart in top-right of chest (kept fully inside body bounds)
        heart_pos = person.get_heart_position()
        chest_x = heart_pos[0] + (0.18 * person.body.width)
        chest_y = heart_pos[1] + (0.16 * person.body.height)
        heart.move_to([chest_x, chest_y, 0])

        # Rotate the opposite way so orientation matches expectation
        heart.rotate(-0.4)  # ~-23 degrees

        # Add person to scene
        self.play(FadeIn(person))
        self.wait(0.5)

        # Add heart to scene
        self.play(FadeIn(heart))
        self.wait(1.0)

        # Hold for review
        _hold_for_review(self)
