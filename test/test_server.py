#!/usr/bin/env python3
"""Tests for the Flask server endpoints.

Each test hits a real endpoint and saves the generated image to test/output/.
"""

import json
import unittest
from pathlib import Path

from src.server import app

OUTPUT_DIR = Path(__file__).parent / "output"


class ServerTestBase(unittest.TestCase):
    def setUp(self) -> None:
        app.config["TESTING"] = True
        self.client = app.test_client()
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def _post(self, endpoint: str, body: dict):
        return self.client.post(
            endpoint,
            data=json.dumps(body),
            content_type="application/json",
        )

    def _assert_png_response(self, resp, save_as: str) -> None:
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, "image/png")
        data = resp.get_data()
        self.assertGreater(len(data), 0)
        output_path = OUTPUT_DIR / save_as
        output_path.write_bytes(data)
        resp.close()


class TestHealthAndIndex(ServerTestBase):
    def test_healthz(self) -> None:
        resp = self.client.get("/healthz")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json(), {"status": "ok"})

    def test_index(self) -> None:
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("/pollack", data["endpoints"])
        self.assertIn("/twombly", data["endpoints"])

    def test_cors_preflight(self) -> None:
        resp = self.client.options(
            "/pollack",
            headers={
                "Origin": "https://example.com",
                "Access-Control-Request-Method": "POST",
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Access-Control-Allow-Origin", resp.headers)


class TestPollackEndpoint(ServerTestBase):
    def test_default_params(self) -> None:
        resp = self._post("/pollack", {})
        self._assert_png_response(resp, "pollack_default.png")

    def test_custom_params(self) -> None:
        resp = self._post("/pollack", {
            "width": 100,
            "height": 100,
            "colors": 4,
            "splats": 500,
        })
        self._assert_png_response(resp, "pollack_custom.png")

    def test_with_layers(self) -> None:
        resp = self._post("/pollack", {
            "width": 100,
            "height": 100,
            "colors": 6,
            "splats": 800,
            "layers": 3,
        })
        self._assert_png_response(resp, "pollack_layers.png")

    def test_with_border(self) -> None:
        resp = self._post("/pollack", {
            "width": 100,
            "height": 100,
            "splats": 500,
            "border": True,
        })
        self._assert_png_response(resp, "pollack_border.png")

    def test_with_alpha(self) -> None:
        resp = self._post("/pollack", {
            "width": 100,
            "height": 100,
            "splats": 500,
            "layers": 2,
            "alpha": 150,
        })
        self._assert_png_response(resp, "pollack_alpha.png")


class TestTwomblyEndpoint(ServerTestBase):
    def test_default_params(self) -> None:
        resp = self._post("/twombly", {})
        self._assert_png_response(resp, "twombly_default.png")

    def test_custom_params(self) -> None:
        resp = self._post("/twombly", {
            "width": 400,
            "height": 300,
            "colors": 5,
            "splats": 10,
        })
        self._assert_png_response(resp, "twombly_custom.png")

    def test_with_border(self) -> None:
        resp = self._post("/twombly", {
            "width": 400,
            "height": 300,
            "splats": 10,
            "border": True,
        })
        self._assert_png_response(resp, "twombly_border.png")


if __name__ == "__main__":
    unittest.main(verbosity=2)
