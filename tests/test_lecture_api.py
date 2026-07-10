from fastapi.testclient import TestClient

from ai_media_lab.lecture.app import app


def test_lecture_upload_returns_complete_study_pack(tmp_path, monkeypatch):
    monkeypatch.setenv("AI_MEDIA_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("AI_MEDIA_FORCE_DEMO", "1")
    client = TestClient(app)

    response = client.post(
        "/api/analyze",
        files={
            "file": (
                "lecture.txt",
                b"Neural networks learn patterns from data. Backpropagation updates weights. Evaluation prevents overfitting.",
                "text/plain",
            )
        },
        data={"topic": "Neural Networks", "demo_mode": "true"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["analysis"]["title"] == "Neural Networks"
    assert payload["analysis"]["clean_notes"]
    assert payload["analysis"]["quiz_questions"]

    markdown = client.get(payload["markdown_url"])
    assert markdown.status_code == 200
    assert "## Quiz" in markdown.text

