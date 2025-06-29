import app.api.v1.journal as journal_api
from fastapi.background import BackgroundTasks


def test_create_journal_schedules_analysis(client, monkeypatch):
    client_app, _ = client
    captured = {}

    def fake_add_task(self, func, *args, **kwargs):
        captured['func'] = func
        captured['args'] = args
        captured['kwargs'] = kwargs

    monkeypatch.setattr(BackgroundTasks, 'add_task', fake_add_task)

    dummy_task = lambda user_id: None
    monkeypatch.setattr(journal_api, 'analyze_profile_task', dummy_task)

    resp = client_app.post(
        '/api/v1/journals/',
        json={'title': 't', 'content': 'c', 'mood': 'ok'}
    )
    assert resp.status_code == 200
    assert captured['func'] is dummy_task
    assert captured['args'][0] == 1

