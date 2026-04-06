"""
scene_04_debug.py - Debug scene for enzyme-pool allocation behavior.

Goal:
- Validate molecule pool spawning and floating motion.
- Validate AND binding behavior vs OR clustering behavior.
- Validate relative positioning around toy reactions.
"""

from __future__ import annotations

import os
import sys

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Circumscribe,
    FadeIn,
    Rectangle,
    Scene,
    Text,
    VGroup,
    config,
)

# Make src/ importable when manim executes this file directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.molecule_pool import MoleculePool
from components.toy_network import ToyNetwork
from utils.styling import DEBUG, FONT_SIZE_CAPTION

INTERACTIVE_REVIEW = os.getenv("MANIM_INTERACTIVE_REVIEW", "1") == "1"
_SCENE_SPEED = float(os.getenv("MANIM_SPEED", "1.0"))


def _is_opengl_renderer() -> bool:
    renderer = getattr(config, "renderer", "")
    renderer_name = getattr(renderer, "value", renderer)
    return str(renderer_name).strip().lower() == "opengl"


def _hold_for_review(scene: Scene) -> None:
    if not (INTERACTIVE_REVIEW and _is_opengl_renderer()):
        return
    try:
        scene.interactive_embed()
    except ModuleNotFoundError:
        scene.wait(3600)


class Scene04Debug(Scene):
    """Debug storyboard for enzyme pool -> reaction allocation."""

    @staticmethod
    def _rt(base_time: float) -> float:
        return float(base_time) * _SCENE_SPEED

    @staticmethod
    def _pair_centers_near_arrow(
        arrow, side: np.ndarray, pair_count: int, spacing: float
    ) -> list[np.ndarray]:
        center = arrow.get_center() + (side * 0.55)
        if pair_count <= 1:
            return [center]

        perpendicular = np.array([-side[1], side[0], 0.0])
        start_offset = -((pair_count - 1) * spacing) / 2.0
        return [
            center + (perpendicular * (start_offset + (idx * spacing)))
            for idx in range(pair_count)
        ]

    def construct(self) -> None:
        # Step 0: Layout
        horizontal_net = ToyNetwork(
            n_reactions=2,
            layout="horizontal",
            node_arrow_buff=0.15,
            debug=DEBUG,
        )
        vertical_net = ToyNetwork(
            n_reactions=1,
            layout="vertical",
            node_arrow_buff=0.15,
            debug=DEBUG,
        )

        vertical_net.next_to(horizontal_net, DOWN, buff=1.1)
        vertical_net.align_to(horizontal_net, RIGHT)

        network_group = VGroup(horizontal_net, vertical_net)
        network_group.to_edge(RIGHT, buff=0.7)

        # Invisible region that defines where molecules are allowed to spawn.
        pool_region = Rectangle(width=5.0, height=5.4, stroke_opacity=0.0, fill_opacity=0.0)
        pool_region.next_to(network_group, LEFT, buff=0.8)
        pool_region.align_to(network_group, UP)

        pool = MoleculePool(debug=DEBUG)

        self.play(FadeIn(network_group), run_time=self._rt(0.8))

        # Step 1: Spawn molecules
        counts = {"A": 4, "B": 6, "C": 4, "D": 3, "E": 6}
        pool.spawn_enzyme_counts(counts, region=pool_region, seed=11)
        self.play(FadeIn(pool), run_time=self._rt(0.8))

        # Step 2: Define reactions
        r1_label = Text("A AND B", font_size=FONT_SIZE_CAPTION)
        r2_label = Text("C OR D", font_size=FONT_SIZE_CAPTION)
        r3_label = Text("A AND E", font_size=FONT_SIZE_CAPTION)

        arrow_r1 = horizontal_net.get_arrow("R1")
        arrow_r2 = horizontal_net.get_arrow("R2")
        arrow_r3 = vertical_net.get_arrow("R1")

        if arrow_r1 is not None:
            r1_label.next_to(arrow_r1, UP, buff=0.28)
        if arrow_r2 is not None:
            r2_label.next_to(arrow_r2, UP, buff=0.28)
        if arrow_r3 is not None:
            r3_label.next_to(arrow_r3, RIGHT, buff=0.28)

        self.play(FadeIn(VGroup(r1_label, r2_label, r3_label)), run_time=self._rt(0.6))

        # Mild floating drift before allocation.
        self.play(pool.drift_unpaired(amplitude=0.12, seed=21), run_time=self._rt(1.4))

        # Step 3: Reaction 1 (A AND B) -> 2 AB complexes
        a_for_ab = pool.take_unpaired("A", 2)
        b_for_ab = pool.take_unpaired("B", 2)
        ab_centers = self._pair_centers_near_arrow(arrow_r1, UP, pair_count=2, spacing=0.55)

        move_ab = []
        for idx, center in enumerate(ab_centers):
            move_ab.append(a_for_ab[idx].animate.move_to(center + (LEFT * 0.11)))
            move_ab.append(b_for_ab[idx].animate.move_to(center + (RIGHT * 0.11)))

        self.play(AnimationGroup(*move_ab, lag_ratio=0.06), run_time=self._rt(1.4))
        self.play(
            Circumscribe(VGroup(a_for_ab[0], b_for_ab[0]), fade_out=True),
            Circumscribe(VGroup(a_for_ab[1], b_for_ab[1]), fade_out=True),
            run_time=self._rt(0.8),
        )

        # Step 4: Reaction 2 (C OR D) -> cluster above reaction, no binding
        c_for_cluster = pool.take_unpaired("C", 4)
        d_for_cluster = pool.take_unpaired("D", 3)

        cluster_anchor = arrow_r2.get_center() + (UP * 0.95)
        cluster_points = [
            cluster_anchor + np.array([-0.48, 0.15, 0.0]),
            cluster_anchor + np.array([-0.18, 0.26, 0.0]),
            cluster_anchor + np.array([0.12, 0.14, 0.0]),
            cluster_anchor + np.array([0.42, 0.24, 0.0]),
            cluster_anchor + np.array([-0.34, -0.12, 0.0]),
            cluster_anchor + np.array([0.02, -0.18, 0.0]),
            cluster_anchor + np.array([0.34, -0.10, 0.0]),
        ]

        move_cluster = []
        for idx, molecule in enumerate(c_for_cluster):
            move_cluster.append(molecule.animate.move_to(cluster_points[idx]))
        for idx, molecule in enumerate(d_for_cluster):
            move_cluster.append(
                molecule.animate.move_to(cluster_points[idx + len(c_for_cluster)])
            )

        self.play(AnimationGroup(*move_cluster, lag_ratio=0.05), run_time=self._rt(1.5))

        # Step 5: Vertical reaction (A AND E) -> 2 AE complexes
        a_for_ae = pool.take_unpaired("A", 2)
        e_for_ae = pool.take_unpaired("E", 2)
        ae_centers = self._pair_centers_near_arrow(
            arrow_r3, RIGHT, pair_count=2, spacing=0.65
        )

        move_ae = []
        for idx, center in enumerate(ae_centers):
            move_ae.append(a_for_ae[idx].animate.move_to(center + (UP * 0.10)))
            move_ae.append(e_for_ae[idx].animate.move_to(center + (DOWN * 0.10)))

        self.play(AnimationGroup(*move_ae, lag_ratio=0.06), run_time=self._rt(1.4))
        self.play(
            Circumscribe(VGroup(a_for_ae[0], e_for_ae[0]), fade_out=True),
            Circumscribe(VGroup(a_for_ae[1], e_for_ae[1]), fade_out=True),
            run_time=self._rt(0.8),
        )

        # Keep leftovers visible in pool for allocation-debug validation.
        self.play(pool.drift_unpaired(amplitude=0.06, seed=33), run_time=self._rt(1.0))
        _hold_for_review(self)
