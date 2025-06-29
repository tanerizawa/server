from app import crud, schemas


def test_articles_endpoint_empty_returns_list(client):
    client_app, _ = client
    resp = client_app.get("/api/v1/articles")
    assert resp.status_code == 200
    data = resp.json()
    assert data == []
    assert isinstance(data, list)


def test_articles_endpoint_returns_items(client):
    client_app, session_local = client
    db = session_local()
    try:
        crud.article.create(db, obj_in=schemas.ArticleCreate(title="t1", url="u1"))
        crud.article.create(db, obj_in=schemas.ArticleCreate(title="t2", url="u2"))
    finally:
        db.close()

    resp = client_app.get("/api/v1/articles")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_audio_endpoint_empty_returns_list(client):
    client_app, _ = client
    resp = client_app.get("/api/v1/audio")
    assert resp.status_code == 200
    data = resp.json()
    assert data == []
    assert isinstance(data, list)


def test_audio_endpoint_returns_items(client):
    client_app, session_local = client
    db = session_local()
    try:
        crud.audio_track.create(db, obj_in=schemas.AudioTrackCreate(title="a1", url="u1"))
    finally:
        db.close()

    resp = client_app.get("/api/v1/audio")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 1


def test_quotes_endpoint_empty_returns_list(client):
    client_app, _ = client
    resp = client_app.get("/api/v1/quotes")
    assert resp.status_code == 200
    data = resp.json()
    assert data == []
    assert isinstance(data, list)


def test_quotes_endpoint_returns_items(client):
    client_app, session_local = client
    db = session_local()
    try:
        crud.motivational_quote.create(
            db,
            obj_in=schemas.MotivationalQuoteCreate(text="q1", author="anon"),
        )
        crud.motivational_quote.create(
            db,
            obj_in=schemas.MotivationalQuoteCreate(text="q2", author="anon"),
        )
    finally:
        db.close()

    resp = client_app.get("/api/v1/quotes")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2
