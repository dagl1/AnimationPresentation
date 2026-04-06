import argparse
import os
import subprocess
from pathlib import Path


# ── Scene selection ───────────────────────────────────────────────────────────
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


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bake a Manim scene to MP4 for slide embedding.",
    )
    parser.add_argument(
        "--scene-key",
        choices=sorted(SCENE_SELECTION.keys()),
        default="scene_1",
        help="Which predefined scene mapping to render.",
    )
    parser.add_argument(
        "--quality",
        default="qh",
        choices=["ql", "qm", "qh", "qk"],
        help="Manim quality preset (default: qh).",
    )
    parser.add_argument(
        "--resolution",
        default="1920,1080",
        help="Render resolution as WIDTH,HEIGHT (default: 1920,1080).",
    )
    parser.add_argument(
        "--config-file",
        default="custom_config.cfg",
        help="Manim config file path, relative to project root.",
    )
    parser.add_argument(
        "--output-file",
        default="scene_01_baked.mp4",
        help="Output filename (passed to manim -o).",
    )
    parser.add_argument(
        "--renderer",
        choices=["cairo", "opengl"],
        default="cairo",
        help="Renderer for baking (default: cairo for stable file output).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the generated command without executing it.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    selected = SCENE_SELECTION[args.scene_key]
    scene_name = os.getenv("MANIM_SCENE", selected["scene_name"])
    scene_file = os.getenv("MANIM_SCENE_FILE", selected["scene_file"])

    src_dir = Path(__file__).resolve().parent
    project_root = src_dir.parent

    env = os.environ.copy()
    env["PYTHONPATH"] = str(src_dir) + os.pathsep + env.get("PYTHONPATH", "")
    # Disable interactive holds while baking files.
    env["MANIM_INTERACTIVE_REVIEW"] = "0"

    command = [
        "manim",
        f"-q{args.quality[-1]}",
        "-c",
        args.config_file,
        "--renderer",
        args.renderer,
        "--write_to_movie",
        "--format",
        "mp4",
        "--resolution",
        args.resolution,
        "-o",
        args.output_file,
        scene_file,
        scene_name,
    ]

    print("[bake] Running from:", project_root)
    print("[bake] Command:", " ".join(command))

    if args.dry_run:
        return

    completed = subprocess.run(command, env=env, cwd=project_root, check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
