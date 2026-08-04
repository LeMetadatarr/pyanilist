"""pyanilist — AniList anime/manga catalog bulk harvesters, grouped on harvestkit.

Importing this package imports :mod:`pyanilist.harvest`, which in turn
imports every scraper module so it registers itself with
:mod:`harvestkit.engine` (``@register``).
"""
from pyanilist.version import __version__

import pyanilist.harvest  # noqa: F401  (import for @register side effects)

__all__ = ["__version__"]
