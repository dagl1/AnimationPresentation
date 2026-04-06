# start.py
import os
import subprocess

# ── Scene to render ───────────────────────────────────────────────────────────
SCENE_SELECTION = {
    "scene_1": {
        "scene_name": "Scene01Storyboard",
        "scene_file": os.path.join("src", "scenes", "scene_01.py"),
    },
    "scene_2": {
        "scene_name": "Scene02Storyboard",
        "scene_file": os.path.join("src", "scenes", "scene_2.py"),
    },
    "scene_4_debug": {
        "scene_name": "Scene04Debug",
        "scene_file": os.path.join("src", "scenes", "scene_04_debug.py"),
    },
}

selected_scene = "scene_4_debug"
SCENE = os.getenv("MANIM_SCENE", SCENE_SELECTION[selected_scene]["scene_name"])
SCENE_FILE = os.getenv("MANIM_SCENE_FILE", SCENE_SELECTION[selected_scene]["scene_file"])

QUALITY = "-qk"  # quick quality for fast iteration
RENDERER = "--renderer=opengl"
PREVIEW = "--preview"  # OpenGL live preview window
FORCE_WINDOW = "--force_window"  # ensure window creation for interactive_embed
DISABLE_CACHING = "--disable_caching"
WINDOW_RESOLUTION = "--resolution=1920,1080"  # render resolution
FULLSCREEN = "--fullscreen"  # enlarge the actual preview window on screen
WINDOW_MONITOR = (
    "--window_monitor=1"  # which monitor to display the preview window on (0-indexed)
)
WINDOW_SIZE = "--window_size=1280,720"  # preview window size (does not affect render res)
WRITE_TO_MOVIE = False  # bool flag: Manim expects --write_to_movie (no value)
INTERACTIVE_REVIEW = os.getenv(
    "MANIM_INTERACTIVE_REVIEW", "1"
)  # "1" keeps interactive_embed enabled in debug scenes
CONFIG_FILE = "custom_config.cfg"  # Manim INI config file


def main() -> None:
    # Add src/ to PYTHONPATH so `from components.xxx` and `from utils.xxx`
    # resolve correctly when manim executes the scene file.
    src_dir = os.path.dirname(os.path.abspath(__file__))
    env = os.environ.copy()
    env["PYTHONPATH"] = src_dir + os.pathsep + env.get("PYTHONPATH", "")
    env["MANIM_INTERACTIVE_REVIEW"] = INTERACTIVE_REVIEW

    # Change to project root so Manim auto-detects custom_config.yml
    project_root = os.path.dirname(src_dir)

    command = [
        "manim",
        QUALITY,
        "-c",
        CONFIG_FILE,
        RENDERER,
        PREVIEW,
        FORCE_WINDOW,
        FULLSCREEN,
        DISABLE_CACHING,
        WINDOW_RESOLUTION,
        SCENE_FILE,
        SCENE,
    ]
    if WRITE_TO_MOVIE:
        command.insert(8, "--write_to_movie")

    # Run from project root so custom_config.yml is auto-detected
    subprocess.run(command, env=env, cwd=project_root)


if __name__ == "__main__":
    main()
