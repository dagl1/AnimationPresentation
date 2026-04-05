"""
equation_block.py – EquationBlock: centre-stage LaTeX equation with
highlight and annotation support.

Style
-----
  Centre-stage, large readable font.
  Emphasis = yellow glow on term (never change equation color).
"""
from __future__ import annotations

from manim import VGroup, VMobject, Animation, AnimationGroup, MathTex, Text

from components.base import BaseComponent
from utils.styling import DEBUG, HIGHLIGHT_COLOR, FONT_SIZE_EQUATION


class EquationBlock(BaseComponent):
    """
    Centre-stage LaTeX equation block.

    Parameters
    ----------
    latex : str
        LaTeX source.  Leave empty to construct the block first and call
        render_latex() later.
    font_size : int
    debug : bool

    Example
    -------
        eq = EquationBlock(r"\\min_{a_i} \\sum_i (1 - a_i / m_i)^2")
        self.add(eq)
        self.play(eq.highlight_term(0))
    """

    def __init__(
        self,
        latex:     str  = "",
        font_size: int  = FONT_SIZE_EQUATION,
        debug:     bool = DEBUG,
        **kwargs,
    ) -> None:
        self.latex     = latex
        self.font_size = font_size
        self.equation: MathTex | None = None

        super().__init__(debug=debug, **kwargs)
        self._build()
        if debug:
            self._add_debug_overlays()

    # ─── Build ───────────────────────────────────────────────────────────────

    def _build(self) -> None:
        if self.latex:
            self.equation = MathTex(self.latex, font_size=self.font_size)
            self.add(self.equation)

    # ─── Public API ──────────────────────────────────────────────────────────

    def render_latex(self, latex: str) -> None:
        """
        Replace the current equation with a new LaTeX string.

        Notes
        -----
        This is a *structural* replacement (removes old, adds new).
        For animated morphing between equations use the scene's
        ``self.play(morph(eq.equation, new_eq))`` instead.
        """
        if self.equation is not None:
            self.remove(self.equation)
        self.latex    = latex
        self.equation = MathTex(latex, font_size=self.font_size)
        self.add(self.equation)

    def highlight_term(
        self,
        term_index: int,
        color: str = HIGHLIGHT_COLOR,
    ) -> Animation:
        """
        Yellow-glow a submobject of the equation by index.

        Style guide: ONLY yellow glow – the equation's own color is unchanged.

        Parameters
        ----------
        term_index : int
            Index into ``self.equation`` submobjects.
        """
        raise NotImplementedError

    def annotate(
        self,
        term_index: int,
        text: str,
        direction=None,
    ) -> VGroup:
        """
        Place a text annotation next to the specified term.

        Returns the VGroup(brace_or_arrow, Text) so the caller can animate it.
        """
        raise NotImplementedError

    def focus_on(self, term_index: int) -> AnimationGroup:
        """
        Dim all other terms, emphasise the target term with a yellow glow.
        """
        raise NotImplementedError

