# ==============================================================
# File: __init__.py
# Version: v0.1.0 | Date: 2026-07-14
# Purpose: Public API for eosx-visual-assets — the shared brand and
#          asset library for the Energy OSX platform.
# ==============================================================

from eosx_visual_assets import tokens
from eosx_visual_assets.apps import APPS, App, ordered_apps
from eosx_visual_assets.banner import build_banner_svg
from eosx_visual_assets.banner_html import app_banner_css, app_banner_html
from eosx_visual_assets.favicon import build_favicon_svg

# Read from the package metadata rather than typed here. These two had
# disagreed since 0.1.0 - pyproject said 0.4.1 while this said 0.1.0 - which
# is the same second-copy fault the library exists to end.
try:  # pragma: no cover - trivial
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version as _pkg_version
    try:
        __version__ = _pkg_version("eosx-visual-assets")
    except PackageNotFoundError:  # running from a source tree, not installed
        __version__ = "0.5.0"
except ImportError:  # pragma: no cover
    __version__ = "0.5.0"

__all__ = [
    "app_banner_css",
    "app_banner_html",
    "tokens",
    "APPS",
    "App",
    "ordered_apps",
    "build_banner_svg",
    "build_favicon_svg",
    "__version__",
]
