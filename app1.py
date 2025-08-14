from flask import Flask, request, jsonify
from vcraft import (
    generate_product_description,
    generate_product_tags,
    generate_images_using_storyboard,
    generate_storyboard_with_prompt,
    change_background_with_gemini
)

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import traceback

# Import your function

load_dotenv()

app = Flask(__name__)


@app.route("/generate_product_description", methods=["POST"])
def api_generate_product_description():
    try:
        data = request.json
        required_fields = ["image1_path", "image2_path", "google_api_key"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": f"Missing required fields. Required: {required_fields}"}), 400

        result = generate_product_description(
            data["image1_path"],
            data["image2_path"],
            data["google_api_key"]
        )
        return jsonify({"description": result})
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


@app.route("/generate_product_tags", methods=["POST"])
def api_generate_product_tags():
    try:
        data = request.json
        required_fields = ["image1_path", "image2_path", "google_api_key"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": f"Missing required fields. Required: {required_fields}"}), 400

        result = generate_product_tags(
            data["image1_path"],
            data["image2_path"],
            data["google_api_key"]
        )
        return jsonify({"tags": result})
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500
    

@app.route("/generate_storyboard", methods=["POST"])
def api_generate_storyboard():
    try:
        data = request.json
        required_fields = ["google_api_key", "image1_path", "image2_path", "pitch", "num_scenes", "style", "language_name", "language_code"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": f"Missing required fields. Required: {required_fields}"}), 400

        language_name = data.get("language_name", "English")
        language_code = data.get("language_code", "en")
        num_scenes = data.get("num_scenes", 1)

        result = generate_storyboard_with_prompt(
            data["google_api_key"],
            data["image1_path"],
            data["image2_path"],
            data["pitch"],
            num_scenes,
            data["style"],
            language_name,
            language_code
        )
        return jsonify({"storyboard": result})
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


@app.route("/get_scenario_prompt_with_images", methods=["POST"])
def api_get_scenario_prompt_with_images():
    try:
        data = request.json
        required_fields = ["pitch", "num_scenes", "style", "language"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": f"Missing required fields. Required: {required_fields}"}), 400

        language = data.get("language", "English")
        num_scenes = data.get("num_scenes", 1)

        result = generate_images_using_storyboard(
            data["pitch"],
            num_scenes,
            data["style"],
            language
        )
        return jsonify({"prompt": result})
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

@app.route("/change_background", methods=["POST"])
def api_change_background():
    try:
        data = request.json
        required_fields = ["google_api_key", "image_path", "prompt"]
        if not all(field in data for field in required_fields):
            return jsonify({
                "error": f"Missing required fields. Required: {required_fields}"
            }), 400

        # Updated to unpack two values
        image_output, saved_path = change_background_with_gemini(
            data["google_api_key"],
            data["image_path"],
            data["prompt"]
        )

        if image_output:
            return jsonify({
                "status": "success",
                "message": "Background changed successfully",
                "saved_path": saved_path
            })
        else:
            return jsonify({
                "status": "error",
                "message": saved_path  # here saved_path will contain error message
            }), 500

    except Exception as e:
        return jsonify({
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
