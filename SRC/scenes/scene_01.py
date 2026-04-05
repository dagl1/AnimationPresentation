"""
scene_01.py – ToyNetwork development scaffold.

This is a debug/verification scene, not production content.
It exercises ToyNetwork visually so the system can be validated
before real scenes are authored.

Run via:
    python src/start.py
"""
from __future__ import annotations
import sys
import os

# Make src/ importable when manim executes this file directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from manim import Scene, ORIGIN, DOWN, RIGHT, Write, GrowArrow, FadeIn

from components.toy_network import ToyNetwork
from utils.styling import DEBUG


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
        net.set_flux_thickness({"R1": 1.0, "R2": 0.15})
        self.wait(1.0)

        net.set_flux_thickness({"R1": 0.15, "R2": 1.0})
        self.wait(1.0)

        # ── Reset flux ────────────────────────────────────────────────────
        net.set_flux_thickness({"R1": 0.5, "R2": 0.5})
        self.wait(1.0)

