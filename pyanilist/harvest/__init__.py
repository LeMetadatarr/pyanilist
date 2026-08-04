"""pyanilist.harvest — the 2 AniList bulk scrapers.

Importing this package imports every scraper module below, which registers
each one with :mod:`harvestkit.engine` (via ``@register``) as a side effect.
Run one from the command line with ``pyanilist-harvest <name>`` (see
:func:`main`), or ``python -m harvestkit <name>`` after importing this
package to populate the registry.
"""
from __future__ import annotations

import sys

from pyanilist.harvest import (
    anilist_anime,
    anilist_crawl,
)

__all__ = [
    "anilist_anime",
    "anilist_crawl",
    "main",
]


def main(argv=None) -> int:
    """Dispatch a registered scraper by name.

        pyanilist-harvest <name> [--output DIR] [--delay S] [--limit N]
        pyanilist-harvest --list

    Every module in this package is already imported (and thus registered)
    by the time this runs, since importing :mod:`pyanilist.harvest` itself
    imports them all.
    """
    from harvestkit.engine import all_sources, get_source, run_cli

    argv = list(sys.argv[1:] if argv is None else argv)

    if not argv or argv[0] in ("--list", "-l", "list"):
        for name in sorted(all_sources()):
            print(name)
        return 0

    name, rest = argv[0], argv[1:]
    try:
        source_cls = get_source(name)
    except KeyError:
        print(f"unknown scraper: {name!r}. Use --list to see available ones.",
              file=sys.stderr)
        return 2
    return run_cli(source_cls, rest)


if __name__ == "__main__":
    raise SystemExit(main())
