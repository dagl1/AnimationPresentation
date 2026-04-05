# run_scene.py – Quick scene launcher
import os
import subprocess
import sys

def run_scene(scene_name: str, scene_file: str) -> None:
    """Run a specific scene with custom config."""
    env = os.environ.copy()
    src_dir = os.path.dirname(os.path.abspath(__file__))
    env["PYTHONPATH"] = os.path.join(src_dir, "src") + os.pathsep + env.get("PYTHONPATH", "")
    env["MANIM_INTERACTIVE_REVIEW"] = "1"

    project_root = src_dir

    command = [
        "manim",
        "-qk",
        "-c", "custom_config.cfg",
        "--renderer=opengl",
        "--preview",
        "--force_window",
        "--fullscreen",
        "--disable_caching",
        "--resolution=1920,1080",
        scene_file,
        scene_name,
    ]

    subprocess.run(command, env=env, cwd=project_root)


if __name__ == "__main__":
    # Examples:
    # python run_scene.py MetabolicModelDebug src/scenes/scene_01.py
    # python run_scene.py BiologicalContextDebug src/scenes/scene_01_biological_context.py

    if len(sys.argv) < 3:
        print("Usage: python run_scene.py <SCENE_NAME> <SCENE_FILE>")
        print("\nExamples:")
        print("  python run_scene.py MetabolicModelDebug src/scenes/scene_01.py")
        print("  python run_scene.py BiologicalContextDebug src/scenes/scene_01_biological_context.py")
        sys.exit(1)

    scene_name = sys.argv[1]
    scene_file = sys.argv[2]
    run_scene(scene_name, scene_file)

