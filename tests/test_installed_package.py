# ==============================================================
# File: test_installed_package.py
# Version: v1.0.0 | Date: 2026-10-04
# Purpose: Prove the package works the way a consumer uses it -
#          installed, with this repository nowhere on sys.path.
#
#          Every other test in this suite runs from the source
#          tree, where the registry sits beside the code and any
#          path arithmetic happens to resolve. That is why 0.2.0
#          shipped: sixty green tests, and an installed copy that
#          raised FileNotFoundError on import. A suite that only
#          proves the source tree works is the suite that lets
#          this through.
#
#          Slow by design - it builds and installs. Run it.
# ==============================================================

from __future__ import annotations

import json
import os
import subprocess
import sys
import venv
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_APPS = [
    "bespoke", "custom", "dashboard", "integrity", "learning", "market",
    "pipeline", "pricing", "professional", "settlement", "signal",
]


def _venv_python(env_dir: Path) -> Path:
    return env_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


@pytest.fixture(scope="module")
def installed_python(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A throwaway virtualenv with this package installed from the repo."""
    env_dir = tmp_path_factory.mktemp("install-proof-venv")
    venv.create(env_dir, with_pip=True)
    python = _venv_python(env_dir)
    result = subprocess.run(
        [str(python), "-m", "pip", "install", "--quiet", str(REPO_ROOT)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.fail(f"pip install of the repo failed:\n{result.stdout}\n{result.stderr}")
    return python


def _run_installed(python: Path, code: str, cwd: Path) -> subprocess.CompletedProcess:
    """Run code in the installed interpreter with the repo kept off sys.path.

    cwd is a scratch directory, never the repo, because Python puts the
    script's directory on sys.path and running from the repo root would
    import src/ instead of the installed copy - hiding the very bug this
    test exists to catch. PYTHONPATH is stripped for the same reason.
    """
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    return subprocess.run(
        [str(python), "-c", code], cwd=str(cwd), env=env, capture_output=True, text=True
    )


@pytest.mark.slow
def test_installed_package_imports(installed_python: Path, tmp_path: Path) -> None:
    """`import eosx_visual_assets` must not raise on an installed copy."""
    code = (
        "import eosx_visual_assets, sys, json;"
        "print(json.dumps({'file': eosx_visual_assets.__file__,"
        " 'repo_on_path': any('eosx_visual_assets' in p and 'site-packages' not in p"
        " for p in sys.path)}))"
    )
    result = _run_installed(installed_python, code, tmp_path)
    assert result.returncode == 0, (
        "the installed package does not import:\n" + result.stderr
    )
    info = json.loads(result.stdout)
    assert "site-packages" in info["file"], (
        f"imported the source tree, not the installed copy: {info['file']}"
    )
    assert not info["repo_on_path"], "the repo is on sys.path; this test proves nothing"


@pytest.mark.slow
def test_installed_registry_holds_every_app(installed_python: Path, tmp_path: Path) -> None:
    """The registry must travel with the package, not be left in the checkout."""
    code = (
        "import json; from eosx_visual_assets import tokens;"
        "print(json.dumps(sorted(tokens.TOKENS['apps'])))"
    )
    result = _run_installed(installed_python, code, tmp_path)
    assert result.returncode == 0, (
        "the registry did not load from the installed package:\n" + result.stderr
    )
    assert json.loads(result.stdout) == EXPECTED_APPS


@pytest.mark.slow
def test_installed_tokens_path_points_at_a_real_file(
    installed_python: Path, tmp_path: Path
) -> None:
    """TOKENS_PATH is exported, so it must be a path that exists - not a guess."""
    code = (
        "import json; from eosx_visual_assets import tokens;"
        "p = tokens.TOKENS_PATH;"
        "print(json.dumps({'path': str(p), 'exists': bool(p and p.exists())}))"
    )
    result = _run_installed(installed_python, code, tmp_path)
    assert result.returncode == 0, result.stderr
    info = json.loads(result.stdout)
    assert info["exists"], f"TOKENS_PATH does not exist on an installed copy: {info['path']}"


@pytest.mark.slow
def test_console_script_is_installed(installed_python: Path) -> None:
    """eosx-assets-build is declared in pyproject; check it was actually created."""
    script = installed_python.parent / (
        "eosx-assets-build.exe" if sys.platform == "win32" else "eosx-assets-build"
    )
    assert script.exists(), f"console script missing from the install: {script}"
