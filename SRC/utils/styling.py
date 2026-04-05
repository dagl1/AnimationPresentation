"""
styling.py – Global style constants for the entire animation system.

ALL colors, font sizes, and stroke widths must be sourced from here.
Never define visual constants inline in component or scene code.
"""

from manim import BLACK, GREEN, ORANGE, PURE_BLUE, RED, WHITE, YELLOW, ManimColor

# ─── Background ───────────────────────────────────────────────────────────────
BACKGROUND_COLOR: ManimColor = BLACK

# ─── Core element colors ──────────────────────────────────────────────────────
GENE_COLOR: ManimColor = WHITE  # gene letter labels
METABOLITE_COLOR: ManimColor = WHITE  # metabolite node outlines
REACTION_COLOR: ManimColor = WHITE  # reaction arrows

NODE_FILL_COLOR: ManimColor = BLACK
NODE_FILL_OPACITY: float = 0.0  # transparent interior by default

# ─── Expression direction arrows ─────────────────────────────────────────────
UP_ARROW_COLOR: ManimColor = ORANGE  # ↑ up-regulated  (style guide)
DOWN_ARROW_COLOR: ManimColor = ManimColor("#A855F7")  # ↓ down-regulated (purple)

# ─── Emphasis / highlight ────────────────────────────────────────────────────
# Style guide: ONLY yellow glow – never change the object's own color.
HIGHLIGHT_COLOR: ManimColor = YELLOW

# ─── Protein shape palette (3 distinct proteins) ─────────────────────────────
# Shape A – rectangle with 2 bumps  (scaffold / large subunit)
PROTEIN_SHAPE_A_COLOR: str = "#2CA02C"  # green
# Shape B – single larger rectangle (catalytic subunit)
PROTEIN_SHAPE_B_COLOR: str = "#1F77B4"  # blue
# Shape C – triangle / wedge        (regulatory subunit)
PROTEIN_SHAPE_C_COLOR: str = "#FF7F0E"  # orange

# ─── Font ────────────────────────────────────────────────────────────────────
DEFAULT_FONT: str = "Arial"

# ─── Font sizes (px, as passed to Manim Text/MathTex) ────────────────────────
FONT_SIZE_TITLE: int = 36
FONT_SIZE_GENE_LABEL: int = 22
FONT_SIZE_NODE_LABEL: int = 16
FONT_SIZE_EXPRESSION: int = 18
FONT_SIZE_TABLE: int = 22
FONT_SIZE_EQUATION: int = 36
FONT_SIZE_CAPTION: int = 20

# ─── Stroke widths ───────────────────────────────────────────────────────────
STROKE_DEFAULT: float = 2.0
STROKE_REACTION_BASE: float = 3.0  # minimum reaction arrow stroke
STROKE_REACTION_MAX: float = 12.0  # maximum stroke at flux = 1.0

# ─── Node geometry ───────────────────────────────────────────────────────────
NODE_RADIUS: float = 0.25
NODE_STROKE_WIDTH: float = 2.0

# ─── Glow parameters ─────────────────────────────────────────────────────────
GLOW_STROKE_WIDTH: float = 8.0
GLOW_OPACITY: float = 0.60

# ─── Debug overlay ───────────────────────────────────────────────────────────
# Toggle globally here; override per-component via constructor arg.
DEBUG: bool = False
DEBUG_BOX_COLOR: ManimColor = RED
DEBUG_ANCHOR_COLOR: ManimColor = GREEN
DEBUG_FONT_SIZE: int = 10
