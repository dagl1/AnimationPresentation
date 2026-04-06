"""
scene_2.py – Scene 2: Gene-Protein-Reaction (GPR) rules and boolean logic.

This scene explains how genes map to reactions via GPR rules, introduces
AND/OR logic visually, and shows combinatorial expansion (IFCs).

It's structured in 10 distinct steps that can be previewed individually
for debugging and component validation.

Run via:
    python src/start.py

    Or preview individual steps:
    MANIM_STEP_PREVIEW=1 python src/start.py  # Preview step 1 only
    MANIM_STEP_END=3 python src/start.py      # Run steps 1–3
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Make src/ importable when manim executes this file directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import (
    config,
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    MathTex,
    ORIGIN,
    RIGHT,
    Scene,
    Text,
    UP,
    VGroup,
    Write,
)

from components.gene_visualization import (
    ColoredGeneLabel,
    GeneHighlight,
)
from components.ifc_system import IFCSystem
from components.molecule_pool import MoleculePool
from components.toy_network import ToyNetwork
from utils.styling import (
    FONT_SIZE_EXPRESSION,
    FONT_SIZE_TITLE,
    HIGHLIGHT_COLOR,
)


INTERACTIVE_REVIEW = os.getenv("MANIM_INTERACTIVE_REVIEW", "1") == "1"

# Global playback tuning for this scene
_SCENE_SPEED = min(1, float(os.getenv("MANIM_SPEED", "1.0")))
_MIN_POSITIVE_DURATION = 1e-3
_STEP_END = int(os.getenv("MANIM_STEP_END", "10"))
_STEP_PREVIEW = os.getenv("MANIM_STEP_PREVIEW", "").strip()
_BREAKPOINTS = {
    token.strip() for token in os.getenv("MANIM_BREAKPOINTS", "").split(",") if token.strip()
}


def _is_opengl_renderer() -> bool:
    """Check if using OpenGL renderer for interactive features."""
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
        print("[review] IPython not installed; falling back to timed hold.")
        scene.wait(3600)


class Scene2Storyboard(Scene):
    """
    Storyboard assembly for Scene 2: GPR rules and boolean logic.

    The scene is written as one continuous construct() method, with
    comment-separated storyboard sections for easier direct editing.

    Preview/end controls still use the original step numbers:
    1. Title + ToyNetwork setup
    2. Single reaction (Gene A)
    3. AND logic (Genes A and B)
    4. OR logic (Genes C or D)
    5. Complex expression: (A OR B) AND (C OR D)
    6. IFC expansion (combinatorial pairs)
    7. Expression/Activity mapping
    8. 3-step pipeline
    9. GPRimproved system
    10. Final conclusion
    """

    @staticmethod
    def _rt(base_time: float) -> float:
        """Apply global speed multiplier to run_time values."""
        return max(_MIN_POSITIVE_DURATION, float(base_time) * _SCENE_SPEED)

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

    def _ensure_network(self) -> ToyNetwork:
        """Create the reusable toy network when needed."""
        if hasattr(self, "network"):
            return self.network

        self.network = ToyNetwork(
            n_reactions=3,
            layout="horizontal",
            gene_mapping={
                "R1": ["A"],
                "R2": ["A", "B"],
                "R3": ["C", "D"],
            },
        )
        self.network.scale(0.8)
        self.network.move_to(DOWN * 0.5)
        self.add(self.network)
        return self.network

    def _finish_section(self, step_id: int, preview_step: int | None) -> bool:
        """Handle breakpoint/end logic after an inline storyboard section."""
        self._maybe_breakpoint(step_id)
        return preview_step == step_id or self._stop_after_if_needed(step_id)

    def construct(self) -> None:
        """Main scene construction method with inline storyboard sections."""
        preview_step: int | None = None
        if _STEP_PREVIEW:
            try:
                preview_step = int(_STEP_PREVIEW)
            except ValueError:
                print(
                    f"[warn] Invalid MANIM_STEP_PREVIEW={_STEP_PREVIEW}; running full scene."
                )

        # ─── Step 1: Title and Setup ──────────────────────────────────────
        if preview_step in (None, 1):
            title = Text(
                "Gene-Protein-Reaction (GPR) Rules",
                font_size=FONT_SIZE_TITLE,
                color="white",
            )
            title.move_to(UP * 3)

            subtitle = Text(
                "How do genes map to reactions?",
                font_size=FONT_SIZE_EXPRESSION,
                color="white",
            )
            subtitle.move_to(UP * 2)

            network = ToyNetwork(
                n_reactions=3,
                layout="horizontal",
                gene_mapping={
                    "R1": ["A"],
                    "R2": ["A", "B"],
                    "R3": ["C", "D"],
                },
            )
            network.scale(0.8)
            network.move_to(DOWN * 0.5)

            self.play(Write(title, run_time=self._rt(1.0)))
            self.play(Write(subtitle, run_time=self._rt(0.8)))
            self.play(Create(network, run_time=self._rt(1.5)))

            self.network = network
            self.wait(self._rt(1.0))

            if self._finish_section(1, preview_step):
                _hold_for_review(self)
                return

        # ─── Step 2: Single Gene (A) ──────────────────────────────────────
        if preview_step in (None, 2):
            self._ensure_network()

            gene_a = GeneHighlight("A", position=(0, 1.5))
            self.add(gene_a)
            self.play(gene_a.animate_glow(run_time=self._rt(0.6)))

            gpr_text = Text("GPR: A", font_size=FONT_SIZE_EXPRESSION)
            gpr_text.move_to(DOWN * 1.5)
            self.play(Write(gpr_text, run_time=self._rt(0.8)))

            self.wait(self._rt(1.0))

            if self._finish_section(2, preview_step):
                _hold_for_review(self)
                return

        # ─── Step 3: AND Logic ────────────────────────────────────────────
        if preview_step in (None, 3):
            self._ensure_network()

            gene_a = GeneHighlight("A", position=(-1.5, 1.5))
            gene_b = GeneHighlight("B", position=(1.5, 1.5))

            self.add(gene_a, gene_b)
            self.play(
                gene_a.animate_glow(run_time=self._rt(0.5)),
                gene_b.animate_glow(run_time=self._rt(0.5)),
            )

            self.play(
                gene_a.gene_text.animate(run_time=self._rt(0.8)).move_to(
                    DOWN * 0.5 + LEFT * 0.3
                ),
                gene_b.gene_text.animate(run_time=self._rt(0.8)).move_to(
                    DOWN * 0.5 + RIGHT * 0.3
                ),
            )

            gpr_text = Text("GPR: A AND B", font_size=FONT_SIZE_EXPRESSION)
            gpr_text.move_to(DOWN * 2.0)
            self.play(Write(gpr_text, run_time=self._rt(0.8)))

            emphasis = Text(
                "Both genes required",
                font_size=FONT_SIZE_EXPRESSION - 4,
                color=HIGHLIGHT_COLOR,
            )
            emphasis.move_to(DOWN * 2.7)
            self.play(Write(emphasis, run_time=self._rt(0.6)))

            self.wait(self._rt(1.0))

            if self._finish_section(3, preview_step):
                _hold_for_review(self)
                return

        # ─── Step 4: OR Logic ─────────────────────────────────────────────
        if preview_step in (None, 4):
            self._ensure_network()

            gene_c = GeneHighlight("C", position=(-1.5, 1.5))
            gene_d = GeneHighlight("D", position=(1.5, 1.5))

            self.add(gene_c, gene_d)
            self.play(
                gene_c.animate_glow(run_time=self._rt(0.5)),
                gene_d.animate_glow(run_time=self._rt(0.5)),
            )

            gpr_text = Text("GPR: C OR D", font_size=FONT_SIZE_EXPRESSION)
            gpr_text.move_to(DOWN * 2.0)
            self.play(Write(gpr_text, run_time=self._rt(0.8)))

            emphasis = Text(
                "Either gene sufficient",
                font_size=FONT_SIZE_EXPRESSION - 4,
                color=HIGHLIGHT_COLOR,
            )
            emphasis.move_to(DOWN * 2.7)
            self.play(Write(emphasis, run_time=self._rt(0.6)))

            self.wait(self._rt(1.0))

            if self._finish_section(4, preview_step):
                _hold_for_review(self)
                return

        # ─── Step 5: Complex Expression ───────────────────────────────────
        if preview_step in (None, 5):
            self._ensure_network()

            expr_text = MathTex(r"(A \text{ OR } B) \text{ AND } (C \text{ OR } D)")
            expr_text.scale(1.2)
            expr_text.move_to(UP * 2.5)
            self.play(Write(expr_text, run_time=self._rt(1.0)))

            pairs = ["AC", "AD", "BC", "BD"]
            positions = [(-2, 0.5), (0, 0.5), (-2, -0.5), (0, -0.5)]

            pair_texts = []
            for pair, pos in zip(pairs, positions, strict=True):
                pair_text = Text(pair, font_size=FONT_SIZE_EXPRESSION)
                pair_text.move_to((pos[0], pos[1], 0))
                pair_texts.append(pair_text)

            pair_group = VGroup(*pair_texts)
            self.play(Write(pair_group, run_time=self._rt(1.2)))

            self.wait(self._rt(1.0))

            if self._finish_section(5, preview_step):
                _hold_for_review(self)
                return

        # ─── Step 6: IFC Expansion ────────────────────────────────────────
        if preview_step in (None, 6):
            ifc = IFCSystem()
            self.add(ifc)

            expr = "(A OR B) AND (C OR D)"
            expand_anim = ifc.expand_expression(expr)
            self.play(expand_anim, run_time=self._rt(1.5))

            title = Text(
                "All functional enzyme complexes",
                font_size=FONT_SIZE_EXPRESSION,
                color=HIGHLIGHT_COLOR,
            )
            title.move_to(UP * 3)
            self.play(Write(title, run_time=self._rt(0.8)))

            self.wait(self._rt(1.0))

            if self._finish_section(6, preview_step):
                _hold_for_review(self)
                return

        # ─── Step 7: Expression/Activity Mapping ──────────────────────────
        if preview_step in (None, 7):
            high_expr = ColoredGeneLabel("Gene", "up", position=LEFT * 2.5 + UP * 1.5)
            low_expr = ColoredGeneLabel("Gene", "down", position=RIGHT * 2.5 + UP * 1.5)

            self.add(high_expr, low_expr)

            question = Text(
                "Expression → Activity?",
                font_size=FONT_SIZE_EXPRESSION,
                color="white",
            )
            question.move_to(DOWN * 2)
            self.play(Write(question, run_time=self._rt(0.8)))

            explanation = Text(
                "Same assumption as Scene 1: higher expression = higher activity",
                font_size=FONT_SIZE_EXPRESSION - 6,
                color="gray",
            )
            explanation.move_to(DOWN * 3)
            self.play(Write(explanation, run_time=self._rt(1.0)))

            self.wait(self._rt(1.0))

            if self._finish_section(7, preview_step):
                _hold_for_review(self)
                return

        # ─── Step 8: 3-Step Pipeline ─────────────────────────────────────
        if preview_step in (None, 8):
            step1 = Text("1. Protein abundance", font_size=FONT_SIZE_EXPRESSION)
            step2 = Text("2. GPR mapping", font_size=FONT_SIZE_EXPRESSION)
            step3 = Text("3. kcat values", font_size=FONT_SIZE_EXPRESSION)

            pipeline = VGroup(step1, step2, step3)
            pipeline.arrange(DOWN, buff=0.8)
            pipeline.move_to(ORIGIN)

            self.play(Write(step1, run_time=self._rt(0.6)))
            self.wait(self._rt(0.3))
            self.play(Write(step2, run_time=self._rt(0.6)))
            self.wait(self._rt(0.3))
            self.play(Write(step3, run_time=self._rt(0.6)))

            highlight_text = Text(
                "← often missing",
                font_size=FONT_SIZE_EXPRESSION - 4,
                color=HIGHLIGHT_COLOR,
            )
            highlight_text.next_to(step1, RIGHT, buff=0.3)
            self.play(Write(highlight_text, run_time=self._rt(0.6)))

            self.wait(self._rt(1.0))

            if self._finish_section(8, preview_step):
                _hold_for_review(self)
                return

        # ─── Step 9: GPRimproved System ───────────────────────────────────
        if preview_step in (None, 9):
            title = Text(
                "GPRimproved",
                font_size=FONT_SIZE_TITLE,
                color=HIGHLIGHT_COLOR,
            )
            title.move_to(UP * 2.5)
            self.play(Write(title, run_time=self._rt(0.8)))

            step_a = Text("RNA → Protein (translation)", font_size=FONT_SIZE_EXPRESSION - 4)
            step_b = Text("Allocation across IFCs", font_size=FONT_SIZE_EXPRESSION - 4)
            step_c = Text("kcat assignment", font_size=FONT_SIZE_EXPRESSION - 4)

            improvements = VGroup(step_a, step_b, step_c)
            improvements.arrange(DOWN, buff=0.6)
            improvements.move_to(DOWN * 0.5)

            self.play(Write(improvements, run_time=self._rt(1.5)))

            self.wait(self._rt(1.0))

            if self._finish_section(9, preview_step):
                _hold_for_review(self)
                return

        # ─── Step 10: Final Conclusion ────────────────────────────────────
        if preview_step in (None, 10):
            conclusion = Text(
                "Objective-independent enzyme allocation",
                font_size=FONT_SIZE_TITLE,
                color=HIGHLIGHT_COLOR,
            )
            conclusion.move_to(ORIGIN)

            self.play(Write(conclusion, run_time=self._rt(1.2)))
            self.play(conclusion.animate(run_time=self._rt(0.8)).scale(1.2))

            self.wait(self._rt(2.0))
            self.play(FadeOut(conclusion, run_time=self._rt(0.8)))

            transition = Text(
                "→ Scene 3: Implementation",
                font_size=FONT_SIZE_EXPRESSION,
                color="gray",
            )
            transition.move_to(DOWN)
            self.play(Write(transition, run_time=self._rt(0.8)))

            self.wait(self._rt(1.0))

            if self._finish_section(10, preview_step):
                _hold_for_review(self)
                return

        _hold_for_review(self)


class Scene2Debug(Scene):
    """
    Debug/test scene for individual Scene 2 components.

    Use this to rapidly test:
    - MoleculePool spawn / bind / accumulate / protein transform
    - IFCSystem expansion
    - GeneHighlight animations
    - ColoredGeneLabel rendering

    Example usage:
        MANIM_SCENE="Scene2Debug" python src/start.py
    """

    def construct(self) -> None:
        """Demonstrate Scene 2 components in isolation."""
        # Title
        title = Text(
            "Scene 2 Component Debug",
            font_size=FONT_SIZE_TITLE,
        )
        title.move_to(UP * 3)
        self.add(title)

        # Test 1: GeneHighlight
        self.add(Text("Test 1: GeneHighlight", font_size=20).move_to(UP * 2))
        gene_a = GeneHighlight("A", position=(LEFT * 3 + UP * 0.5))
        gene_b = GeneHighlight("B", position=(RIGHT * 3 + UP * 0.5))

        self.add(gene_a, gene_b)
        self.play(
            gene_a.animate_glow(run_time=0.5),
            gene_b.animate_glow(run_time=0.5),
        )
        self.wait(0.5)

        # Test 2: MoleculePool (AND/OR + protein transform)
        self.add(Text("Test 2: MoleculePool", font_size=20).move_to(UP * 0.5))
        pool = MoleculePool()
        pool.scale(0.9)
        pool.move_to(DOWN * 0.15)
        self.add(pool)

        a_copies = pool.spawn("A", count=4, layout="grid")
        b_copies = pool.spawn("B", count=4, layout="grid")
        c_copies = pool.spawn("C", count=3, layout="grid")
        d_copies = pool.spawn("D", count=3, layout="grid")

        a_copies.shift(LEFT * 3 + UP * 0.2)
        b_copies.shift(LEFT * 0.8 + UP * 0.2)
        c_copies.shift(RIGHT * 0.8 + UP * 0.2)
        d_copies.shift(RIGHT * 3 + UP * 0.2)

        self.play(
            FadeIn(a_copies),
            FadeIn(b_copies),
            FadeIn(c_copies),
            FadeIn(d_copies),
            run_time=0.8,
        )
        self.play(pool.bind_pairs("A", "B"), run_time=1.2)
        self.play(pool.accumulate(["C", "D"]), run_time=1.0)
        self.play(pool.transform_to_proteins(), run_time=1.1)
        self.wait(0.6)

        # Test 3: IFCSystem
        self.add(Text("Test 3: IFCSystem", font_size=20).move_to(DOWN * 1.05))
        ifc = IFCSystem()
        ifc.scale(0.95)
        ifc.move_to(DOWN * 0.15)
        self.add(ifc)
        expand_anim = ifc.expand_expression("(A OR B) AND (C OR D)")
        self.play(expand_anim, run_time=1.5)
        self.wait(1.0)

        # Test 4: ColoredGeneLabel
        self.add(Text("Test 4: ColoredGeneLabel", font_size=20).move_to(DOWN * 2))
        label_up = ColoredGeneLabel("A", "up", position=(LEFT * 3 + DOWN * 2.5))
        label_down = ColoredGeneLabel("B", "down", position=(RIGHT * 3 + DOWN * 2.5))
        self.add(label_up, label_down)
        self.wait(1.0)
