"""
toy_network.py – ToyNetwork: a minimal, configurable metabolic toy network.

Network anatomy
---------------
  [M0] ──R1──▶ [M1] ──R2──▶ [M2] …
        gene(s)       gene(s)

  - Metabolite nodes  : white circles
  - Reaction arrows   : white arrows, stroke width encodes flux
  - Gene labels       : white letter text above (horizontal) or
                        beside (vertical) each reaction arrow

Layouts
-------
  'horizontal' (default) – nodes arranged left → right
  'vertical'             – nodes arranged top → bottom

Usage example
-------------
    net = ToyNetwork(
        n_reactions=2,
        layout="horizontal",
        gene_mapping={"R1": ["A", "B"], "R2": ["C"]},
    )
    self.add(net)

    # Adjust flux thickness (normalised 0–1)
    net.set_flux_thickness({"R1": 0.8, "R2": 0.2})
"""
from __future__ import annotations

from typing import Optional
import numpy as np

from manim import (
    VGroup, Circle, Arrow, Text,
    RIGHT, DOWN, UP, LEFT,
)

from components.base import BaseComponent
from utils.styling import (
    GENE_COLOR,
    METABOLITE_COLOR,
    REACTION_COLOR,
    FONT_SIZE_GENE_LABEL,
    FONT_SIZE_EXPRESSION,
    STROKE_REACTION_BASE,
    STROKE_REACTION_MAX,
    NODE_RADIUS,
    NODE_STROKE_WIDTH,
    DEBUG,
)

# ─── Internal spacing constants (relative, not absolute scene coords) ─────────
_NODE_BUFF: float = 2.2    # gap between adjacent node centres
_GENE_BUFF: float = 0.35   # gap between arrow and gene labels
_EXPR_BUFF: float = 0.22   # gap between gene label and expression value


class ToyNetwork(BaseComponent):
    """
    Configurable toy metabolic network.

    Parameters
    ----------
    n_reactions : int
        Number of reaction edges (= number of nodes − 1).  Default: 2.
    layout : str
        ``'horizontal'`` (default) or ``'vertical'``.
    gene_mapping : dict, optional
        Initial gene labels.  Format: { reaction_id → [gene_name, …] }
        Reaction IDs accept: ``'R1'``, ``'r1'``, ``1`` (1-based str/int)
        or ``0`` (0-based int).
    node_labels : list[str], optional
        Short labels placed inside each metabolite node circle.
    debug : bool
        Toggle bounding-box / anchor overlay.
    """

    def __init__(
        self,
        n_reactions: int = 2,
        layout: str = "horizontal",
        gene_mapping: Optional[dict] = None,
        node_labels: Optional[list[str]] = None,
        debug: bool = DEBUG,
        **kwargs,
    ) -> None:
        # Store config before _build() is called
        self.n_reactions: int    = n_reactions
        self.n_nodes:     int    = n_reactions + 1
        self.layout:      str    = layout
        self._node_labels: list[str] = node_labels or []

        # Named sub-groups – always accessible for external animation
        self.nodes:  VGroup = VGroup()   # metabolite circles (+ optional label)
        self.arrows: VGroup = VGroup()   # reaction arrows

        # gene_label_groups : "R1" → VGroup of Text objects
        self.gene_label_groups: dict[str, VGroup] = {}
        # expression_value_groups : "R1" → VGroup of value Text objects
        self.expression_value_groups: dict[str, VGroup] = {}

        super().__init__(debug=debug, **kwargs)
        self._build()

        # Attach gene labels supplied at construction time
        if gene_mapping:
            self.add_gene_labels(gene_mapping)

        if debug:
            self._add_debug_overlays()

    # ─── Internal build ──────────────────────────────────────────────────────

    def _build(self) -> None:
        main_dir = RIGHT if self.layout == "horizontal" else DOWN

        # ── Metabolite nodes ──────────────────────────────────────────────
        for i in range(self.n_nodes):
            circle = Circle(
                radius=NODE_RADIUS,
                color=METABOLITE_COLOR,
                fill_opacity=0.0,
                stroke_width=NODE_STROKE_WIDTH,
            )
            if i > 0:
                circle.next_to(self.nodes[-1], main_dir, buff=_NODE_BUFF)

            if i < len(self._node_labels):
                lbl = Text(
                    self._node_labels[i],
                    font_size=14,
                    color=METABOLITE_COLOR,
                ).move_to(circle.get_center())
                self.nodes.add(VGroup(circle, lbl))
            else:
                self.nodes.add(circle)

        # ── Reaction arrows ───────────────────────────────────────────────
        for i in range(self.n_reactions):
            src = self.nodes[i]
            dst = self.nodes[i + 1]

            # Arrow tail / tip at the circle edges
            if self.layout == "horizontal":
                tail = src.get_right()
                tip  = dst.get_left()
            else:
                tail = src.get_bottom()
                tip  = dst.get_top()

            arrow = Arrow(
                start=tail,
                end=tip,
                buff=0.08,
                stroke_width=STROKE_REACTION_BASE,
                color=REACTION_COLOR,
                tip_length=0.20,
                max_stroke_width_to_length_ratio=10,
            )
            self.arrows.add(arrow)

        self.add(self.nodes, self.arrows)

    # ─── Public API ──────────────────────────────────────────────────────────

    def add_gene_labels(self, mapping: dict) -> None:
        """
        Place gene letter labels above (horizontal) or beside (vertical)
        each reaction arrow.

        Parameters
        ----------
        mapping : dict
            { reaction_id → list[str] }
            e.g.  ``{"R1": ["A", "B"], "R2": ["C"]}``

            Reaction IDs are flexible:
              - ``"R1"`` / ``"r1"`` → 1-based (converted to index 0)
              - ``1``               → treated as 1-based int
              - ``0``               → treated as 0-based int

        Notes
        -----
        Calling this method a second time appends additional label groups;
        it does **not** replace existing ones.
        """
        for key, genes in mapping.items():
            idx = self._resolve_idx(key)
            if idx is None or idx >= self.n_reactions:
                continue

            arrow = self.arrows[idx]

            # Build a horizontal row of gene letters
            label_group = VGroup()
            for gene in genes:
                lbl = Text(gene, font_size=FONT_SIZE_GENE_LABEL, color=GENE_COLOR)
                label_group.add(lbl)
            label_group.arrange(RIGHT, buff=0.20)

            # Position relative to the arrow midpoint
            if self.layout == "horizontal":
                label_group.next_to(arrow, UP, buff=_GENE_BUFF)
            else:
                label_group.next_to(arrow, RIGHT, buff=_GENE_BUFF)

            reaction_id = f"R{idx + 1}"
            self.gene_label_groups[reaction_id] = label_group
            self.add(label_group)

    def set_flux_thickness(self, mapping: dict) -> None:
        """
        Adjust stroke width of reaction arrows to visualise flux.

        Style guide: flux is encoded **only** via line thickness.

        Parameters
        ----------
        mapping : dict
            { reaction_id → flux_value }
            ``flux_value`` is normalised to **[0.0, 1.0]** and mapped
            linearly to [STROKE_REACTION_BASE, STROKE_REACTION_MAX].
            Values outside [0, 1] are clamped silently.
        """
        for key, flux in mapping.items():
            idx = self._resolve_idx(key)
            if idx is None or idx >= self.n_reactions:
                continue

            clamped = max(0.0, min(1.0, float(flux)))
            stroke  = STROKE_REACTION_BASE + clamped * (
                STROKE_REACTION_MAX - STROKE_REACTION_BASE
            )
            self.arrows[idx].set_stroke(width=stroke)

    def show_expression(self, values: dict) -> None:
        """
        Display numeric expression values above the corresponding gene labels.

        Parameters
        ----------
        values : dict
            { gene_name (str) → numeric_value }

        Notes
        -----
        Only labels that were previously added via add_gene_labels() will
        have their expression values displayed.  Existing expression labels
        for the same reaction are removed before new ones are added.
        """
        for reaction_id, label_group in self.gene_label_groups.items():
            # Remove old expression labels for this reaction if present
            if reaction_id in self.expression_value_groups:
                old = self.expression_value_groups[reaction_id]
                if old in self.submobjects:
                    self.remove(old)

            expr_group = VGroup()
            for lbl in label_group:
                if not isinstance(lbl, Text):
                    continue
                gene_name: str = getattr(lbl, "original_text", "")
                if gene_name in values:
                    val_lbl = Text(
                        str(values[gene_name]),
                        font_size=FONT_SIZE_EXPRESSION,
                        color=GENE_COLOR,
                    ).next_to(lbl, UP, buff=_EXPR_BUFF)
                    expr_group.add(val_lbl)

            if expr_group.submobjects:
                self.expression_value_groups[reaction_id] = expr_group
                self.add(expr_group)

    # ─── Convenience accessors ────────────────────────────────────────────────

    def get_reaction_midpoint(self, reaction_idx: int) -> np.ndarray:
        """Return the midpoint of the i-th reaction arrow (0-based index)."""
        return self.arrows[reaction_idx].get_center()

    def get_gene_labels(self, reaction_id: str) -> Optional[VGroup]:
        """
        Return the VGroup of gene label Text objects for a given reaction.

        Parameters
        ----------
        reaction_id : str
            Accepts the same formats as :meth:`add_gene_labels`.
        """
        idx = self._resolve_idx(reaction_id)
        if idx is None:
            return None
        key = f"R{idx + 1}"
        return self.gene_label_groups.get(key)

    def get_arrow(self, reaction_id) -> Optional["Arrow"]:
        """Return the Arrow mobject for the given reaction ID."""
        idx = self._resolve_idx(reaction_id)
        if idx is None or idx >= self.n_reactions:
            return None
        return self.arrows[idx]

    def get_node(self, node_idx: int) -> VGroup:
        """Return the VGroup (circle + optional label) for node i (0-based)."""
        return self.nodes[node_idx]

    # ─── Internal helpers ─────────────────────────────────────────────────────

    @staticmethod
    def _resolve_idx(key) -> Optional[int]:
        """
        Convert a reaction key to a **0-based** integer index.

        Accepted formats
        ----------------
        ``int``      0, 1, 2   → used as 0-based index directly
        ``str``      ``"R1"``, ``"r2"``, ``"1"``, ``"2"``
                     → strip leading R/r, parse as 1-based, subtract 1
        """
        if isinstance(key, int):
            return key
        cleaned = str(key).strip().upper().lstrip("R")
        try:
            return int(cleaned) - 1
        except ValueError:
            return None

