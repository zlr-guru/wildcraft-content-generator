
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
                You are a product content writer for Wildcraft, a performance-oriented outdoor lifestyle brand known for functional, durable, and stylish gear.
                Based on the provided product image(s), write a detailed, engaging, and brand-aligned product description for use on Wildcraft’s official product page.

                 Instructions for the Output:
                Your generated description must:
                Start with a punchy, branded intro

                - Start with a **dynamic and varied introduction**. Avoid repeating phrases like "Introducing the X Backpack".
                Use alternative openers that match the Wildcraft tone (e.g., “Engineered for the everyday explorer,” or “Crafted for comfort and resilience on the move.”)

               - Include visually inferred features from the image, such as:
               - Number and type of compartments/pockets
               - Fabric texture, color, or layering
               - Zippers, straps, handle design, soles, mesh panels, reflective details
               - Padding or ergonomic shape

                 Tone & Style Guide:
               - Wildcraft’s tone is confident, active, practical, and design-forward.
               - Use short, energetic sentences.
               - Highlight features + benefits (not just specs).
               - Avoid technical jargon or overly flowery language.
               - The description should feel both functional and aspirational, tailored for everyday adventurers.

                Call out functional and design features:
               - Storage capacity (estimated if not given)
               - Water-repellent/waterproof elements
               - Durability (e.g., reinforced stitching, YKK zippers)
               - Comfort (e.g., padded straps, breathable back panel)
               - Mention use cases
               - Commuting, trekking, city travel, monsoon utility, outdoor adventures
               - Finish with an aspirational but grounded closing line
                Example: “Elevate your adventures with the Evo 35 – your all-in-one travel partner!”

                **Focus strictly on the product do not suggest any matching accessories for the product.**
                Give a 2 -3 paragraph descrption not more than that focusing on all the aspects mentioned.
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
        base_prompt = f"""
        You are an intelligent product content parser for an e-commerce platform.

        Given one or more product images, analyze the visual details , extract the following structured fields in JSON format:

        - Key Feature (list of distinct single worded features or benefits)
        - Technology (zippers, tech-enabled design, special construction,Hypalite - for bags with room capacity less than 40 liters)
        - Material (e.g., Nylon, Polyester depict the correct material from the images provided.)
        - Gender (Capture the correct gender either Men, Women, Unisex from the image.)
        - Occasion (e.g., Travel, Outdoor, Work, Hiking)
        - Compartments (e.g., "2 main compartments, 1 front pocket")
        - Sleeve Type (Only if the product is apparel and sleeves are visible, e.g., "Full Sleeve", "Sleeveless")
        - Compartment Closure (e.g., Zipper, Buckle)
        - Imported or Manufactured or Marketed By (Default: "Wildcraft India")

        Respond as N/A for a feature if it is not eligible for the product.

        Respond ONLY with JSON.
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

        system_message = """
            You are a highly skilled background change assistant.  
            Your role is to modify or replace the background of images while strictly preserving the main subject’s integrity, details, and proportions.  
            Always ensure that the output looks natural, high-quality, and visually consistent with the subject.  
            Do not alter the subject’s appearance, angle, POV, clothing, or identity.  
            If the user provides creative background prompts, adapt them faithfully while maintaining photorealism and proper lighting.  
            Never remove, distort, or obscure the main subject.  
                    """

        full_prompt = system_message + prompt
        # Send to Gemini API
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=[full_prompt, img],
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


import gradio as gr

# Wrap functions with api_key input
def wrapper_generate_product_description(image1, image2, api_key):
    return generate_product_description(image1, image2, api_key)

def wrapper_generate_product_tags(image1, image2, api_key):
    return generate_product_tags(image1, image2, api_key)

def wrapper_generate_storyboard(image1, image2, pitch, num_scenes, style, language_name, language_code, api_key):
    return generate_storyboard_with_prompt(api_key, image1, image2, pitch, num_scenes, style, language_name, language_code)

def wrapper_generate_storyboard_images(storyboard, num_images, api_key):
    return generate_storyboard_images(storyboard, num_images=num_images, api_key=api_key)

def wrapper_change_background(api_key, image, bg_prompt):
    output, path = change_background_with_gemini(api_key, image, bg_prompt)
    return output

# import gradio as gr

# with gr.Blocks(title="WILDCRAFT PDP Content Generation") as interface:
#     gr.Markdown("## 🏕️ Wildcraft Product Content & Storyboard Generator")

#     api_key = gr.Textbox(label="Google API Key", type="password")

#     with gr.Tab("Product Content"):
#         with gr.Row():
#             image1 = gr.Image(type="filepath", label="Upload Product Image 1")
#             image2 = gr.Image(type="filepath", label="Upload Product Image 2")

#         with gr.Row():
#             generate_description = gr.Button("✨ Generate Product Description")
#             generate_tags_btn = gr.Button("🏷️ Generate Product Tags")

#         description_box = gr.Textbox(label="Generated Product Description")
#         tags_box = gr.Textbox(label="Generated Product Tags (JSON)")

#         generate_description.click(
#             fn=wrapper_generate_product_description,
#             inputs=[image1, image2, api_key],
#             outputs=description_box
#         )

#         generate_tags_btn.click(
#             fn=wrapper_generate_product_tags,
#             inputs=[image1, image2, api_key],
#             outputs=tags_box
#         )

#     with gr.Tab("Storyboard"):
#         pitch_input = gr.Textbox(label="Story Pitch", placeholder="Enter your storyboard idea...")
#         num_scenes_input = gr.Number(label="Number of Scenes", value=1, precision=0)
#         style_input = gr.Textbox(label="Style", placeholder="Cinematic, Minimalist, etc.")

#         generate_storyboard_btn = gr.Button("🎬 Generate Storyboard JSON")
#         storyboard_box = gr.Textbox(label="Generated Storyboard JSON")

#         generate_storyboard_btn.click(
#             fn=wrapper_generate_storyboard,
#             inputs=[image1, image2, pitch_input, num_scenes_input, style_input, api_key],
#             outputs=storyboard_box
#         )

#         with gr.Row():
#             num_images = gr.Number(label="Number of Images", value=1, precision=0)
#             generate_images_btn = gr.Button("🖼️ Generate Storyboard Images")

#         gallery = gr.Gallery(label="Generated Storyboard Images", columns=2, height="auto")

#         generate_images_btn.click(
#             fn=wrapper_generate_storyboard_images,
#             inputs=[storyboard_box, num_images, api_key],
#             outputs=gallery
#         )

#     with gr.Tab("Background Changer"):
#         input_img = gr.Image(type="filepath", label="Upload Product Image")
#         prompt_box = gr.Textbox(label="Background Change Prompt", placeholder="e.g., Add a Wildcraft store in the background")
#         generate_btn = gr.Button("🔄 Change Background")
#         output_img = gr.Image(label="Background Changed Image")

#         generate_btn.click(
#             fn=wrapper_change_background,
#             inputs=[api_key, input_img, prompt_box],
#             outputs=output_img
#         )


# if __name__ == "__main__":
#     interface.launch(debug=True)
