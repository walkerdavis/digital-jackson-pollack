#!/usr/bin/env python3
"""Flask server exposing generative art as downloadable HTTP endpoints."""

import os
import tempfile
import uuid
from pathlib import Path

from flask import Flask, Response, after_this_request, jsonify, request, send_file
from flask_cors import CORS

from src.canvas import cy_twombly, jackson_pollack
from src.image import add_border_to_image, canvas_to_image

DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 482

TEMP_OUTPUT_DIR = Path(tempfile.gettempdir()) / "pollack-api"
TEMP_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
CORS(app)


def _request_data() -> dict:
    return request.get_json(silent=True) or {}


def _make_output_path(prefix: str) -> Path:
    return TEMP_OUTPUT_DIR / f"{prefix}_{uuid.uuid4().hex}.png"


def _download_response(output_path: Path, download_name: str) -> Response:
    @after_this_request
    def _cleanup(response: Response) -> Response:
        try:
            output_path.unlink(missing_ok=True)
        except OSError:
            pass
        return response

    return send_file(
        output_path,
        mimetype="image/png",
        as_attachment=True,
        download_name=download_name,
        conditional=False,
    )


def _generate_pollack_image(
    width, height, num_colors, num_splats, num_layers, alpha, add_border
):
    if num_layers > 1 and alpha == 255:
        alpha = 200

    canvas, layer_canvas = jackson_pollack(
        width, height, num_colors, num_splats, num_layers
    )
    image = canvas_to_image(
        canvas=canvas,
        alpha=alpha,
        layer_canvas=layer_canvas if num_layers > 1 else None,
    )

    if add_border:
        add_border_to_image(image)

    return image


def _generate_twombly_image(width, height, num_colors, num_splats, add_border):
    canvas = cy_twombly(width, height, num_colors, num_splats)
    image = canvas_to_image(canvas=canvas)

    if add_border:
        add_border_to_image(image)

    return image


@app.get("/healthz")
def healthz() -> Response:
    return jsonify({"status": "ok"}), 200


@app.get("/")
def index() -> Response:
    return jsonify(
        {
            "status": "ok",
            "endpoints": [
                "/healthz",
                "/pollack",
                "/twombly",
            ],
            "method": "POST for generation endpoints",
        }
    ), 200


@app.route("/pollack", methods=["POST"])
def pollack_endpoint() -> Response:
    data = _request_data()

    try:
        image = _generate_pollack_image(
            width=data.get("width", DEFAULT_WIDTH),
            height=data.get("height", DEFAULT_HEIGHT),
            num_colors=data.get("colors", 8),
            num_splats=data.get("splats", 2000),
            num_layers=data.get("layers", 1),
            alpha=data.get("alpha", 255),
            add_border=data.get("border", False),
        )
        output_path = _make_output_path("pollack")
        image.save(str(output_path), "PNG")
        return _download_response(output_path, "pollack.png")
    except Exception as exc:
        return jsonify({"error": f"Unexpected error: {exc}"}), 500


@app.route("/twombly", methods=["POST"])
def twombly_endpoint() -> Response:
    data = _request_data()

    try:
        image = _generate_twombly_image(
            width=data.get("width", DEFAULT_WIDTH),
            height=data.get("height", DEFAULT_HEIGHT),
            num_colors=data.get("colors", 8),
            num_splats=data.get("splats", 20),
            add_border=data.get("border", False),
        )
        output_path = _make_output_path("twombly")
        image.save(str(output_path), "PNG")
        return _download_response(output_path, "twombly.png")
    except Exception as exc:
        return jsonify({"error": f"Unexpected error: {exc}"}), 500


if __name__ == "__main__":
    TEMP_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5001")), debug=False)
