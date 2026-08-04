# pyanilist

2 AniList anime/manga catalog bulk harvesters grouped onto the
[harvestkit](https://github.com/LeMetadatarr/harvestkit) resumable-harvest
engine. Extracted from [metadatarr](https://github.com/TigreGotico/metadatarr)'s
scraper collection into its own standalone package.

## Sources

| Scraper | Registry name | Source |
| --- | --- | --- |
| `anilist_anime` | `anilist_anime` | AniList GraphQL, paginated (`--type ANIME/MANGA/ALL`) |
| `anilist_crawl` | `anilist_crawl` | AniList GraphQL, sequential `id_in` sweep — tops up the same `anilist_anime` dataset |

## Install

```bash
pip install pyanilist
# or, for the HuggingFace publisher (via harvestkit):
pip install "pyanilist[hf]"
# or, for Cloudflare-guarded sources:
pip install "pyanilist[stealth]"
```

## Usage

```bash
# list every registered scraper
pyanilist-harvest --list

# harvest one source (resumable — safe to Ctrl-C and rerun)
pyanilist-harvest anilist_anime --output ~/.cache/metadatarr/scrapers/
```

Every scraper is a `harvestkit.engine.Source` subclass: checkpoint/dedup/
pagination/throttle are handled by the shared engine, each module only
answers `initial_cursor()` and `fetch(cursor)`. See
[harvestkit](https://github.com/LeMetadatarr/harvestkit) for the full engine
API.

## License

Apache-2.0
