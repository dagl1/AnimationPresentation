"""
molecule_pool.py – MoleculePool: a floating collection of labelled gene
or protein copies.

Used to visualise quantities and AND / OR combinatorial logic:
  - AND: letters float in and bind pairwise into complexes
  - OR:  letters accumulate / cluster without binding

Protein shapes (for transform_to_proteins)
------------------------------------------
  Shape A – rectangle with 2 bumps      (PROTEIN_SHAPE_A_COLOR, green)
  Shape B – single larger rectangle     (PROTEIN_SHAPE_B_COLOR, blue)
  Shape C – triangle / wedge            (PROTEIN_SHAPE_C_COLOR, orange)
"""

from __future__ import annotations

from typing import Iterable

import numpy as np
from manim import AnimationGroup, Polygon, Rectangle, RoundedRectangle, Text, VGroup

from components.base import BaseComponent
from utils.styling import (
    DEBUG,
    FONT_SIZE_GENE_LABEL,
    GENE_COLOR,
    PROTEIN_SHAPE_A_COLOR,
    PROTEIN_SHAPE_B_COLOR,
    PROTEIN_SHAPE_C_COLOR,
)


class MoleculePool(BaseComponent):
    """
    Pool of floating molecule (gene / protein) labels.

    Parameters
    ----------
    debug : bool
    """

    def __init__(self, debug: bool = DEBUG, **kwargs) -> None:
        # gene_name → VGroup of individual copies
        self._pool: dict[str, VGroup] = {}
        self._unpaired: dict[str, VGroup] = {}

        super().__init__(debug=debug, **kwargs)
        self._build()
        if debug:
            self._add_debug_overlays()

    # ─── Build ───────────────────────────────────────────────────────────────

    def _build(self) -> None:
        pass  # pool is populated on demand via spawn()

    def _arrange_grid(self, molecules: VGroup, cols: int = 4, spacing: float = 0.55) -> None:
        if len(molecules) == 0:
            return
        for idx, molecule in enumerate(molecules):
            row = idx // cols
            col = idx % cols
            x = (col - (cols - 1) / 2) * spacing
            y = (1 - row) * spacing
            molecule.move_to(np.array([x, y, 0.0]))

    def _arrange_cloud(self, molecules: VGroup, radius: float = 1.2) -> None:
        if len(molecules) == 0:
            return
        for idx, molecule in enumerate(molecules):
            angle = (2 * np.pi * idx) / max(1, len(molecules))
            x = np.cos(angle) * radius * 0.8
            y = np.sin(angle) * radius * 0.55
            molecule.move_to(np.array([x, y, 0.0]))

    def _iter_gene(self, gene: str) -> Iterable:
        return self._pool.get(gene, VGroup()).submobjects

    def _protein_shape_for_gene(self, gene: str):
        center = np.array([0.0, 0.0, 0.0])
        code = gene.upper()[:1]
        if code == "A":
            base = RoundedRectangle(
                width=0.65,
                height=0.35,
                corner_radius=0.08,
                color=PROTEIN_SHAPE_A_COLOR,
                fill_opacity=0.8,
                stroke_opacity=0.9,
            )
            bump_left = Rectangle(
                width=0.14,
                height=0.11,
                color=PROTEIN_SHAPE_A_COLOR,
                fill_opacity=0.8,
                stroke_opacity=0.9,
            ).shift(np.array([-0.18, 0.2, 0.0]))
            bump_right = Rectangle(
                width=0.14,
                height=0.11,
                color=PROTEIN_SHAPE_A_COLOR,
                fill_opacity=0.8,
                stroke_opacity=0.9,
            ).shift(np.array([0.18, 0.2, 0.0]))
            shape = VGroup(base, bump_left, bump_right)
        elif code == "C":
            shape = Polygon(
                np.array([-0.30, -0.22, 0.0]),
                np.array([0.34, 0.00, 0.0]),
                np.array([-0.30, 0.22, 0.0]),
                color=PROTEIN_SHAPE_C_COLOR,
                fill_opacity=0.8,
                stroke_opacity=0.9,
            )
        else:
            shape = Rectangle(
                width=0.72,
                height=0.40,
                color=PROTEIN_SHAPE_B_COLOR,
                fill_opacity=0.8,
                stroke_opacity=0.9,
            )
        shape.move_to(center)
        return shape

    # ─── Public API ──────────────────────────────────────────────────────────

    def spawn(
        self,
        gene: str,
        count: int,
        layout: str = "grid",
    ) -> VGroup:
        """
        Create ``count`` copies of the gene label and arrange them.

        Parameters
        ----------
        gene   : str   Gene name letter(s), e.g. ``'A'``.
        count  : int   Number of copies to create.
        layout : str   ``'grid'`` or ``'random'``.

        Returns
        -------
        VGroup   The newly created copies (also stored in ``self._pool``).
        """
        copies = VGroup()
        for _ in range(max(0, count)):
            copies.add(Text(gene, font_size=FONT_SIZE_GENE_LABEL, color=GENE_COLOR))

        if layout == "random":
            self._arrange_cloud(copies)
        else:
            self._arrange_grid(copies)

        self._pool[gene] = copies
        self._unpaired[gene] = VGroup(*copies)
        self.add(copies)
        return copies

    def bind_pairs(self, gene_a: str, gene_b: str) -> AnimationGroup:
        """
        Animate pairwise binding of gene_a and gene_b molecules (AND logic).

        Excess unbound copies of the larger pool remain visible.

        Returns an AnimationGroup that can be passed to scene.play().
        """
        copies_a = list(self._iter_gene(gene_a))
        copies_b = list(self._iter_gene(gene_b))
        pair_count = min(len(copies_a), len(copies_b))
        if pair_count == 0:
            return AnimationGroup()

        animations = []
        step = 0.95
        start_x = -((pair_count - 1) * step) / 2

        for idx in range(pair_count):
            midpoint = np.array([start_x + (idx * step), -0.25, 0.0])
            left_target = midpoint + np.array([-0.18, 0.0, 0.0])
            right_target = midpoint + np.array([0.18, 0.0, 0.0])
            animations.append(copies_a[idx].animate.move_to(left_target))
            animations.append(copies_b[idx].animate.move_to(right_target))

        self._unpaired[gene_a] = VGroup(*copies_a[pair_count:])
        self._unpaired[gene_b] = VGroup(*copies_b[pair_count:])
        return AnimationGroup(*animations, lag_ratio=0.08)

    def remain_unpaired(self, gene: str) -> VGroup:
        """
        Return the VGroup of molecules that did not find a binding partner
        after a bind_pairs() call.
        """
        return self._unpaired.get(gene, VGroup())

    def accumulate(self, genes: list[str]) -> AnimationGroup:
        """
        Cluster molecules from multiple genes together without binding
        (OR logic – they function independently).
        """
        if not genes:
            return AnimationGroup()

        animations = []
        centers = []
        radius = 1.5
        for idx, _gene in enumerate(genes):
            angle = (2 * np.pi * idx) / len(genes)
            centers.append(np.array([np.cos(angle) * radius, np.sin(angle) * 0.75, 0.0]))

        for idx, gene in enumerate(genes):
            copies = list(self._iter_gene(gene))
            center = centers[idx]
            for jdx, molecule in enumerate(copies):
                local_angle = (2 * np.pi * jdx) / max(1, len(copies))
                offset = np.array(
                    [np.cos(local_angle) * 0.32, np.sin(local_angle) * 0.24, 0.0]
                )
                animations.append(molecule.animate.move_to(center + offset))

        return AnimationGroup(*animations, lag_ratio=0.05)

    def transform_to_proteins(self) -> AnimationGroup:
        """
        Morph gene letter Text objects into protein shape representations.

        Protein shapes are defined in utils/styling.py:
          PROTEIN_SHAPE_A_COLOR, PROTEIN_SHAPE_B_COLOR, PROTEIN_SHAPE_C_COLOR
        """
        from manim import Transform

        transforms = []
        for gene, copies in self._pool.items():
            for molecule in copies:
                target = self._protein_shape_for_gene(gene)
                target.move_to(molecule.get_center())
                transforms.append(Transform(molecule, target))

        return AnimationGroup(*transforms, lag_ratio=0.06)
