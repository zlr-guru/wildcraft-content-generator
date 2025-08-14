
import google.genai as genai
from google.genai import types
import os
from dotenv import load_dotenv

# load_dotenv()

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# print("Using credentials from:", os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))

# import vertexai

# PROJECT_ID = os.getenv("PROJECT_ID")
# LOCATION = os.getenv("LOCATION")
# vertexai.init(project=PROJECT_ID, location=LOCATION)

import base64
import io
import json     
from typing import Optional, Tuple, Union, List
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image as im
# import gradio as gr
from typer import prompt
from vertexai.preview.vision_models import (
    ImageGenerationModel,
)
from vertexai.generative_models import GenerativeModel
from vertexai.generative_models import Image as image_gen

from google import genai
from google.genai import types
from PIL import Image as PILImage
import io
from io import BytesIO

def resize_image(image_path, max_size=(1024, 1024)):
    """Resize image for faster processing."""
    img = PILImage.open(image_path)
    img.thumbnail(max_size)
    byte_arr = io.BytesIO()
    img.save(byte_arr, format=img.format)
    return byte_arr.getvalue()

def image_to_bytes(image: PILImage.Image):
    """Convert PIL Image to bytes."""
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format="PNG")
    return img_byte_arr.getvalue()
    
import google.generativeai as genai
import base64
from PIL import Image
import io

def image_to_base64(image_path):
    """Convert image to base64 string."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def generate_product_description(image1_path, image2_path, google_api_key):
    """Generates a product description for an image using Gemini with user-provided API key."""
    try:
        # Configure Gemini with user API key
        genai.configure(api_key=google_api_key)

        # Load Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Convert images to base64
        img1_b64 = image_to_base64(image1_path)
        img2_b64 = image_to_base64(image2_path)

        # Prompt
        base_prompt = """
        You are a product content writer for Wildcraft, a brand known for outdoor gear and travel accessories.
        Write a detailed, SEO-friendly product description for the provided images.
        Make sure it is engaging, informative, and professional.
        """

        # Generate
        response = model.generate_content([
            {"mime_type": "image/jpeg", "data": img1_b64},
            {"mime_type": "image/jpeg", "data": img2_b64},
            base_prompt
        ])
        return response.text.strip()

    except Exception as e:
        print(f"Error generating product description: {e}")
        return "Error generating product description."


def generate_product_tags(image1_path, image2_path, google_api_key):
    """Generates product tags in JSON format using Gemini with user-provided API key."""
    try:
        # Configure Gemini with user API key
        genai.configure(api_key=google_api_key)

        # Load Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Convert images to base64
        img1_b64 = image_to_base64(image1_path)
        img2_b64 = image_to_base64(image2_path)

        # Prompt
        base_prompt = """
        You are an intelligent product content parser for an e-commerce platform.
        Look at the provided product images and generate JSON tags containing:
        {
          "category": "",
          "color": "",
          "material": "",
          "activity": "",
          "gender": "",
          "keywords": []
        }
        Only return valid JSON.
        """

        # Generate
        response = model.generate_content([
            {"mime_type": "image/jpeg", "data": img1_b64},
            {"mime_type": "image/jpeg", "data": img2_b64},
            base_prompt
        ])
        return response.text.strip()

    except Exception as e:
        print(f"Error generating product tags: {e}")
        return "Error generating product tags."


def generate_storyboard_with_prompt(google_api_key, image1_path, image2_path, pitch, num_scenes, style, language_name, language_code):
    """
    Generates a storyboard JSON based on pitch, style, and two product images.
    Requires the user to provide their Google API key.
    """
    # Configure API key (user-provided)
    genai.configure(api_key=google_api_key)

    # Prepare image bytes
    image1_bytes = resize_image(image1_path)
    image2_bytes = resize_image(image2_path)

    # Build scenario prompt
    prompt = f"""
You are tasked with generating a creative scenario for a short marketing storyboard for a product.
You will be given:
- A short user-provided story pitch.
- Two product images (assume you can see them).
- A style preference.

<pitch>
{pitch}
</pitch>

**Instructions:**
1. Generate a scenario in English that matches the pitch and product images.
   - No children in the story.
   - The product must be a key visual element in the story.

2. Divide the scenario into exactly 1 scene.

3. Select the most fitting Music Genre from:
- Alternative & Punk
- Ambient
- Children's
- Cinematic
- Classical
- Country & Folk
- Dance & Electronic
- Hip-Hop & Rap
- Holiday
- Jazz & Blues
- Pop
- R&B & Soul
- Reggae
- Rock

4. Select the Mood from:
- Angry
- Bright
- Calm
- Dark
- Dramatic
- Funky
- Happy
- Inspirational
- Romantic
- Sad

5. Generate a short description of the background music (in English only). No story references, no known artist/song names.

6. Provide a JSON object with:
- "scenario": Full scenario text in English.
- "scenes": A list of scene objects each with:
   - "title": Scene title in English
   - "description": Scene description in English
- "genre": Music genre.
- "mood": Mood.
- "music": Music description in English.
- "language": {{ "name": "English", "code": "en" }}
- "characters": List of character objects with:
   - "name"
   - "description": [General appearance in English, Clothing & textures, Voice description]
- "settings": List of setting objects with:
   - "name"
   - "description": [General environment in English, Atmosphere details, Sensory description]

**IMPORTANT:** Output only valid JSON. Do not include any extra text, explanations, or markdown.
"""

    # Call Gemini API with text + images
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(
        [
            {"mime_type": "image/jpeg", "data": image1_bytes},
            {"mime_type": "image/jpeg", "data": image2_bytes},
            prompt
        ]
    )

    return response.text.strip()


def init_client(api_key=None):
    from google import genai
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
    return genai.Client()

def generate_storyboard_images(storyboard, num_images=1, api_key=None, save_dir="generated_images"):
    """
    Generate images using Google Imagen API.

    Args:
        storyboard (str): Storyboard description to generate images from.
        num_images (int): Number of images to generate.
        api_key (str, optional): Google API key. If not provided, uses env var.
        save_dir (str): Directory to save images.

    Returns:
        list: List of file paths for saved images.
    """
    # Ensure save directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Initialize client
    client = init_client(api_key)

    base_prompt = f"""
        Create a highly realistic, cinematic lifestyle photograph based on the following storyboard description:
        {storyboard}.
        The image should depict natural lighting, real human appearances, authentic clothing textures, and realistic backgrounds.
        Avoid any cartoon, illustration, or animated styles.
        Ensure the photo has the depth, detail, and sharpness of a high-resolution DSLR photograph, resembling an actual scene from real life.

        Create only a single image. Do not create a collage.
        """

    if isinstance(base_prompt, dict):
        prompt = json.dumps(base_prompt, indent=2)
    else:
        prompt = str(base_prompt)
    
    # Request image generation
    response = client.models.generate_images(
        model="imagen-4.0-generate-preview-06-06",
        prompt=prompt,
        config=types.GenerateImagesConfig(number_of_images=num_images)
    )

    saved_files = []
    for idx, generated_image in enumerate(response.generated_images):
        file_path = os.path.join(save_dir, f"storyboard_{idx+1}.png")
        with open(file_path, "wb") as f:
            f.write(generated_image.image.image_bytes)
        saved_files.append(file_path)

    return saved_files

def change_background_with_gemini(google_api_key, image_path, prompt):
    try:
        import google.genai as genai
        # Ensure output folder exists
        output_dir = "bg_change_images"
        os.makedirs(output_dir, exist_ok=True)

        # Output file path
        output_filename = f"bg_changed_{int(os.times()[4])}.png"
        output_path = os.path.join(output_dir, output_filename)

        # Read image from disk
        img = PILImage.open(image_path)

        # Initialize Gemini client
        client = genai.Client(api_key=google_api_key)

        # Send to Gemini API
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=[prompt, img],
            config=genai.types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )

        image_output = None

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_output = PILImage.open(BytesIO(part.inline_data.data))
                image_output.save(output_path)  # Save to output folder

        return image_output, output_path

    except Exception as e:
        return None, f"Error: {e}"



# import gradio as gr


# with gr.Blocks(title="WILDCRAFT PDP Content Generation") as interface:
#     gr.Markdown("## Upload Two images to generate Description and Tags for WildCraft Products")

#     with gr.Row():
#         image1 = gr.Image(type="pil", label="Image 1")
#         image2 = gr.Image(type="pil", label="Image 2")

#     with gr.Row():
#         description_box = gr.Textbox(
#             label="Generated Product Description"
#         )
#         tags_box = gr.Textbox(
#             label="Generated Product Tags"
#         )


#     with gr.Row():
#         pitch_input = gr.Textbox(label="Story Pitch", placeholder="Enter your storyboard idea...")
#         num_scenes_input = gr.Number(label="Number of Scenes", value=4, precision=0)
#         style_input = gr.Textbox(label="Style", placeholder="Cinematic, Minimalist, etc.")
#         language_name = gr.Textbox(label="Language Name", value="English")
#         language_code = gr.Textbox(label="Language Code", value="en")



#     with gr.Row():
#         generate_description = gr.Button("Generate Product Description")
#         generate_tags_btn = gr.Button("Generate Product Tags")
#         generate_storyboard_btn = gr.Button("Generate Storyboard")


#     generate_description.click(
#         fn=generate_product_description,
#         inputs=[image1, image2],
#         outputs=description_box
#     )

#     generate_tags_btn.click(
#         fn=generate_product_tags,
#         inputs=[image1, image2],
#         outputs=tags_box
#     )

#     with gr.Row():
#         storyboard_box = gr.Textbox(
#             label="Generated Storyboard"
#         )

#     generate_storyboard_btn.click(
#         fn=generate_storyboard_with_prompt,
#         inputs=[image1, image2, pitch_input, num_scenes_input, style_input, language_name, language_code],
#         outputs=storyboard_box
#     )

#     with gr.Row():
#         generate_images_btn = gr.Button("Generate Images from Storyboard")
#     gallery = gr.Gallery(label="Generated Storyboard Images",columns=2 , height="auto")

#     generate_images_btn.click(
#         fn=generate_images_using_storyboard,
#         inputs=storyboard_box,
#         outputs=gallery
#     )

#     with gr.Row():
#         input_img = gr.Image(type="pil", label="Upload Product Image")
#         prompt_box = gr.Textbox(label="Background Change Prompt", placeholder="e.g., Add a Wildcraft store in the background")

#     with gr.Row():
#         generate_btn = gr.Button("Generate Image")

#     with gr.Row():
#         output_img = gr.Image(label="Generated Image")
#         # output_text = gr.Textbox(label="Gemini's Response", lines=3)

#     generate_btn.click(
#         fn=change_background_with_gemini,
#         inputs=[input_img, prompt_box],
#         outputs=output_img
#     )

# if __name__ == "__main__":
#     interface.launch(debug=True)


