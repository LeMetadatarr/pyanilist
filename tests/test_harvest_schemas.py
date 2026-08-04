"""Row-schema equivalence tests for the 2 AniList scrapers.

Relocated verbatim (assertions untouched) from metadatarr's
test_scrapers_batch2.py / test_scrapers_batch3.py, keeping only the tests
for scrapers that live in this package, re-pointed at pyanilist.harvest.*.
These lock the exact flat-row shape each scraper emits (the contract the
LeData datasets depend on) against a realistic upstream sample, so a future
engine change can't silently alter the output schema.
"""
from __future__ import annotations

from harvestkit.engine import all_sources

from pyanilist.harvest.anilist_anime import AniListAnimeSource
from pyanilist.harvest.anilist_crawl import AniListCrawlSource


# ---------------------------------------------------------------------------
# anilist_anime  (from test_scrapers_batch2.py)
# ---------------------------------------------------------------------------

def test_anilist_map_row_schema():
    src = AniListAnimeSource()
    m = {
        "id": 1,
        "idMal": 21,
        "title": {"romaji": "Cowboy Bebop", "english": "Cowboy Bebop", "native": "カウボーイビバップ"},
        "type": "ANIME",
        "format": "TV",
        "status": "FINISHED",
        "episodes": 26,
        "duration": 24,
        "chapters": None,
        "volumes": None,
        "countryOfOrigin": "JP",
        "source": "ORIGINAL",
        "startDate": {"year": 1998, "month": 4, "day": 3},
        "endDate": {"year": 1999, "month": 4, "day": 24},
        "season": "SPRING",
        "seasonYear": 1998,
        "genres": ["Action"],
        "tags": [{"name": "Space", "category": "Setting", "isAdult": False}],
        "studios": {"nodes": [{"id": 14, "name": "Sunrise"}]},
        "averageScore": 86,
        "popularity": 100000,
        "favourites": 5000,
        "isAdult": False,
    }
    row = src.map_row(m)
    assert row["anilist_id"] == 1
    assert row["start_date"] == "1998-04-03"
    assert row["tags"] == ["Space"]
    assert row["studios"] == ["Sunrise"]
    assert set(row) == {
        "anilist_id", "mal_id", "title_romaji", "title_english", "title_native",
        "type", "format", "status", "episodes", "duration", "chapters", "volumes",
        "country_of_origin", "source_material", "start_date", "end_date", "season",
        "season_year", "genres", "tags", "studios", "studio_ids", "average_score",
        "popularity", "favourites", "is_adult",
    }


def test_anilist_fetch_advances_page_then_type(monkeypatch):
    src = AniListAnimeSource()
    src.media_types = ["ANIME", "MANGA"]

    class FakeResp:
        def __init__(self, payload, status=200):
            self._payload = payload
            self.status_code = status
            self.headers = {}

        def raise_for_status(self):
            pass

        def json(self):
            return self._payload

    class FakeSession:
        def post(self, url, json=None, headers=None, timeout=None):
            page = json["variables"]["page"]
            mtype = json["variables"]["type"]
            if mtype == "ANIME" and page == 1:
                return FakeResp({"data": {"Page": {"pageInfo": {"hasNextPage": True}, "media": [{"id": 1}]}}})
            if mtype == "ANIME" and page == 2:
                return FakeResp({"data": {"Page": {"pageInfo": {"hasNextPage": False}, "media": [{"id": 2}]}}})
            return FakeResp({"data": {"Page": {"pageInfo": {"hasNextPage": False}, "media": []}}})

    src._session = FakeSession()
    src.throttle.wait = lambda: None

    rows, cursor = src.fetch({"type_idx": 0, "page": 1})
    assert len(rows) == 1
    assert cursor == {"type_idx": 0, "page": 2}

    rows, cursor = src.fetch(cursor)
    assert len(rows) == 1
    assert cursor == {"type_idx": 1, "page": 1}


# ---------------------------------------------------------------------------
# anilist_crawl  (from test_scrapers_batch3.py)
# ---------------------------------------------------------------------------

def test_anilist_crawl_map_row_schema():
    src = AniListCrawlSource()
    m = {
        "id": 1, "idMal": 21,
        "title": {"romaji": "Cowboy Bebop", "english": "Cowboy Bebop", "native": "カウボーイビバップ"},
        "type": "ANIME", "format": "TV", "status": "FINISHED",
        "episodes": 26, "duration": 24, "chapters": None, "volumes": None,
        "countryOfOrigin": "JP", "source": "ORIGINAL",
        "startDate": {"year": 1998, "month": 4, "day": 3},
        "endDate": {"year": 1999, "month": 4, "day": 24},
        "season": "SPRING", "seasonYear": 1998,
        "genres": ["Action"],
        "tags": [{"name": "Space", "isAdult": False}],
        "studios": {"nodes": [{"id": 14, "name": "Sunrise"}]},
        "averageScore": 86, "popularity": 100000, "favourites": 5000, "isAdult": False,
    }
    row = src.map_row(m)
    assert row["anilist_id"] == 1
    assert row["start_date"] == "1998-04-03"
    assert row["tags"] == ["Space"]
    assert set(row) == {
        "anilist_id", "mal_id", "title_romaji", "title_english", "title_native",
        "type", "format", "status", "episodes", "duration", "chapters", "volumes",
        "country_of_origin", "source_material", "start_date", "end_date", "season",
        "season_year", "genres", "tags", "studios", "studio_ids", "average_score",
        "popularity", "favourites", "is_adult",
    }


def test_anilist_crawl_fetch_walks_id_chunks_and_stops_at_max_id():
    src = AniListCrawlSource()
    src.max_id = 600
    src.throttle.wait = lambda: None

    class FakeResp:
        def __init__(self, payload):
            self._payload = payload
            self.status_code = 200
            self.headers = {}

        def raise_for_status(self):
            pass

        def json(self):
            return self._payload

    class FakeSession:
        def post(self, url, json=None, headers=None, timeout=None):
            ids = json["variables"]["ids"]
            media = [{"id": ids[0]}] if ids else []
            return FakeResp({"data": {"Page": {"pageInfo": {"hasNextPage": False}, "media": media}}})

    src._session = FakeSession()
    rows, cursor = src.fetch(1)
    assert len(rows) == 1
    assert cursor == 501

    rows, cursor = src.fetch(cursor)
    assert cursor is None


def test_pyanilist_scrapers_are_registered():
    reg = all_sources()
    assert reg.get("anilist_anime") is AniListAnimeSource
    assert reg.get("anilist_crawl") is AniListCrawlSource
