"""
graph_plot.py – GraphPlot: stylised x/y plot component.

Style
-----
  - Faint gridlines
  - Clean axes, minimal ticks
  - Mostly positive value ranges
  - Smooth point / curve animations

Sub-types (subclasses, to be implemented)
-----------------------------------------
  PTRVariancePlot        – categorical x-axis, R² on y
  DetectionLimitPlot     – point cloud + horizontal detection-limit line
  RNAHalfLifePlot        – time vs concentration, 3 curves
  RNATurnoverPlot        – PDE-driven curve, interactive parameters
  ProteinTurnoverPlot    – similar to RNA turnover
  PTRMissingnessPlot     – boxplots + regression, 0–29 missing tissues
  KcatDistributionPlot   – per-compartment, log10 y-axis
"""
from __future__ import annotations

from manim import VGroup, VMobject, Animation, AnimationGroup, Axes, YELLOW

from components.base import BaseComponent
from utils.styling import DEBUG


class GraphPlot(BaseComponent):
    """
    Base class for all graph/plot components.

    Parameters
    ----------
    x_range : tuple   (x_min, x_max, x_step)
    y_range : tuple   (y_min, y_max, y_step)
    x_label : str
    y_label : str
    show_grid : bool
    debug : bool
    """

    def __init__(
        self,
        x_range:   tuple = (0, 10, 1),
        y_range:   tuple = (0, 10, 1),
        x_label:   str   = "",
        y_label:   str   = "",
        show_grid: bool  = True,
        debug:     bool  = DEBUG,
        **kwargs,
    ) -> None:
        self.x_range   = x_range
        self.y_range   = y_range
        self.x_label   = x_label
        self.y_label   = y_label
        self.show_grid = show_grid

        self.axes:            Axes | None    = None
        self.data_dots:       VGroup         = VGroup()
        self.threshold_line:  VMobject | None = None

        super().__init__(debug=debug, **kwargs)
        self._build()
        if debug:
            self._add_debug_overlays()

    # ─── Build ───────────────────────────────────────────────────────────────

    def _build(self) -> None:
        # TODO: construct stylised axes with faint gridlines
        pass

    # ─── Public API ──────────────────────────────────────────────────────────

    def show_threshold(self, y: float, color: str = YELLOW) -> VMobject:
        """Draw a horizontal threshold line at the given y value."""
        raise NotImplementedError

    def highlight_region(self, y_min: float, y_max: float) -> VMobject:
        """Shade the area between y_min and y_max on the plot."""
        raise NotImplementedError

    def animate_points(
        self, points: list[tuple[float, float]]
    ) -> AnimationGroup:
        """Animate data points appearing one by one."""
        raise NotImplementedError

    def add_regression_line(self, slope: float, intercept: float) -> VMobject:
        """Overlay a regression line on the plot."""
        raise NotImplementedError

    def animate_curve_change(self, new_params: dict) -> Animation:
        """Smoothly morph the plotted curve when parameters change."""
        raise NotImplementedError

