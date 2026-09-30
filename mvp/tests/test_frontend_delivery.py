import pytest


pytest.importorskip('fastapi', reason='FastAPI is an optional MVP dependency')
pytest.importorskip('multipart', reason='python-multipart is required by the upload endpoint')
pytest.importorskip('httpx', reason='httpx is required by FastAPI TestClient')

from fastapi.testclient import TestClient

from mvp.backend.main import app


def test_frontend_html_css_and_javascript_are_served():
    client = TestClient(app)

    for path, expected_content in (
        ('/', 'کاتالوگ محصولات'),
        ('/css/base.css', ':root'),
        ('/js/app.js', "from './api.js'"),
    ):
        response = client.get(path)
        assert response.status_code == 200
        assert expected_content in response.text
