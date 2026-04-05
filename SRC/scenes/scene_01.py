"""
scene_01.py – ToyNetwork development scaffold.

This is a debug/verification scene, not production content.
It exercises ToyNetwork visually so the system can be validated
before real scenes are authored.

Run via:
    python src/start.py
"""

from __future__ import annotations

import os
import sys

# Make src/ importable when manim executes this file directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manim import ORIGIN, DOWN, RIGHT, FadeIn, GrowArrow, Scene, Write, config

from components.metabolic_model import MetabolicModel
from components.toy_network import ToyNetwork
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


class ToyNetworkDebug(Scene):
    """
    Visual test of ToyNetwork – horizontal layout, gene labels, flux thickness.
    Not a production scene.
    """

    def construct(self) -> None:
        # ── Build network ─────────────────────────────────────────────────
        net = ToyNetwork(
            n_reactions=2,
            layout="horizontal",
            gene_mapping={"R1": ["A", "B"], "R2": ["C"]},
            debug=DEBUG,
        )
        net.move_to(ORIGIN)

        # ── Introduce nodes and arrows ────────────────────────────────────
        self.play(FadeIn(net.nodes))
        self.play(*[GrowArrow(a) for a in net.arrows])

        # ── Write gene labels ─────────────────────────────────────────────
        for rg in net.gene_label_groups.values():
            self.play(Write(rg))

        self.wait(0.5)

        # ── Demonstrate flux thickness ────────────────────────────────────
        self.play(net.animate_flux_thickness({"R1": 1.0, "R2": 0.15}, run_time=0.8))
        self.wait(0.6)

        self.play(net.animate_flux_thickness({"R1": 0.15, "R2": 1.0}, run_time=0.8))
        self.wait(0.6)

        # ── Reset flux ────────────────────────────────────────────────────
        self.play(net.animate_flux_thickness({"R1": 0.5, "R2": 0.5}, run_time=0.8))
        self.wait(0.6)

        # Keep OpenGL window interactive for manual review until user exits.
        _hold_for_review(self)


class MetabolicModelDebug(Scene):
    """Visual test of MetabolicModel structure and core pathway APIs."""

    def construct(self) -> None:
        model = MetabolicModel(debug=DEBUG)
        # Scale down to 0.6 of original size
        model.scale(0.6)
        # Start at top-left
        model.move_to([-3.5, 2.0, 0.0])
        self.add(model)

        # Animate movement from top-left to bottom-right
        self.play(model.animate.move_to([3.5, -2.0, 0.0]), run_time=2.0)

        self.wait(0.4)
        self.play(
            model.show_flux("G3_G4", 0.85),
            model.show_flux("T2_T3", 0.95),
            model.show_flux("T7_O2", 0.65),
            run_time=0.9,
        )

        self.play(model.highlight_reactions(high=["T7_O2"], low=["G2_G3"]), run_time=0.8)
        self.wait(0.4)

        self.play(
            model.fade_pathway(MetabolicModel.PATHWAY_GLYCOLYSIS, opacity=0.25), run_time=0.8
        )
        self.wait(0.4)
        self.play(
            model.fade_pathway(MetabolicModel.PATHWAY_GLYCOLYSIS, opacity=1.0), run_time=0.8
        )

        _hold_for_review(self)
