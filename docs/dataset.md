# Dataset

This repo produces the `anilist_anime` dataset: a JSONL dump of anime and manga titles from the AniList GraphQL catalog. Two harvesters write to the same file:

- `anilist_anime` paginates the catalog by media type (`ANIME`, `MANGA`, or `ALL`).
- `anilist_crawl` scans sequential AniList IDs in batches and tops up the same file; rows already collected by `anilist_anime` are skipped.

One row represents one anime or manga title.

## Format

The output is a JSONL file at `{output_dir}/anilist_anime.jsonl`. Each line is a flat JSON object with these fields:

| Field | Type | Description |
| --- | --- | --- |
| `anilist_id` | integer | AniList ID |
| `mal_id` | integer or null | MyAnimeList ID |
| `title_romaji` | string or null | Romaji title |
| `title_english` | string or null | English title |
| `title_native` | string or null | Native title |
| `type` | string or null | `ANIME` or `MANGA` |
| `format` | string or null | Format, e.g. `TV`, `MOVIE`, `MANGA` |
| `status` | string or null | Release status |
| `episodes` | integer or null | Episode count |
| `duration` | integer or null | Episode duration in minutes |
| `chapters` | integer or null | Chapter count |
| `volumes` | integer or null | Volume count |
| `country_of_origin` | string or null | ISO country code |
| `source_material` | string or null | Original source material |
| `start_date` | string or null | Start date as `YYYY-MM-DD`, `YYYY-MM`, or `YYYY` |
| `end_date` | string or null | End date as `YYYY-MM-DD`, `YYYY-MM`, or `YYYY` |
| `season` | string or null | Release season |
| `season_year` | integer or null | Release season year |
| `genres` | list of strings | Genre list |
| `tags` | list of strings | Non-adult tag names |
| `studios` | list of strings | Main studio names |
| `studio_ids` | list of integers | Main studio IDs |
| `average_score` | integer or null | Average user score |
| `popularity` | integer or null | Popularity count |
| `favourites` | integer or null | Favourites count |
| `is_adult` | boolean | Adult flag |

## How to generate

Install the package:

```bash
pip install pyanilist
```

Harvest anime:

```bash
pyanilist-harvest anilist_anime --output ~/.cache/metadatarr/scrapers/
```

Harvest manga, or both:

```bash
pyanilist-harvest anilist_anime --type MANGA --output ~/.cache/metadatarr/scrapers/
pyanilist-harvest anilist_anime --type ALL --output ~/.cache/metadatarr/scrapers/
```

Top up missing IDs:

```bash
pyanilist-harvest anilist_crawl --output ~/.cache/metadatarr/scrapers/
```

Python equivalent:

```python
from pathlib import Path
from pyanilist.harvest.anilist_anime import AniListAnimeSource

src = AniListAnimeSource()
src.run(Path.home() / ".cache/metadatarr/scrapers")
```

## Publish on Hugging Face

Yes. The dataset is a clean, structured catalog of anime and manga metadata with multi-language titles, genres, tags, and popularity signals. It is useful for media-metadata projects, recommendation systems, and catalog classification.

## ML tasks served

- Genre and tag prediction from title and metadata.
- Catalog classification into type, format, and status.
- Recommendation systems based on genres, tags, studios, and popularity.
- Cross-lingual title normalization and entity linking.
- Release-window and seasonal-trend analysis.
