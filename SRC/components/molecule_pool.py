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

from manim import VGroup, Animation, AnimationGroup

from components.base import BaseComponent
from utils.styling import DEBUG, GENE_COLOR, FONT_SIZE_GENE_LABEL


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

        super().__init__(debug=debug, **kwargs)
        self._build()
        if debug:
            self._add_debug_overlays()

    # ─── Build ───────────────────────────────────────────────────────────────

    def _build(self) -> None:
        pass   # pool is populated on demand via spawn()

    # ─── Public API ──────────────────────────────────────────────────────────

    def spawn(
        self,
        gene:   str,
        count:  int,
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
        raise NotImplementedError

    def bind_pairs(self, gene_a: str, gene_b: str) -> AnimationGroup:
        """
        Animate pairwise binding of gene_a and gene_b molecules (AND logic).

        Excess unbound copies of the larger pool remain visible.

        Returns an AnimationGroup that can be passed to scene.play().
        """
        raise NotImplementedError

    def remain_unpaired(self, gene: str) -> VGroup:
        """
        Return the VGroup of molecules that did not find a binding partner
        after a bind_pairs() call.
        """
        raise NotImplementedError

    def accumulate(self, genes: list[str]) -> AnimationGroup:
        """
        Cluster molecules from multiple genes together without binding
        (OR logic – they function independently).
        """
        raise NotImplementedError

    def transform_to_proteins(self) -> AnimationGroup:
        """
        Morph gene letter Text objects into protein shape representations.

        Protein shapes are defined in utils/styling.py:
          PROTEIN_SHAPE_A_COLOR, PROTEIN_SHAPE_B_COLOR, PROTEIN_SHAPE_C_COLOR
        """
        raise NotImplementedError

