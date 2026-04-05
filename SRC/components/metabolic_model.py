"""
metabolic_model.py – MetabolicModel: stylised genome-scale metabolic network.

Pathways
--------
  - Glycolysis  : vertical chain (~5 reactions)
  - TCA cycle   : circular loop (centre/right)
  - OxPhos      : left vertical chain (~5 reactions)
  - Co-substrates: small side nodes (less prominent)

Special feature
---------------
  Alternative bottom entry into TCA allows glycolysis to be faded
  independently (used in Scene 1 iMAT demonstration).

Style
-----
  Stylised / illustrative – not a dense biochemistry diagram.
  Generous spacing between pathways.
"""
from __future__ import annotations

from manim import VGroup, Animation, AnimationGroup

from components.base import BaseComponent
from utils.styling import DEBUG, UP_ARROW_COLOR, DOWN_ARROW_COLOR


class MetabolicModel(BaseComponent):
    """
    Stylised metabolic network (glycolysis + TCA + OxPhos).

    Parameters
    ----------
    show_glycolysis : bool
    show_tca : bool
    show_oxphos : bool
    debug : bool
    """

    PATHWAY_GLYCOLYSIS: str = "glycolysis"
    PATHWAY_TCA:        str = "tca"
    PATHWAY_OXPHOS:     str = "oxphos"

    def __init__(
        self,
        show_glycolysis: bool = True,
        show_tca:         bool = True,
        show_oxphos:      bool = True,
        debug:            bool = DEBUG,
        **kwargs,
    ) -> None:
        self.show_glycolysis = show_glycolysis
        self.show_tca        = show_tca
        self.show_oxphos     = show_oxphos

        # Named sub-groups for external animation access
        self.glycolysis_nodes:   VGroup = VGroup()
        self.glycolysis_arrows:  VGroup = VGroup()
        self.tca_nodes:          VGroup = VGroup()
        self.tca_arrows:         VGroup = VGroup()
        self.oxphos_nodes:       VGroup = VGroup()
        self.oxphos_arrows:      VGroup = VGroup()
        self.co_substrate_nodes: VGroup = VGroup()
        self.regulation_arrows:  VGroup = VGroup()

        super().__init__(debug=debug, **kwargs)
        self._build()
        if debug:
            self._add_debug_overlays()

    # ─── Build ───────────────────────────────────────────────────────────────

    def _build(self) -> None:
        # TODO: implement full stylised metabolic network layout
        pass

    # ─── Public API ──────────────────────────────────────────────────────────

    def highlight_reactions(
        self,
        high: list[str] | None = None,
        low: list[str] | None = None,
    ) -> AnimationGroup:
        """
        Highlight reactions by expression direction.

        Parameters
        ----------
        high : list[str]
            Reaction IDs to mark as highly expressed.
            Visual: orange arrow + UP_ARROW_COLOR glow.
        low : list[str]
            Reaction IDs to mark as lowly expressed.
            Visual: purple arrow + DOWN_ARROW_COLOR glow.
        """
        raise NotImplementedError

    def fade_pathway(self, path_id: str, opacity: float = 0.15) -> Animation:
        """
        Reduce opacity of a named pathway.

        Parameters
        ----------
        path_id : str
            One of: ``'glycolysis'``, ``'tca'``, ``'oxphos'``,
            or a custom subset key.
        opacity : float
            Target opacity (default 0.15 = nearly invisible).
        """
        raise NotImplementedError

    def show_flux(self, reaction_id: str, magnitude: float) -> Animation:
        """
        Dynamically adjust stroke width of a reaction arrow.

        Parameters
        ----------
        magnitude : float   Normalised [0, 1].
        """
        raise NotImplementedError

    def show_regulation(self, reaction_id: str, direction: str) -> Animation:
        """
        Place an up/down regulation arrow beside a reaction.

        Parameters
        ----------
        direction : str   ``'up'`` | ``'down'``
        """
        raise NotImplementedError

    def zoom_to_region(self, region_id: str) -> Animation:
        """Scale and recentre the model to focus on a sub-region."""
        raise NotImplementedError

