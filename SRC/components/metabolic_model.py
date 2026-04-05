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

import numpy as np
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Animation,
    AnimationGroup,
    Arrow,
    Circle,
    ManimColor,
    UpdateFromAlphaFunc,
    VGroup,
    VMobject,
    interpolate_color,
)

from components.base import BaseComponent
from utils.styling import (
    DEBUG,
    DOWN_ARROW_COLOR,
    METABOLITE_COLOR,
    NODE_STROKE_WIDTH,
    REACTION_COLOR,
    STROKE_REACTION_BASE,
    STROKE_REACTION_MAX,
    UP_ARROW_COLOR,
)

_MAIN_NODE_RADIUS: float = 0.15
_CO_SUBSTRATE_RADIUS: float = 0.08
_TCA_RADIUS: float = 2.0
_GLYCOLYSIS_STEP: float = 0.8
_GLYCOLYSIS_TO_TCA_GAP: float = 0.2
_OXPHOS_STEP: float = 1.0
_OXPHOS_TO_TCA_GAP: float = 1.7
_ALT_ENTRY_GAP: float = 1.2
_CO_SUBSTRATE_GAP: float = 0.38
_CO_FLOW_MERGE_OFFSET: float = 0.15  # How far along reaction direction merge happens
_CO_FLOW_ARC: float = 0.80  # Increased arc for smoother parallel approach
_CO_INPUT_OFFSET: float = 0.20  # How far along reaction start the input co-substrate merges
_CO_OUTPUT_OFFSET: float = (
    0.20  # How far back from reaction end the output co-substrate merges
)


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
    PATHWAY_TCA: str = "tca"
    PATHWAY_OXPHOS: str = "oxphos"
    PATHWAY_ALT_ENTRY: str = "alt_entry"
    PATHWAY_CO_SUBSTRATES: str = "co_substrates"

    def __init__(
        self,
        show_glycolysis: bool = True,
        show_tca: bool = True,
        show_oxphos: bool = True,
        debug: bool = DEBUG,
        **kwargs,
    ) -> None:
        self.show_glycolysis = show_glycolysis
        self.show_tca = show_tca
        self.show_oxphos = show_oxphos

        # Named sub-groups for external animation access
        self.glycolysis_nodes: VGroup = VGroup()
        self.glycolysis_arrows: VGroup = VGroup()
        self.tca_nodes: VGroup = VGroup()
        self.tca_arrows: VGroup = VGroup()
        self.oxphos_nodes: VGroup = VGroup()
        self.oxphos_arrows: VGroup = VGroup()
        self.alt_entry_nodes: VGroup = VGroup()
        self.alt_entry_arrows: VGroup = VGroup()
        self.co_substrate_nodes: VGroup = VGroup()
        self.co_substrate_arrows: VGroup = VGroup()
        self.regulation_arrows: VGroup = VGroup()

        self.node_by_id: dict[str, Circle] = {}
        self.reaction_by_id: dict[str, Arrow] = {}
        self.co_substrates_by_reaction: dict[str, VGroup] = {}
        self._base_opacity_by_mobject_id: dict[int, tuple[float, float]] = {}
        self.pathway_groups: dict[str, VGroup] = {}
        self._regulation_by_reaction: dict[str, Arrow] = {}

        super().__init__(debug=debug, **kwargs)
        self._build()
        if debug:
            self._add_debug_overlays()

    # ─── Build ───────────────────────────────────────────────────────────────

    def _build(self) -> None:
        self._build_tca_cycle()
        self._build_glycolysis()
        self._build_alt_entry()
        self._build_oxphos()
        self._build_co_substrates()

        self.add(
            self.tca_arrows,
            self.glycolysis_arrows,
            self.alt_entry_arrows,
            self.oxphos_arrows,
            self.tca_nodes,
            self.glycolysis_nodes,
            self.alt_entry_nodes,
            self.oxphos_nodes,
            self.co_substrate_nodes,
            self.co_substrate_arrows,
            self.regulation_arrows,
        )

        self.pathway_groups = {
            self.PATHWAY_GLYCOLYSIS: self._build_pathway_group(
                self.glycolysis_nodes,
                self.glycolysis_arrows,
                reaction_ids=["G1_G2", "G2_G3", "G3_G4", "G4_G5", "G5_T1"],
            ),
            self.PATHWAY_TCA: self._build_pathway_group(
                self.tca_nodes,
                self.tca_arrows,
                reaction_ids=[
                    "T1_T2",
                    "T2_T3",
                    "T3_T4",
                    "T4_T5",
                    "T5_T6",
                    "T6_T7",
                    "T7_T8",
                    "T8_T1",
                ],
            ),
            self.PATHWAY_OXPHOS: self._build_pathway_group(
                self.oxphos_nodes,
                self.oxphos_arrows,
                reaction_ids=["O1_O2", "O2_O3", "O3_O4", "O4_O5", "T7_O2", "T6_O3"],
            ),
            self.PATHWAY_ALT_ENTRY: self._build_pathway_group(
                self.alt_entry_nodes,
                self.alt_entry_arrows,
                reaction_ids=["A1_T5"],
            ),
            self.PATHWAY_CO_SUBSTRATES: VGroup(
                self.co_substrate_nodes,
                self.co_substrate_arrows,
            ),
            "tca_cycle": self._build_pathway_group(
                self.tca_nodes,
                self.tca_arrows,
                reaction_ids=[
                    "T1_T2",
                    "T2_T3",
                    "T3_T4",
                    "T4_T5",
                    "T5_T6",
                    "T6_T7",
                    "T7_T8",
                    "T8_T1",
                ],
            ),
            "upper_tca": self._build_pathway_group(
                self.node_by_id["T1"],
                self.node_by_id["T2"],
                self.node_by_id["T3"],
                self.node_by_id["T8"],
                self.reaction_by_id["T1_T2"],
                self.reaction_by_id["T2_T3"],
                self.reaction_by_id["T3_T4"],
                self.reaction_by_id["T7_T8"],
                self.reaction_by_id["T8_T1"],
                reaction_ids=["T1_T2", "T2_T3", "T7_T8", "T8_T1"],
            ),
            "lower_tca": self._build_pathway_group(
                self.node_by_id["T4"],
                self.node_by_id["T5"],
                self.node_by_id["T6"],
                self.node_by_id["T7"],
                self.reaction_by_id["T3_T4"],
                self.reaction_by_id["T4_T5"],
                self.reaction_by_id["T5_T6"],
                self.reaction_by_id["T6_T7"],
                self.reaction_by_id["T7_T8"],
                reaction_ids=["T3_T4", "T4_T5", "T5_T6", "T6_T7", "T7_T8"],
            ),
        }

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
        animations = []

        for reaction_id in high or []:
            key = self._reaction_key(reaction_id)
            arrow = self.reaction_by_id.get(key)
            if arrow is None:
                continue
            animations.append(arrow.animate.set_color(UP_ARROW_COLOR))
            animations.append(self.show_regulation(key, direction="up"))

        for reaction_id in low or []:
            key = self._reaction_key(reaction_id)
            arrow = self.reaction_by_id.get(key)
            if arrow is None:
                continue
            animations.append(arrow.animate.set_color(DOWN_ARROW_COLOR))
            animations.append(self.show_regulation(key, direction="down"))

        return AnimationGroup(*animations, lag_ratio=0.0)

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
        key = str(path_id).strip().lower()
        group = self.pathway_groups.get(key)
        if group is None:
            return AnimationGroup()

        clamped = max(0.0, min(1.0, float(opacity)))
        members = self._unique_family_members(group)
        start_opacities = {
            id(mob): (float(mob.get_stroke_opacity()), float(mob.get_fill_opacity()))
            for mob in members
            if isinstance(mob, VMobject)
        }
        target_opacities = {
            id(mob): tuple(value * clamped for value in self._base_opacity_for(mob))
            for mob in members
            if isinstance(mob, VMobject)
        }

        def update_pathway_opacity(updated_group: VGroup, alpha: float) -> VGroup:
            for mob in members:
                if not isinstance(mob, VMobject):
                    continue
                start_stroke, start_fill = start_opacities[id(mob)]
                target_stroke, target_fill = target_opacities[id(mob)]
                current_stroke = start_stroke + ((target_stroke - start_stroke) * alpha)
                current_fill = start_fill + ((target_fill - start_fill) * alpha)
                mob.set_stroke(opacity=current_stroke)
                mob.set_fill(opacity=current_fill)
            return updated_group

        return UpdateFromAlphaFunc(group, update_pathway_opacity)

    def show_flux(self, reaction_id: str, magnitude: float) -> Animation:
        """
        Dynamically adjust stroke width of a reaction arrow.

        Parameters
        ----------
        magnitude : float   Normalised [0, 1].
        """
        key = self._reaction_key(reaction_id)
        arrow = self.reaction_by_id.get(key)
        if arrow is None:
            return AnimationGroup()

        clamped = max(0.0, min(1.0, float(magnitude)))
        stroke = STROKE_REACTION_BASE + clamped * (STROKE_REACTION_MAX - STROKE_REACTION_BASE)
        return arrow.animate.set_stroke(width=stroke)

    def show_regulation(self, reaction_id: str, direction: str) -> Animation:
        """
        Place an up/down regulation arrow beside a reaction.

        Parameters
        ----------
        direction : str   ``'up'`` | ``'down'``
        """
        key = self._reaction_key(reaction_id)
        arrow = self.reaction_by_id.get(key)
        if arrow is None:
            return AnimationGroup()

        marker = self._build_regulation_marker(arrow=arrow, direction=direction)
        existing = self._regulation_by_reaction.get(key)

        if existing is None:
            marker.set_opacity(0.0)
            self.regulation_arrows.add(marker)
            self._regulation_by_reaction[key] = marker
            return marker.animate.set_opacity(1.0)

        return existing.animate.become(marker)

    def zoom_to_region(self, region_id: str) -> Animation:
        """Scale and recentre the model to focus on a sub-region."""
        key = str(region_id).strip().lower()
        group = self.pathway_groups.get(key)
        if group is None:
            return AnimationGroup()

        region_shift = group.get_center() - self.get_center()
        target_center = self.get_center() - (0.35 * region_shift)
        return self.animate.scale(1.15).move_to(target_center)

    def fade_pathways(
        self, path_ids: list[str] | tuple[str, ...], opacity: float = 0.15
    ) -> Animation:
        """Fade multiple pathways/subsets with one stable combined animation."""
        members: list[VMobject] = []
        seen_ids: set[int] = set()

        for path_id in path_ids:
            group = self.pathway_groups.get(str(path_id).strip().lower())
            if group is None:
                continue

            for mob in self._unique_family_members(group):
                mob_id = id(mob)
                if mob_id in seen_ids:
                    continue
                seen_ids.add(mob_id)
                members.append(mob)

        if not members:
            return AnimationGroup()

        return self._fade_members(members, opacity=opacity)

    def _fade_members(self, members: list[VMobject], opacity: float) -> Animation:
        clamped = max(0.0, min(1.0, float(opacity)))
        animation_group = VGroup(*members)

        start_opacities = {
            id(mob): (float(mob.get_stroke_opacity()), float(mob.get_fill_opacity()))
            for mob in members
        }
        target_opacities = {
            id(mob): tuple(value * clamped for value in self._base_opacity_for(mob))
            for mob in members
        }

        def update_pathway_opacity(updated_group: VGroup, alpha: float) -> VGroup:
            for mob in members:
                start_stroke, start_fill = start_opacities[id(mob)]
                target_stroke, target_fill = target_opacities[id(mob)]
                current_stroke = start_stroke + ((target_stroke - start_stroke) * alpha)
                current_fill = start_fill + ((target_fill - start_fill) * alpha)
                mob.set_stroke(opacity=current_stroke)
                mob.set_fill(opacity=current_fill)
            return updated_group

        return UpdateFromAlphaFunc(animation_group, update_pathway_opacity)

    # ─── Internal builders ───────────────────────────────────────────────────

    def _build_tca_cycle(self) -> None:
        prototype = self._make_node(radius=_MAIN_NODE_RADIUS)
        for i in range(8):
            node_id = f"T{i + 1}"
            node = prototype.copy().move_to(UP * _TCA_RADIUS)
            node.rotate(-i * (2.0 * np.pi / 8.0), about_point=ORIGIN)
            self.tca_nodes.add(node)
            self.node_by_id[node_id] = node

        ordered = [f"T{i}" for i in range(1, 9)] + ["T1"]
        for src, dst in zip(ordered[:-1], ordered[1:]):
            self._connect_nodes(src, dst, f"{src}_{dst}", self.tca_arrows)

    def _build_glycolysis(self) -> None:
        chain = VGroup(*[self._make_node(radius=_MAIN_NODE_RADIUS) for _ in range(5)])
        chain.arrange(DOWN, buff=_GLYCOLYSIS_STEP)
        chain.next_to(self.node_by_id["T1"], UP, buff=_GLYCOLYSIS_TO_TCA_GAP)

        for idx, node in enumerate(chain, start=1):
            node_id = f"G{idx}"
            self.glycolysis_nodes.add(node)
            self.node_by_id[node_id] = node

        ordered = [f"G{i}" for i in range(1, 6)]
        for src, dst in zip(ordered[:-1], ordered[1:]):
            self._connect_nodes(src, dst, f"{src}_{dst}", self.glycolysis_arrows)

        self._connect_nodes("G5", "T1", "G5_T1", self.glycolysis_arrows)

    def _build_alt_entry(self) -> None:
        alt = self._make_node(radius=_MAIN_NODE_RADIUS)
        alt.next_to(self.node_by_id["T5"], DOWN, buff=_ALT_ENTRY_GAP)
        self.alt_entry_nodes.add(alt)
        self.node_by_id["A1"] = alt
        self._connect_nodes("A1", "T5", "A1_T5", self.alt_entry_arrows)

    def _build_oxphos(self) -> None:
        chain = VGroup(*[self._make_node(radius=_MAIN_NODE_RADIUS) for _ in range(5)])
        chain.arrange(DOWN, buff=_OXPHOS_STEP)
        chain.next_to(self.tca_nodes, LEFT, buff=_OXPHOS_TO_TCA_GAP)
        chain.align_to(self.node_by_id["T1"], UP)

        for idx, node in enumerate(chain, start=1):
            node_id = f"O{idx}"
            self.oxphos_nodes.add(node)
            self.node_by_id[node_id] = node

        ordered = [f"O{i}" for i in range(1, 6)]
        for src, dst in zip(ordered[:-1], ordered[1:]):
            self._connect_nodes(src, dst, f"{src}_{dst}", self.oxphos_arrows)

        self._connect_nodes("T7", "O2", "T7_O2", self.oxphos_arrows)
        self._connect_nodes("T6", "O3", "T6_O3", self.oxphos_arrows)

    def _build_co_substrates(self) -> None:
        for reaction_id in ("G1_G2", "G2_G3", "G3_G4", "G4_G5"):
            self._add_co_substrate_pair(reaction_id)

        for reaction_id in ("T2_T3", "T4_T5", "T6_T7"):
            self._add_co_substrate_pair(reaction_id)

        for reaction_id in ("O1_O2", "O2_O3", "O3_O4", "O4_O5"):
            self._add_co_substrate_pair(reaction_id)

    # ─── Internal helpers ────────────────────────────────────────────────────

    @staticmethod
    def _reaction_key(reaction_id: str) -> str:
        return str(reaction_id).strip().upper().replace("->", "_")

    @staticmethod
    def _make_node(radius: float) -> Circle:
        return Circle(
            radius=radius,
            color=METABOLITE_COLOR,
            fill_opacity=0.0,
            stroke_width=NODE_STROKE_WIDTH,
        )

    def _connect_nodes(
        self,
        src_node_id: str,
        dst_node_id: str,
        reaction_id: str,
        target_group: VGroup,
    ) -> Arrow:
        src = self.node_by_id[src_node_id]
        dst = self.node_by_id[dst_node_id]

        start = src.get_center()
        end = dst.get_center()
        direction = end - start
        length = float(np.linalg.norm(direction))
        if length == 0:
            unit = np.array([1.0, 0.0, 0.0])
        else:
            unit = direction / length

        arrow = Arrow(
            start=start + (unit * _MAIN_NODE_RADIUS),
            end=end - (unit * _MAIN_NODE_RADIUS),
            buff=0.0,
            stroke_width=STROKE_REACTION_BASE,
            color=REACTION_COLOR,
            tip_length=0.16,
            max_stroke_width_to_length_ratio=10,
        )
        key = self._reaction_key(reaction_id)
        self.reaction_by_id[key] = arrow
        target_group.add(arrow)
        return arrow

    def _build_pathway_group(
        self, *mobjects, reaction_ids: list[str] | None = None
    ) -> VGroup:
        group = VGroup(*mobjects)
        for reaction_id in reaction_ids or []:
            co_group = self.co_substrates_by_reaction.get(self._reaction_key(reaction_id))
            if co_group is not None:
                group.add(co_group)
        return group

    def _unique_family_members(self, group: VGroup) -> list[VMobject]:
        unique_members: list[VMobject] = []
        seen_ids: set[int] = set()
        for mob in group.family_members_with_points():
            mob_id = id(mob)
            if mob_id in seen_ids:
                continue
            seen_ids.add(mob_id)
            unique_members.append(mob)
        return unique_members

    def _base_opacity_for(self, mob: VMobject) -> tuple[float, float]:
        mob_id = id(mob)
        cached = self._base_opacity_by_mobject_id.get(mob_id)
        if cached is not None:
            return cached

        stroke_opacity = float(mob.get_stroke_opacity())
        fill_opacity = float(mob.get_fill_opacity())
        cached = (stroke_opacity, fill_opacity)
        self._base_opacity_by_mobject_id[mob_id] = cached
        return cached

    def _add_co_substrate_pair(self, reaction_id: str) -> None:
        key = self._reaction_key(reaction_id)
        arrow = self.reaction_by_id.get(key)
        if arrow is None:
            return

        arrow_start = arrow.get_start()
        arrow_end = arrow.get_end()
        arrow_vec = arrow_end - arrow_start
        arrow_length = float(np.linalg.norm(arrow_vec))

        if arrow_length == 0:
            return

        direction = arrow_vec / arrow_length
        perpendicular = np.array([-direction[1], direction[0], 0.0])

        # Position co-substrates at 25% and 75% along the reaction
        input_pos = arrow_start + (direction * arrow_length * 0.25)
        output_pos = arrow_start + (direction * arrow_length * 0.75)

        # Both arrows merge at 50% (middle of reaction)
        merge_point = arrow_start + (direction * arrow_length * 0.50)

        # Create nodes positioned perpendicular to the reaction
        input_node = self._make_node(radius=_CO_SUBSTRATE_RADIUS)
        output_node = self._make_node(radius=_CO_SUBSTRATE_RADIUS)
        input_node.move_to(input_pos + (perpendicular * _CO_SUBSTRATE_GAP))
        output_node.move_to(output_pos - (perpendicular * _CO_SUBSTRATE_GAP))
        self.co_substrate_nodes.add(input_node, output_node)

        # Adjust arrow start/end points to respect node radius
        in_start = input_node.get_center()
        in_vec = merge_point - in_start
        in_norm = float(np.linalg.norm(in_vec))
        if in_norm > 0:
            in_start = in_start + ((in_vec / in_norm) * (_CO_SUBSTRATE_RADIUS + 0.01))

        out_end = output_node.get_center()
        out_vec = out_end - merge_point
        out_norm = float(np.linalg.norm(out_vec))
        if out_norm > 0:
            out_end = out_end - ((out_vec / out_norm) * (_CO_SUBSTRATE_RADIUS + 0.01))

        # Determine arc direction based on which side the co-substrate is on
        arc_sign = 1.0 if perpendicular[1] > 0 else -1.0

        # Input arrow: angles towards the reaction, arriving parallel at merge point
        in_arrow = Arrow(
            start=in_start,
            end=merge_point,
            buff=0.0,
            path_arc=arc_sign * _CO_FLOW_ARC,
            stroke_width=STROKE_REACTION_BASE * 0.6,
            color=REACTION_COLOR,
            tip_length=0.10,
            max_stroke_width_to_length_ratio=10,
        )

        # Output arrow: starts parallel from merge point, angles away to co-substrate
        out_arrow = Arrow(
            start=merge_point,
            end=out_end,
            buff=0.0,
            path_arc=-arc_sign * _CO_FLOW_ARC,
            stroke_width=STROKE_REACTION_BASE * 0.6,
            color=REACTION_COLOR,
            tip_length=0.10,
            max_stroke_width_to_length_ratio=10,
        )
        self.co_substrate_arrows.add(in_arrow, out_arrow)
        self.co_substrates_by_reaction[key] = VGroup(
            input_node,
            output_node,
            in_arrow,
            out_arrow,
        )

    def _build_regulation_marker(self, arrow: Arrow, direction: str) -> Arrow:
        flow = arrow.get_end() - arrow.get_start()
        flow_norm = float(np.linalg.norm(flow))
        if flow_norm == 0:
            flow_unit = np.array([1.0, 0.0, 0.0])
        else:
            flow_unit = flow / flow_norm

        perpendicular = np.array([-flow_unit[1], flow_unit[0], 0.0])
        anchor = arrow.get_center() + (0.32 * perpendicular)

        if str(direction).strip().lower() == "up":
            start = anchor + (0.16 * DOWN)
            end = anchor + (0.16 * UP)
            color = UP_ARROW_COLOR
        else:
            start = anchor + (0.16 * UP)
            end = anchor + (0.16 * DOWN)
            color = DOWN_ARROW_COLOR

        return Arrow(
            start=start,
            end=end,
            buff=0.0,
            stroke_width=STROKE_REACTION_BASE,
            color=color,
            tip_length=0.12,
            max_stroke_width_to_length_ratio=10,
        )

    def reset_reaction_colors(self, reaction_ids: list[str]) -> Animation:
        """Reset multiple reactions to default color in one animation."""
        arrows = []
        for rid in reaction_ids:
            key = self._reaction_key(rid)
            arrow = self.reaction_by_id.get(key)
            if arrow is not None:
                arrows.append(arrow)

        if not arrows:
            return AnimationGroup()

        animation_group = VGroup(*arrows)
        start_colors = {id(arrow): arrow.get_color() for arrow in arrows}
        target_color = REACTION_COLOR

        def update_arrow_colors(updated_group: VGroup, alpha: float) -> VGroup:
            for arrow in arrows:
                start_color = start_colors[id(arrow)]
                current_color = ManimColor(
                    interpolate_color(start_color, target_color, alpha)
                )
                # Reset the full arrow color (shaft + tip) in one call.
                arrow.set_color(current_color)
                tip = getattr(arrow, "tip", None)
                if tip is not None:
                    tip.set_fill(color=current_color)
                    tip.set_stroke(color=current_color)
            return updated_group

        return UpdateFromAlphaFunc(animation_group, update_arrow_colors)
