import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    parser.add_argument("examples", type=Path)
    args = parser.parse_args()
    artifact, examples = args.artifact.resolve(), args.examples.resolve()
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    with tempfile.TemporaryDirectory(prefix="outcome-check-release-") as directory:
        root = Path(directory)
        subprocess.run([sys.executable, "-m", "venv", str(root / "venv")], check=True, env=env)
        scripts = root / "venv" / ("Scripts" if os.name == "nt" else "bin")
        python = scripts / ("python.exe" if os.name == "nt" else "python")
        subprocess.run(
            ["uv", "pip", "install", "--python", str(python), str(artifact)],
            cwd=root,
            env=env,
            check=True,
        )
        origin = subprocess.check_output(
            [str(python), "-c", "import outcome_check; print(outcome_check.__file__)"],
            cwd=root,
            env=env,
            text=True,
        ).strip()
        if not Path(origin).resolve().is_relative_to(root):
            raise RuntimeError("Imported checkout instead of isolated artifact")
        command = scripts / ("outcome-check.exe" if os.name == "nt" else "outcome-check")
        result = subprocess.run(
            [str(command), str(examples / "packet.json")],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
        )
        expected = json.loads((examples / "expected.json").read_text())
        if (
            result.returncode != expected["exit_code"]
            or json.loads(result.stdout)["counts"] != expected["counts"]
        ):
            raise RuntimeError(f"Release smoke failed: {result.returncode} {result.stderr}")
        print("PASS: isolated installed artifact; synthetic missing/partial case")


if __name__ == "__main__":
    main()
