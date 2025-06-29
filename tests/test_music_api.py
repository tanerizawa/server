# tests/test_music_api.py (Versi Perbaikan)

import pytest
from unittest.mock import AsyncMock
from spotipy import Spotify
from app.core.config import settings
from app.api.v1 import music

from app import crud
from app.models.journal import Journal
from app.services.music_keyword_service import MusicKeywordService


def test_music_endpoint_returns_list(client, monkeypatch):
    monkeypatch.setattr(settings, "SPOTIFY_CLIENT_ID", "id")
    monkeypatch.setattr(settings, "SPOTIFY_CLIENT_SECRET", "secret")
    monkeypatch.setattr(music, "spotify", None)
    # Return fake Spotify search payload
    def fake_search(self, q, type="track", limit=20):
        return {"tracks": {"items": [{"name": "Song", "id": "abc123"}]}}

    # Kita tidak lagi memanggil get_song di backend, jadi mock ini bisa disederhanakan/dihapus.
    # Namun, kita biarkan untuk keamanan jika ada logika lain yang mungkin memanggilnya.
    monkeypatch.setattr(Spotify, "search", fake_search)

    client_app, _ = client
    resp = client_app.get("/api/v1/music?mood=test")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]["url"] == "abc123"


def test_music_recommend_uses_keyword_and_journals(client, monkeypatch):
    monkeypatch.setattr(settings, "SPOTIFY_CLIENT_ID", "id")
    monkeypatch.setattr(settings, "SPOTIFY_CLIENT_SECRET", "secret")
    monkeypatch.setattr(music, "spotify", None)
    captured = {}

    # --- PERBAIKAN 2: Menambahkan `order_by` ke mock ---
    def fake_get_multi_by_owner(db, owner_id: int, skip: int = 0, limit: int = 100, order_by: str = None):
        captured["limit"] = limit
        # Memastikan mock mengembalikan objek Journal yang valid
        return [Journal(id=i, content=f"j{i}", owner_id=owner_id) for i in range(3)]

    async def fake_generate_keyword(self, journals):
        captured["journals"] = journals
        return "lofi"

    def fake_search(self, q, type="track", limit=20):
        captured["query"] = q
        return {"tracks": {"items": [{"name": "Song", "id": "xyz"}]}}

    # Mock ini tidak lagi dipanggil oleh logika utama, tetapi kita biarkan untuk keamanan.
    monkeypatch.setattr(crud.journal, "get_multi_by_owner", fake_get_multi_by_owner)
    monkeypatch.setattr(MusicKeywordService, "generate_keyword", fake_generate_keyword)
    monkeypatch.setattr(Spotify, "search", fake_search)

    client_app, _ = client
    resp = client_app.get("/api/v1/music/recommend")
    assert resp.status_code == 200
    assert captured["limit"] == 5
    assert len(captured["journals"]) == 3
    assert captured["query"] == "lofi"


def test_music_recommend_returns_empty_list_when_no_results(client, monkeypatch):
    monkeypatch.setattr(settings, "SPOTIFY_CLIENT_ID", "id")
    monkeypatch.setattr(settings, "SPOTIFY_CLIENT_SECRET", "secret")
    monkeypatch.setattr(music, "spotify", None)
    # --- PERBAIKAN 3: Menambahkan `order_by` ke mock ---
    def fake_get_multi_by_owner(db, owner_id: int, skip: int = 0, limit: int = 100, order_by: str = None):
        # Mengembalikan jurnal untuk memicu logika fallback
        return [Journal(id=1, content="test", mood="Netral", owner_id=owner_id)]

    async def fake_generate_keyword(self, journals):
        return "keyword_yang_tidak_ada_hasilnya"

    # Mock search sekarang mengembalikan list kosong untuk semua query
    def fake_search(self, q, type="track", limit=20):
        return {"tracks": {"items": []}}

    monkeypatch.setattr(crud.journal, "get_multi_by_owner", fake_get_multi_by_owner)
    monkeypatch.setattr(MusicKeywordService, "generate_keyword", fake_generate_keyword)
    monkeypatch.setattr(Spotify, "search", fake_search)

    client_app, _ = client
    resp = client_app.get("/api/v1/music/recommend")
    assert resp.status_code == 200
    assert resp.json() == []


def test_music_endpoint_returns_503_without_credentials(client, monkeypatch):
    monkeypatch.setattr(settings, "SPOTIFY_CLIENT_ID", None)
    monkeypatch.setattr(settings, "SPOTIFY_CLIENT_SECRET", None)
    monkeypatch.setattr(music, "spotify", None)
    client_app, _ = client
    resp = client_app.get("/api/v1/music?mood=test")
    assert resp.status_code == 503

