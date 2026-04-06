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

import numpy as np
from manim import (
    DOWN,
    LEFT,
    ORANGE,
    ORIGIN,
    PURPLE,
    RIGHT,
    UP,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Line,
    Scene,
    Text,
    Transform,
    VGroup,
    Write,
    config,
    interpolate_color,
)

from components.heart import Heart
from components.metabolic_model import MetabolicModel
from components.person import Person
from components.toy_network import ToyNetwork
from utils.styling import DEBUG, REACTION_COLOR

INTERACTIVE_REVIEW = os.getenv("MANIM_INTERACTIVE_REVIEW", "1") == "1"

# Global playback tuning for this scene.
# MANIM_SPEED > 1.0 slows down all timed plays, < 1.0 speeds up.
_SCENE_SPEED = min(1, float(os.getenv("MANIM_SPEED", "1.0")))
_STEP_END = int(os.getenv("MANIM_STEP_END", "8"))
_BREAKPOINTS = {
    token.strip() for token in os.getenv("MANIM_BREAKPOINTS", "").split(",") if token.strip()
}


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


class Scene01Storyboard(Scene):
    """Storyboard assembly for Scene 1 (intro + iMAT/eFlux + toy-network setup)."""

    @staticmethod
    def _rt(base_time: float) -> float:
        """Apply global speed multiplier to run_time values."""
        return float(base_time) * _SCENE_SPEED

    def _maybe_breakpoint(self, step_id: int) -> None:
        """Optional interactive pause at named step boundaries."""
        if str(step_id) not in _BREAKPOINTS:
            return
        if not (INTERACTIVE_REVIEW and _is_opengl_renderer()):
            return
        self.interactive_embed()

    def _stop_after_if_needed(self, step_id: int) -> bool:
        """Return True when scene should stop after this step."""
        return step_id >= _STEP_END

    @staticmethod
    def _expr_color(value: str):
        """Map expression values to a purple→orange gradient with 20 at midpoint."""
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            return interpolate_color(PURPLE, ORANGE, 0.5)

        if numeric <= 0.0:
            return PURPLE
        if numeric >= 200.0:
            return ORANGE

        # Piecewise mapping: 0 -> 0.0, 20 -> 0.5, 200 -> 1.0
        if numeric <= 20.0:
            t = 0.5 * (numeric / 20.0)
        else:
            t = 0.5 + (0.5 * ((numeric - 20.0) / 180.0))

        return interpolate_color(PURPLE, ORANGE, t)

    def _expr_group_for(self, net: ToyNetwork, values: tuple[str, str]) -> VGroup:
        """Build expression labels for R1/R2, falling back to arrow-based placement."""
        labels_r1 = net.get_gene_labels("R1")
        labels_r2 = net.get_gene_labels("R2")

        # Preferred placement: above gene labels when they exist.
        if labels_r1 is not None and labels_r2 is not None:
            expr_r1 = Text(
                values[0],
                font_size=20,
                color=self._expr_color(values[0]),
            ).next_to(labels_r1[0], UP, buff=0.22)
            expr_r2 = Text(
                values[1],
                font_size=20,
                color=self._expr_color(values[1]),
            ).next_to(labels_r2[0], UP, buff=0.22)
            return VGroup(expr_r1, expr_r2)

        # Step 6/7 fallback: place numeric expressions above reaction arrows.
        arrow_r1 = net.get_arrow("R1")
        arrow_r2 = net.get_arrow("R2")
        if arrow_r1 is None or arrow_r2 is None:
            return VGroup()

        expr_r1 = Text(values[0], font_size=20, color=self._expr_color(values[0])).next_to(
            arrow_r1,
            UP,
            buff=0.22,
        )
        expr_r2 = Text(values[1], font_size=20, color=self._expr_color(values[1])).next_to(
            arrow_r2,
            UP,
            buff=0.22,
        )
        return VGroup(expr_r1, expr_r2)

    def construct(self) -> None:
        # Step 1: person + heart -> extracted heart -> question mark
        person = Person(size=3.0, debug=DEBUG).to_edge(LEFT, buff=1.0)
        heart = Heart(size=0.16, debug=DEBUG)
        chest_center = person.get_heart_position()
        heart.move_to(
            [
                chest_center[0] + (0.18 * person.body.width),
                chest_center[1] + (0.16 * person.body.height),
                0.0,
            ]
        )
        heart.rotate(-0.4)

        self.play(FadeIn(person), run_time=self._rt(0.7))
        self.play(FadeIn(heart), run_time=self._rt(1.6))

        question_mark = Text("Metabolic State?", font_size=30)
        question_mark.next_to(person, RIGHT, buff=1.5)
        self.play(heart.animate.move_to(question_mark.get_center()), run_time=self._rt(1.6))
        self.play(Transform(heart, question_mark), run_time=self._rt(0.6))
        # self.interactive_embed()
        self.wait(2)

        self._maybe_breakpoint(1)
        if self._stop_after_if_needed(1):
            return

        # Step 2: show metabolic model and shift focus left
        model = MetabolicModel(debug=DEBUG)
        model.scale(0.52)
        model.next_to(heart, RIGHT, buff=1.0)
        self.play(FadeIn(model), run_time=self._rt(0.8))

        self.play(person.animate.set_opacity(0.0), run_time=self._rt(0.4))

        left_focus = VGroup(model, heart)
        self.play(left_focus.animate.to_edge(LEFT, buff=0.5), run_time=self._rt(0.8))
        self.wait(2)

        # Step 3: iMAT overlays and pathway fade/recovery
        starting_parenthesis = Text("(", font_size=20)
        imat_text = Text("iMAT", font_size=34)
        high_text = Text("High", font_size=20, color=ORANGE)
        slash_text = Text("/", font_size=20)
        low_text = Text("Low", font_size=20, color=PURPLE)
        thresholds_text = Text(" thresholds)", font_size=20)
        threshold_group = VGroup(
            starting_parenthesis, high_text, slash_text, low_text, thresholds_text
        ).arrange(RIGHT, buff=0.1)
        imat_vgroup = VGroup(imat_text, threshold_group).arrange(DOWN, buff=0.15)
        imat_vgroup.next_to(model, RIGHT, buff=0.4).shift(UP * 0.2).shift(RIGHT * 0.4)
        imat_ref = Text("(Shlomi et al. 2008)", font_size=20)
        imat_ref.to_edge(DOWN, buff=0.7).to_edge(LEFT, buff=0.8)

        self.play(FadeIn(imat_vgroup), FadeIn(imat_ref), run_time=self._rt(0.6))

        high_rxns = ["T7_O2", "T6_O3", "T4_T5", "T5_T6", "G3_G4", "O1_O2", "O3_O4", "A1_T5"]
        low_rxns = ["G1_G2", "G2_G3", "G4_G5", "T3_T4", "O2_O3"]
        self.play(
            model.highlight_reactions(high=high_rxns, low=low_rxns), run_time=self._rt(2.9)
        )
        self.wait(2)
        self.play(
            model.fade_pathways(
                [MetabolicModel.PATHWAY_GLYCOLYSIS, "upper_tca"],
                opacity=0.10,
            ),
            run_time=self._rt(1.2),
        )
        self.wait(3)
        self.play(
            model.fade_pathways(
                [MetabolicModel.PATHWAY_GLYCOLYSIS, "upper_tca"],
                opacity=1.0,
            ),
            run_time=self._rt(0.8),
        )

        # Reset colors and hide regulation arrows in one fast animation
        self.play(
            model.reset_reaction_colors(high_rxns + low_rxns),
            model.regulation_arrows.animate.set_opacity(0.0),
            run_time=self._rt(0.3),
        )
        # Step 4: eFlux overlays
        eflux_text = Text("eFlux", font_size=34)
        prefix = Text("Relative expression (", font_size=20)
        gradient_part = Text("log2 fold change", font_size=20)
        gradient_part.set_color_by_gradient(ORANGE, PURPLE)
        suffix = Text(")", font_size=20)
        relative_expression_text = VGroup(prefix, gradient_part, suffix).arrange(
            RIGHT, buff=0.03
        )
        eflux_group = VGroup(eflux_text, relative_expression_text).arrange(DOWN, buff=0.15)
        eflux_group.next_to(imat_text, DOWN, buff=0.8)
        eflux_ref = Text("(Colijn et al. 2009)", font_size=20)
        eflux_ref.next_to(imat_ref, DOWN, buff=0.15).align_to(imat_ref, LEFT)

        self.play(FadeIn(eflux_group), FadeIn(eflux_ref), run_time=self._rt(0.6))

        all_reactions = sorted(model.reaction_by_id.keys())
        reaction_values = {
            rid: (-2.0 + (4.0 * idx / max(1, len(all_reactions) - 1)))
            for idx, rid in enumerate(all_reactions)
        }
        self.play(
            model.color_reactions_by_value(reaction_values, value_min=-2.0, value_max=2.0),
            run_time=self._rt(2.7),
        )

        # Step 5: move model + labels to the right side and remove refs
        self.play(
            model.animate.to_edge(RIGHT, buff=0.5).scale(0.95).shift(DOWN * 0.1),
            FadeOut(imat_vgroup),
            FadeOut(eflux_group),
            FadeOut(imat_ref),
            FadeOut(eflux_ref),
            FadeOut(heart),
            run_time=self._rt(0.9),
        )

        # Step 6: two toy networks with expression and flux contrast
        top_net = ToyNetwork(
            n_reactions=2,
            layout="horizontal",
            debug=DEBUG,
        )
        bottom_net = ToyNetwork(
            n_reactions=2,
            layout="horizontal",
            debug=DEBUG,
        )

        top_net.scale(0.9)
        bottom_net.scale(0.9)
        top_net.to_edge(LEFT, buff=0.8).to_edge(UP, buff=1.2).shift(DOWN * 0.5)
        bottom_net.next_to(top_net, DOWN, buff=1.0).align_to(top_net, LEFT)

        self.play(FadeIn(top_net), run_time=self._rt(0.6))
        self.play(FadeIn(bottom_net), run_time=self._rt(0.6))

        top_expr = self._expr_group_for(top_net, ("20", "20"))
        bottom_expr = self._expr_group_for(bottom_net, ("200", "200"))
        self.play(FadeIn(top_expr), run_time=self._rt(2.6))
        self.play(FadeIn(bottom_expr), run_time=self._rt(2.6))

        self.play(
            top_net.animate_flux_thickness({"R1": 0.25, "R2": 0.25}, run_time=self._rt(1.5)),
        )
        self.wait(1)
        self.play(
            bottom_net.animate_flux_thickness(
                {"R1": 0.85, "R2": 0.85}, run_time=self._rt(1.5)
            ),
        )

        center_question = Text("?", font_size=70)
        center_question.next_to(VGroup(top_net, bottom_net), RIGHT, buff=0.9)
        top_arrow = Arrow(
            start=center_question.get_left() + LEFT * 0.1,
            end=top_net.get_right() + RIGHT * 0.1,
            buff=0.0,
        )
        bottom_arrow = Arrow(
            start=center_question.get_left() + LEFT * 0.1,
            end=bottom_net.get_right() + RIGHT * 0.1,
            buff=0.0,
        )
        arrows_group = VGroup(top_arrow, bottom_arrow)

        self.play(
            Create(top_arrow),
            Create(bottom_arrow),
            FadeIn(center_question),
            run_time=self._rt(2.7),
        )
        self.wait(3)

        # Step 7: modify bottom network by transform (no object recreation for network)
        target_expr = self._expr_group_for(bottom_net, ("20", "0"))
        self.play(Transform(bottom_expr, target_expr), run_time=self._rt(1.3))
        self.play(
            bottom_net.animate_flux_thickness(
                {"R1": 0.35, "R2": 0.02}, run_time=self._rt(1.5)
            )
        )

        reaction2 = bottom_net.get_arrow("R2")
        if reaction2 is not None:
            start = reaction2.get_start()
            end = reaction2.get_end()
            direction = end - start
            length = float(np.linalg.norm(direction))
            if length <= 1e-8:
                direction = RIGHT
                length = 1.0
            unit = direction / length
            perpendicular = np.array([-unit[1], unit[0], 0.0])

            # Build an actual small X from two perpendicular diagonals.
            center = reaction2.get_center()
            arm = max(0.06, min(0.14, length * 0.12))
            diag1 = unit + perpendicular
            diag2 = unit - perpendicular
            diag1 /= float(np.linalg.norm(diag1))
            diag2 /= float(np.linalg.norm(diag2))

            x1 = Line(
                center - (diag1 * arm),
                center + (diag1 * arm),
                color="#FF3333",
                stroke_width=4,
            )
            x2 = Line(
                center - (diag2 * arm),
                center + (diag2 * arm),
                color="#FF3333",
                stroke_width=4,
            )
            red_x = VGroup(x1, x2)
            self.play(Create(red_x), run_time=self._rt(1.5))

        # Step 8: final GPR focus text
        gpr_text = Text("Gene-Protein-Reaction (GPR) rules", font_size=32)
        # shift both networks down slightly to make room for the text above without overlap
        networks_expression_vgroup = VGroup(
            top_net,
            bottom_net,
            top_expr,
            bottom_expr,
            red_x if reaction2 is not None else VGroup(),
            arrows_group,
        )
        networks_expression_vgroup.shift(DOWN * 0.3)
        gpr_text.next_to(top_net, UP, buff=1.2).shift(RIGHT * 0.2)
        self.play(
            networks_expression_vgroup.animate.shift(DOWN * 0.3),
            run_time=self._rt(1.5),
        )
        self.play(Write(gpr_text), run_time=self._rt(1.5))
        _hold_for_review(self)
