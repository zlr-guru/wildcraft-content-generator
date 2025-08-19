from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from vcraft import (
    generate_product_description,
    generate_product_tags,
    generate_storyboard_images,
    # generate_images_using_storyboard,
    generate_storyboard_with_prompt,
    change_background_with_gemini
)

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import traceback
import json

load_dotenv()

app = Flask(__name__)

CORS(app, 
     origins=["*"], 
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"])

def create_error_response(message, status_code=500):
    """Helper function to create error responses."""
    response = jsonify({"error": message})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response, status_code

def create_success_response(data):
    """Helper function to create success responses."""
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

@app.route("/generate_product_tags", methods=["OPTIONS"])
@app.route("/generate_product_description", methods=["OPTIONS"])
@app.route("/generate_storyboard", methods=["OPTIONS"])
@app.route("/list-images", methods=["OPTIONS"])
def handle_options():
    """Handle preflight OPTIONS requests."""
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

@app.route("/generate_storyboard", methods=["POST"])
def api_generate_storyboard():
    try:
        data = request.json
        required_fields = ["google_api_key", "image1_path", "image2_path", "pitch", "num_scenes", "style", "language_name", "language_code"]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return create_error_response(f"Missing required fields: {missing_fields}", 400)

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
        
        return create_success_response({"storyboard": result})
        
    except Exception as e:
        print(f"Error in generate_storyboard: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return create_error_response(f"Error: {str(e)}", 500)

@app.route("/generate_product_tags", methods=["POST"])
def api_generate_product_tags():
    try:
        data = request.json
        required_fields = ["image1_path", "image2_path", "google_api_key"]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return create_error_response(f"Missing required fields: {missing_fields}", 400)

        result = generate_product_tags(
            data["image1_path"],
            data["image2_path"],
            data["google_api_key"]
        )
        
        return create_success_response({"tags": result})
        
    except Exception as e:
        print(f"Error in generate_product_tags: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return create_error_response(f"Error: {str(e)}", 500)

@app.route("/generate_product_description", methods=["POST"])
def api_generate_product_description():
    try:
        data = request.json
        required_fields = ["image1_path", "image2_path", "google_api_key"]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return create_error_response(f"Missing required fields: {missing_fields}", 400)

        result = generate_product_description(
            data["image1_path"],
            data["image2_path"],
            data["google_api_key"]
        )
        
        return create_success_response({"description": result})
        
    except Exception as e:
        print(f"Error in generate_product_description: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return create_error_response(f"Error: {str(e)}", 500)

@app.route("/health", methods=["GET"])
def health_check():
    """Simple health check endpoint."""
    return create_success_response({"status": "healthy", "message": "Wildcraft API is running"})


@app.route("/upload-image", methods=["POST"])
def upload_image():
    """Upload an image file and return the saved path."""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Create uploads directory if it doesn't exist
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save the file with a unique name
        import time
        timestamp = int(time.time() * 1000)
        filename = f"upload_{timestamp}_{file.filename}"
        file_path = os.path.join(upload_dir, filename)
        
        file.save(file_path)
        
        return jsonify({
            "status": "success",
            "filename": filename,
            "file_path": file_path
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/change_background", methods=["POST"])
def api_change_background():
    try:
        data = request.json
        required_fields = ["image_path", "prompt", "google_api_key"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": f"Missing required fields. Required: {required_fields}"}), 400

        # Call the function and get both image and path
        output_image, output_path = change_background_with_gemini(
            data["google_api_key"],
            data["image_path"],
            data["prompt"]
        )
        
        if output_image and output_path:
            # Extract just the filename from the full path
            filename = os.path.basename(output_path)
            return jsonify({
                "status": "success", 
                "message": "Background changed successfully",
                "saved_path": filename  # This is what the frontend expects!
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "Background change failed",
                "error": output_path if isinstance(output_path, str) and output_path.startswith("Error:") else "Unknown error"
            }), 500
            
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

@app.route("/list-images", methods=["GET"])
def list_images():
    """List all generated images."""
    try:
        image_dir = "bg_change_images"
        if not os.path.exists(image_dir):
            return jsonify({"images": []})
        
        images = []
        for filename in os.listdir(image_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                images.append({
                    "filename": filename,
                    "url": f"/image-file/{filename}",
                    "full_url": f"http://localhost:5000/image-file/{filename}"
                })
        
        response = jsonify({"images": images})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        return response
    except Exception as e:
        response = jsonify({"error": str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        return response, 500

@app.route("/images/<filename>")
def serve_image(filename):
    """Serve generated images from the bg_change_images folder."""
    try:
        image_dir = "bg_change_images"
        image_path = os.path.join(image_dir, filename)
        
        if os.path.exists(image_path):
            # Return an HTML page with the image and a proper title
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Generated Product Background</title>
                <style>
                    body {{
                        margin: 0;
                        padding: 20px;
                        background-color: #f5f5f5;
                        font-family: Arial, sans-serif;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        min-height: 100vh;
                    }}
                    .container {{
                        background: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        max-width: 90vw;
                        max-height: 90vh;
                        overflow: auto;
                    }}
                    h1 {{
                        color: #333;
                        margin-bottom: 20px;
                        text-align: center;
                    }}
                    img {{
                        max-width: 100%;
                        height: auto;
                        border-radius: 4px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    }}
                    .info {{
                        margin-top: 15px;
                        text-align: center;
                        color: #666;
                        font-size: 14px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Generated Product Background</h1>
                    <img src="/api/image-file/{filename}" alt="Generated product background" />
                    <div class="info">
                        <p>Generated using AI-powered background replacement</p>
                        <p>Filename: {filename}</p>
                    </div>
                </div>
            </body>
            </html>
            """
            return html_content, 200, {'Content-Type': 'text/html'}
        else:
            return create_error_response(f"Image {filename} not found", 404)
            
    except Exception as e:
        return create_error_response(f"Error serving image: {str(e)}")

@app.route("/image-file/<filename>")
@app.route("/image-file/<filename>")
def serve_image_file(filename):
    """Serve the actual image file for frontend display."""
    try:
        print(f"Serving image file: {filename}")
        image_dir = "bg_change_images"
        image_path = os.path.join(image_dir, filename)
        print(f"Looking for image at: {image_path}")
        
        if os.path.exists(image_path):
            print(f"Image found in bg_change_images, serving: {filename}")
            return send_from_directory(image_dir, filename)
        
        # Try generated_images folder if not found
        image_dir = "generated_images"
        image_path = os.path.join(image_dir, filename)
        print(f"Looking for image at: {image_path}")
        
        if os.path.exists(image_path):
            print(f"Image found in generated_images, serving: {filename}")
            return send_from_directory(image_dir, filename)
        else:
            print(f"Image not found in either folder: {filename}")
            return create_error_response(f"Image file {filename} not found", 404)
            
    except Exception as e:
        print(f"Error serving image file: {e}")
        return create_error_response(f"Error serving image file: {str(e)}")


@app.route("/generate_storyboard_image", methods=["POST"])
def generate_image_endpoint():
    data = request.json
    storyboard = data.get("storyboard")
    num_images = data.get("num_images", 1)
    api_key = data.get("api_key")  # API key can be passed in request

    if not storyboard:
        return jsonify({"error": "Storyboard is required"}), 400

    try:
        file_paths = generate_storyboard_images(storyboard, num_images, api_key)
        return jsonify({"message": "Images generated successfully", "files": file_paths})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)