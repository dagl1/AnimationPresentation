"""
config.py – Manim configuration settings for AnimationPresentation.

This module configures Manim's rendering, window, and style settings.
Import and use with:
    from config import config as manim_config
"""

from manim import config as global_config

# Create a copy of the global config to customize
config = global_config.copy()

# ─── Directories ─────────────────────────────────────────────────────────
config.media_dir = "E:\\Git\\AnimationPresentation\\Data\\videos\\"
config.images_dir = "E:\\Git\\AnimationPresentation\\Data\\raster_images\\"
config.vector_images_dir = "E:\\Git\\AnimationPresentation\\Data\\vector_images\\"
config.sounds_dir = "E:\\Git\\AnimationPresentation\\Data\\sounds\\"
config.temporary_storage = "C:/TempLatex/"

# ─── Rendering ───────────────────────────────────────────────────────────
config.pixel_height = 1080
config.pixel_width = 1920
config.frame_rate = 30
config.preview = True
config.renderer = "opengl"
config.write_to_movie = False
config.disable_caching = True

# ─── Window / Preview ────────────────────────────────────────────────────
config.window_size = (1920, 1080)  # Preview window size
config.window_position = "UR"  # Upper Right corner
config.window_monitor = 0  # Monitor index
config.full_screen = True  # Fullscreen preview window

# ─── Style ───────────────────────────────────────────────────────────────
config.background_color = "#000000"  # Black background
config.tex_template = "default"
config.text_alignment = "left"

# ─── Debug / Logging ─────────────────────────────────────────────────────
config.embed_exception_mode = "Verbose"
config.embed_error_sound = False
config.log_to_file = False
