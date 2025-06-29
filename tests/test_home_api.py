from app import crud, schemas


def _create_sample_data(db):
    crud.article.create(db, obj_in=schemas.ArticleCreate(title="a1", url="u1"))
    crud.article.create(db, obj_in=schemas.ArticleCreate(title="a2", url="u2"))
    crud.audio_track.create(db, obj_in=schemas.AudioTrackCreate(title="t1", url="au1"))
    crud.motivational_quote.create(db, obj_in=schemas.MotivationalQuoteCreate(text="q1", author="au"))


def test_home_feed_structure_and_ordering(client):
    client_app, session_local = client
    db = session_local()
    try:
        _create_sample_data(db)
    finally:
        db.close()

    resp = client_app.get("/api/v1/home-feed")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 4
    assert all("type" in item and "data" in item for item in data)
    ids = [item["data"]["id"] for item in data]
    assert ids == sorted(ids, reverse=True)
    types = {item["type"] for item in data}
    assert types == {"article", "audio", "quote"}
