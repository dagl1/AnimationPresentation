"""
ifc_system.py – IFCSystem: Isozyme Functional Complex expansion and visualization.

The IFCSystem takes a GPR (Gene-Protein-Reaction) expression and expands it
into all possible functional enzyme complexes (IFCs).

Example
-------
    Input:   (A OR B) AND (C OR D)
    Output:  AC, AD, BC, BD

    ifc = IFCSystem()
    self.add(ifc)
    self.play(ifc.expand_expression("(A OR B) AND (C OR D)"))

The component handles:
    - Expansion of OR/AND boolean expressions
    - Visual duplication and transformation of gene pairs
    - Grouping and labeling of IFCs
    - Combinatorial rendering per scene_2.yml Step 6
"""

from __future__ import annotations

import re
from itertools import product
from typing import Optional, Union

import numpy as np
from manim import (
    AnimationGroup,
    FadeIn,
    LaggedStart,
    SurroundingRectangle,
    Text,
    TransformFromCopy,
    VGroup,
    DOWN,
    RIGHT,
    ORIGIN,
)

from components.base import BaseComponent
from utils.styling import (
    DEBUG,
    FONT_SIZE_EXPRESSION,
    FONT_SIZE_GENE_LABEL,
    GENE_COLOR,
    HIGHLIGHT_COLOR,
    METABOLITE_COLOR,
    STROKE_DEFAULT,
)


class IFCSystem(BaseComponent):
    """
    Expands GPR expressions into functional enzyme complexes (IFCs).

    Parameters
    ----------
    debug : bool
        Enable debug overlays.
    **kwargs
        Passed to BaseComponent.

    Attributes
    ----------
    ifcs : dict[str, VGroup]
        Expanded IFC pairs, keyed by gene combination (e.g., "AC").
    """

    def __init__(self, debug: bool = DEBUG, **kwargs) -> None:
        self._ifcs: dict[str, VGroup] = {}
        self._layout: str = "grid"  # "grid", "linear", "circular"

        super().__init__(debug=debug, **kwargs)
        self._build()
        if debug:
            self._add_debug_overlays()

    def _build(self) -> None:
        """Initialize empty; IFCs created on demand via expand_expression()."""
        pass

    # ─── Expression Parsing & Expansion ───────────────────────────────────────

    def _parse_groups(self, expression: str) -> list[list[str]]:
        """
        Parse a GPR expression into groups of genes connected by OR.

        Example
        -------
            "(A OR B) AND (C OR D)" → [["A", "B"], ["C", "D"]]
            "A AND B" → [["A"], ["B"]]
            "C OR D" → [["C", "D"]]

        Parameters
        ----------
        expression : str
            Boolean GPR expression with parentheses and AND/OR operators.

        Returns
        -------
        list[list[str]]
            Groups of genes (each group connected by OR).
        """
        expr = expression.strip()
        groups: list[list[str]] = []
        matches = re.findall(r"\(([^()]*)\)|([A-Za-z][A-Za-z0-9_]*)", expr)
        for grouped, standalone in matches:
            if grouped:
                genes = [g.strip() for g in re.split(r"\bOR\b", grouped) if g.strip()]
                if genes:
                    groups.append(genes)
                continue

            token = standalone.strip()
            if token and token not in {"AND", "OR"}:
                groups.append([token])

        return groups

    def _expand_to_combinations(self, groups: list[list[str]]) -> list[str]:
        """
        Generate all combinations from groups using Cartesian product.

        Example
        -------
            [["A", "B"], ["C", "D"]] → ["AC", "AD", "BC", "BD"]

        Parameters
        ----------
        groups : list[list[str]]
            Groups of genes (each group connected by OR).

        Returns
        -------
        list[str]
            All possible gene combinations.
        """
        combinations = []
        for combo in product(*groups):
            combinations.append("".join(combo))
        return combinations

    # ─── IFC Creation & Animation ────────────────────────────────────────────

    def create_ifc(self, label: str, position: Union[tuple, np.ndarray] = None) -> VGroup:
        """
        Create a single IFC (enzyme complex) as a grouped object.

        Parameters
        ----------
        label : str
            Gene combination label, e.g., "AC".
        position : Union[tuple, np.ndarray], optional
            Position in scene. Default: origin.

        Returns
        -------
        VGroup
            Grouped IFC containing gene labels.
        """
        ifc_group = VGroup()

        for gene in label:
            gene_text = Text(
                gene,
                font_size=FONT_SIZE_GENE_LABEL,
                color=GENE_COLOR,
            )
            ifc_group.add(gene_text)
        ifc_group.arrange(RIGHT, buff=0.18)

        box = SurroundingRectangle(
            ifc_group,
            color=METABOLITE_COLOR,
            buff=0.10,
            stroke_width=STROKE_DEFAULT,
        )
        ifc_group.add_to_back(box)

        # Center the group
        ifc_group.move_to(ORIGIN)

        # Add subtle outline/box if desired (optional enhancement)
        # For now, just group the genes

        if position is not None:
            ifc_group.move_to(self._coerce_point3(position))

        self._ifcs[label] = ifc_group
        return ifc_group

    def expand_expression(self, expression: str) -> AnimationGroup:
        """
        Parse a GPR expression and animate expansion to IFC pairs.

        This method returns an AnimationGroup that, when played:
        1. Parses the expression into OR groups
        2. Generates all combinations (Cartesian product)
        3. Animates duplication + transform of gene pairs
        4. Groups each pair visually

        Parameters
        ----------
        expression : str
            Boolean GPR expression, e.g., "(A OR B) AND (C OR D)".

        Returns
        -------
        AnimationGroup
            Animation sequence for expanding and displaying IFCs.
        """
        groups = self._parse_groups(expression)
        combinations = self._expand_to_combinations(groups)
        if not groups or not combinations:
            return AnimationGroup()

        self._ifcs.clear()

        source_row = VGroup()
        source_lookup: dict[str, Text] = {}
        y = 1.85
        for group_idx, genes in enumerate(groups):
            group_items = VGroup()
            x_center = (group_idx - (len(groups) - 1) / 2) * 3.4
            for gene_idx, gene in enumerate(genes):
                item = Text(gene, font_size=FONT_SIZE_GENE_LABEL, color=GENE_COLOR)
                x = x_center + (gene_idx - (len(genes) - 1) / 2) * 0.9
                item.move_to(np.array([x, y, 0.0]))
                group_items.add(item)
                source_lookup.setdefault(gene, item)
            source_row.add(group_items)

        expression_text = Text(
            expression, font_size=FONT_SIZE_EXPRESSION, color=HIGHLIGHT_COLOR
        )
        expression_text.move_to(np.array([0.0, 2.6, 0.0]))
        expression_text.set_opacity(0)
        source_row.set_opacity(0)
        self.add(expression_text, source_row)

        positions = self._compute_layout(len(combinations))
        combo_anims = []
        for idx, combo in enumerate(combinations):
            pos = np.array([positions[idx][0], positions[idx][1] - 0.8, 0.0])
            ifc = self.create_ifc(combo, position=pos)

            pair_anims = []
            for char_idx, gene in enumerate(combo):
                source = source_lookup.get(gene)
                if source is None:
                    continue
                target_char = ifc[char_idx + 1] if len(ifc) > 1 else ifc[char_idx]
                pair_anims.append(TransformFromCopy(source, target_char, run_time=0.45))

            pair_anims.append(FadeIn(ifc[0], run_time=0.2))
            combo_anims.append(AnimationGroup(*pair_anims, lag_ratio=0.0))

        expansion = LaggedStart(*combo_anims, lag_ratio=0.16)
        return AnimationGroup(
            FadeIn(expression_text, run_time=0.2),
            FadeIn(source_row, run_time=0.2),
            expansion,
            lag_ratio=0.2,
        )

    # ─── Layout Helpers ─────────────────────────────────────────────────────────

    def _compute_layout(self, n_ifcs: int) -> list[tuple]:
        """
        Compute positions for n IFCs based on layout mode.

        Parameters
        ----------
        n_ifcs : int
            Number of IFCs to layout.

        Returns
        -------
        list[tuple]
            List of (x, y) positions.
        """
        if self._layout == "grid":
            return self._layout_grid(n_ifcs)
        elif self._layout == "linear":
            return self._layout_linear(n_ifcs)
        elif self._layout == "circular":
            return self._layout_circular(n_ifcs)
        else:
            return [(0, 0)] * n_ifcs

    def _layout_grid(self, n_ifcs: int) -> list[tuple]:
        """Arrange IFCs in a grid (2x2, 3x3, etc.)."""
        cols = int(np.ceil(np.sqrt(n_ifcs)))
        positions = []
        for i in range(n_ifcs):
            row = i // cols
            col = i % cols
            x = (col - cols / 2 + 0.5) * 1.5
            y = (2 - row) * 1.0  # top to bottom
            positions.append((x, y))
        return positions

    def _layout_linear(self, n_ifcs: int) -> list[tuple]:
        """Arrange IFCs in a horizontal line."""
        positions = []
        for i in range(n_ifcs):
            x = (i - n_ifcs / 2 + 0.5) * 1.5
            positions.append((x, 0))
        return positions

    def _layout_circular(self, n_ifcs: int) -> list[tuple]:
        """Arrange IFCs in a circle."""
        positions = []
        radius = 2.0
        for i in range(n_ifcs):
            angle = 2 * np.pi * i / n_ifcs
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            positions.append((x, y))
        return positions

    def set_layout(self, layout: str) -> None:
        """Set layout mode: 'grid', 'linear', or 'circular'."""
        if layout in ("grid", "linear", "circular"):
            self._layout = layout

    # ─── Public API ──────────────────────────────────────────────────────────

    def get_ifc(self, label: str) -> Optional[VGroup]:
        """Retrieve an IFC VGroup by its gene combination label."""
        return self._ifcs.get(label)

    def get_all_ifcs(self) -> VGroup:
        """Return all created IFCs as a single VGroup."""
        return VGroup(*self._ifcs.values())

    def highlight_ifc(self, label: str) -> AnimationGroup:
        """
        Create animation to highlight a specific IFC (yellow glow).
        Placeholder for now; can integrate with utils.animations.
        """
        ifc = self.get_ifc(label)
        if not ifc:
            return AnimationGroup()
        # TODO: Apply glow effect via add_glow or similar
        return AnimationGroup()
