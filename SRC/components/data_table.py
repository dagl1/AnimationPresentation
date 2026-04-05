"""
data_table.py – DataTable: clean, fully-animatable Manim table component.

Builds on top of ModifiableTable in utils/Utilities.py.

Supports:
  - Row / column highlighting (yellow glow)
  - Computing and displaying column medians
  - Showing normalisation ratios
  - Imputation animation (fill missing cell)
  - Appending new rows
  - Sliding rows out right and squishing remaining rows together
"""

from __future__ import annotations

from manim import YELLOW, Animation, AnimationGroup, VGroup

from components.base import BaseComponent
from utils.styling import DEBUG, FONT_SIZE_TABLE, HIGHLIGHT_COLOR


class DataTable(BaseComponent):
    """
    Animatable data table.

    Parameters
    ----------
    data : dict
        { row_label (str) → list[str | number] }
        Each value list must be the same length (= number of data columns).
    column_headers : list[str], optional
        Header labels for each data column (excluding the row-label column).
    fontsize : int
        Font size used for all cell text.
    debug : bool
    """

    def __init__(
        self,
        data: dict,
        column_headers: list[str] | None = None,
        fontsize: int = FONT_SIZE_TABLE,
        debug: bool = DEBUG,
        **kwargs,
    ) -> None:
        self.data = data
        self.column_headers = column_headers or []
        self.fontsize = fontsize

        # Named sub-groups
        self.header_group: VGroup = VGroup()
        self.row_groups: list[VGroup] = []
        # (row_idx, col_idx) → cell Mobject for targeted animation
        self.cell_map: dict = {}

        super().__init__(debug=debug, **kwargs)
        self._build()
        if debug:
            self._add_debug_overlays()

    # ─── Build ───────────────────────────────────────────────────────────────

    def _build(self) -> None:
        # TODO: implement clean grid table using cell rectangles + Text
        # Reference: ModifiableTable.create_table_with_removable_objects()
        #            in utils/Utilities.py for the removable-row pattern.
        pass

    # ─── Public API ──────────────────────────────────────────────────────────

    def highlight_rows(
        self,
        indices: list[int],
        color: str = HIGHLIGHT_COLOR,
    ) -> AnimationGroup:
        """Flash a yellow highlight over the specified row indices."""
        raise NotImplementedError

    def highlight_columns(
        self,
        indices: list[int],
        color: str = HIGHLIGHT_COLOR,
    ) -> AnimationGroup:
        """Flash a yellow highlight over the specified column indices."""
        raise NotImplementedError

    def compute_median(self, col_idx: int) -> Animation:
        """Animate the median value appearing above the specified column."""
        raise NotImplementedError

    def show_ratio_to_median(self, col_idx: int) -> Animation:
        """Display normalised ratio values replacing raw values in a column."""
        raise NotImplementedError

    def show_imputation(self, row_idx: int, col_idx: int, value: str) -> Animation:
        """
        Fill a missing cell with an imputed value using a write animation.

        Parameters
        ----------
        row_idx : int   0-based row index.
        col_idx : int   0-based column index (0 = data column 1).
        value : str     The imputed value to display.
        """
        raise NotImplementedError

    def add_rows(self, rows: dict) -> Animation:
        """
        Append new row entries to the bottom of the table.

        Parameters
        ----------
        rows : dict   Same format as the constructor ``data`` dict.
        """
        raise NotImplementedError

    def fade_rows(self, indices: list[int]) -> Animation:
        """
        Slide specified rows out to the right, fade them, then squish the
        remaining rows together.

        Pattern sourced from utils/Utilities.py (ModifiableTable).
        """
        raise NotImplementedError
