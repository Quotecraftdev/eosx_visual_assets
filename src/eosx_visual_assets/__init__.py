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

__version__ = "0.1.0"

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
