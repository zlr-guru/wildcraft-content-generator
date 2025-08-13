
import google.genai as genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

print("Using credentials from:", os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))

import vertexai

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")
vertexai.init(project=PROJECT_ID, location=LOCATION)



import base64
import io
from typing import Optional, Tuple, Union, List
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image as im
# import gradio as gr
from vertexai.preview.vision_models import (
    Image,
    ImageGenerationModel,
    StyleReferenceImage,
    SubjectReferenceImage,
)
from vertexai.generative_models import GenerativeModel, Part
from vertexai.generative_models import Image as image_gen


def pil_to_image(image: im) -> str:
    """Converts a PIL Image object to a base64 string."""
    with io.BytesIO() as buffer:
        image.save(buffer, format="JPEG")
        img_bytes = buffer.getvalue()
    return img_bytes

def resize_image(image_input, base_width=300):
    """
    Resizes an image to the specified base width while maintaining aspect ratio.
    Accepts either a file path (str) or a PIL Image object.
    """
    # Convert file path to PIL Image if needed
    if isinstance(image_input, str):
        image_input = im.open(image_input)

    # Calculate new height maintaining aspect ratio
    wpercent = (base_width / float(image_input.size[0]))
    hsize = int((float(image_input.size[1]) * float(wpercent)))
    
    # Resize image
    img = image_input.resize((base_width, hsize), im.LANCZOS)
    return img

def image_to_bytes(image: im) -> str:
    """Converts a PIL object to a base64 string."""
    with io.BytesIO() as buffer:
        image.save(buffer, format="JPEG")
        img_bytes = buffer.getvalue()
    return img_bytes

def pil_to_file(image: im, file_path: str) -> str:
    """
    Saves a PIL Image object to the specified file path.

    Args:
        image: The PIL Image object to save.
        file_path: The file path where the image will be saved.

    Returns:
        The file path where the image was saved.
    """
    try:
        image.save(file_path, format="JPEG")  # Change format if needed (e.g., PNG)
        return file_path
    except Exception as e:
        print(f"Error saving image to file: {e}")
        return None



def generate_product_description(image1_path,image2_path):
    """Generates a product description for an image using Gemini."""
    # try:
    #     image = resize_image(image_path)
    #     # new_image_path = pil_to_file(image,"/content/sample_data/image.jpeg")
    #     image = image_gen.from_bytes(image_to_bytes(image) )# Convert to Vertex AI Image object
    #     # image = image_to_base64(image)
    #     # image = Image(pil_to_image(image))
    try:
        image1 = resize_image(image1_path)
        image2 = resize_image(image2_path)
        image1 = image_gen.from_bytes(image_to_bytes(image1))
        image2 = image_gen.from_bytes(image_to_bytes(image2))

        model = GenerativeModel("gemini-2.5-flash")  # Or a suitable Gemini model

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

        prompt = [image1,image2,base_prompt]

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print(f"An error occurred generating product description: {e}")
        return "Error generating product description."

import json

def generate_product_tags(image1_path,image2_path):
    model = GenerativeModel("gemini-2.5-flash")

    image1 = resize_image(image1_path)
    image2 = resize_image(image2_path)
    image1 = image_gen.from_bytes(image_to_bytes(image1))
    image2 = image_gen.from_bytes(image_to_bytes(image2))

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
    prompt = [image1,image2,base_prompt]
    response = model.generate_content(prompt)
    return response.text
    # try:
    #     json_start = response.text.find('{')
    #     parsed_json = json.loads(response.text[json_start:])
    #     return json.dumps(parsed_json, indent=2)
    # except Exception as e:
    #     return {"error": "Could not parse response", "raw_output": response.text}


def get_scenario_prompt_with_images(pitch: str, num_scenes: int, style: str, language: dict) -> str:
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
1. Generate a scenario in {language['name']} that matches the pitch and product images.
   - No children in the story.
   - The product must be a key visual element in the story.

2. Divide the scenario into exactly {num_scenes} scenes.

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
- "scenario": Full scenario text in {language['name']}.
- "scenes": A list of scene objects each with:
   - "title": Scene title in {language['name']}
   - "description": Scene description in {language['name']}
- "genre": Music genre.
- "mood": Mood.
- "music": Music description in English.
- "language": {{ "name": "{language['name']}", "code": "{language['code']}" }}
- "characters": List of character objects with:
   - "name"
   - "description": [General appearance in {language['name']}, Clothing & textures, Voice description]
- "settings": List of setting objects with:
   - "name"
   - "description": [General environment in {language['name']}, Atmosphere details, Sensory description]

**IMPORTANT:** Output only valid JSON. Do not include any extra text, explanations, or markdown.
"""
    return prompt


def generate_storyboard(image1_path, image2_path, pitch, num_scenes, style, language_name, language_code):
    try:
        image1 = image_gen.from_bytes(image_to_bytes(resize_image(image1_path)))
        image2 = image_gen.from_bytes(image_to_bytes(resize_image(image2_path)))

        language = {"name": language_name, "code": language_code}
        scenario_prompt = get_scenario_prompt_with_images(pitch, int(num_scenes), style, language)

        model = GenerativeModel("gemini-2.5-flash")
        prompt_parts = [image1, image2, scenario_prompt]
        response = model.generate_content(prompt_parts)

        return response.text.strip()
    except Exception as e:
        return f"Error generating storyboard: {e}"



from vertexai.preview.vision_models import ImageGenerationModel

from google.auth import credentials
from vertexai.preview.vision_models import ImageGenerationModel

# Initialize with your project and location
generation_model = ImageGenerationModel.from_pretrained("imagegeneration@002")
IMAGEN_MODEL = "imagen-3.0-generate-002"
generation_model = ImageGenerationModel.from_pretrained(IMAGEN_MODEL)


import base64
import logging
from io import BytesIO
import uuid

# Third-party imports
from google.genai import types
from PIL import Image as PILImage, ImageOps

def generate_images_using_storyboard(storyboard, product_type=None):
    """Generate images for each scene in the storyboard using the generation_model."""
    try:
        generated_images = []

        gen_prompt = f"""
        Create a highly realistic, cinematic lifestyle photograph based on the following storyboard description:
        {storyboard}.
        The image should depict natural lighting, real human appearances, authentic clothing textures, and realistic backgrounds.
        Avoid any cartoon, illustration, or animated styles.
        Ensure the photo has the depth, detail, and sharpness of a high-resolution DSLR photograph, resembling an actual scene from real life.

        Create only a single image. Do not create a collage.
        """

        print(f"Generating images with prompt: {gen_prompt}")

        # Call image generation model
        images = generation_model.generate_images(
            prompt=gen_prompt,
            number_of_images=2,
            add_watermark=False
        )

        for image in images:
            pil_image = image._pil_image  # direct method from GeneratedImage

            if pil_image.mode != 'RGBA':
                pil_image = pil_image.convert('RGBA')

            generated_images.append(pil_image)

        return generated_images

    except Exception as e:
        print(f"Error generating images: {e}")
        return []

def change_background_with_gemini(input_image, prompt, output_path="output_image.png"):
    """
    Uses Gemini image generation to change the background of an image while keeping the main object intact.
    """
    try:
        # Initialize Gemini client
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

        # Send to Gemini API
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=[prompt, input_image],  # Gradio already passes a PIL Image here
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )

        text_output = None
        image_output = None

        for part in response.candidates[0].content.parts:
            if part.text is not None:
                text_output = part.text
            elif part.inline_data is not None:
                image_output = PILImage.open(BytesIO(part.inline_data.data))
                image_output.save(output_path)

        return image_output   #, text_output

    except Exception as e:
        print(f"Error changing background: {e}")
        return None, f"Error: {e}"



import gradio as gr


with gr.Blocks(title="WILDCRAFT PDP Content Generation") as interface:
    gr.Markdown("## Upload Two images to generate Description and Tags for WildCraft Products")

    with gr.Row():
        image1 = gr.Image(type="pil", label="Image 1")
        image2 = gr.Image(type="pil", label="Image 2")

    with gr.Row():
        description_box = gr.Textbox(
            label="Generated Product Description"
        )
        tags_box = gr.Textbox(
            label="Generated Product Tags"
        )


    with gr.Row():
        pitch_input = gr.Textbox(label="Story Pitch", placeholder="Enter your storyboard idea...")
        num_scenes_input = gr.Number(label="Number of Scenes", value=4, precision=0)
        style_input = gr.Textbox(label="Style", placeholder="Cinematic, Minimalist, etc.")
        language_name = gr.Textbox(label="Language Name", value="English")
        language_code = gr.Textbox(label="Language Code", value="en")



    with gr.Row():
        generate_description = gr.Button("Generate Product Description")
        generate_tags_btn = gr.Button("Generate Product Tags")
        generate_storyboard_btn = gr.Button("Generate Storyboard")


    generate_description.click(
        fn=generate_product_description,
        inputs=[image1, image2],
        outputs=description_box
    )

    generate_tags_btn.click(
        fn=generate_product_tags,
        inputs=[image1, image2],
        outputs=tags_box
    )

    with gr.Row():
        storyboard_box = gr.Textbox(
            label="Generated Storyboard"
        )

    generate_storyboard_btn.click(
        fn=generate_storyboard,
        inputs=[image1, image2, pitch_input, num_scenes_input, style_input, language_name, language_code],
        outputs=storyboard_box
    )

    with gr.Row():
        generate_images_btn = gr.Button("Generate Images from Storyboard")
    gallery = gr.Gallery(label="Generated Storyboard Images",columns=2 , height="auto")

    generate_images_btn.click(
        fn=generate_images_using_storyboard,
        inputs=storyboard_box,
        outputs=gallery
    )

    with gr.Row():
        input_img = gr.Image(type="pil", label="Upload Product Image")
        prompt_box = gr.Textbox(label="Background Change Prompt", placeholder="e.g., Add a Wildcraft store in the background")

    with gr.Row():
        generate_btn = gr.Button("Generate Image")

    with gr.Row():
        output_img = gr.Image(label="Generated Image")
        # output_text = gr.Textbox(label="Gemini's Response", lines=3)

    generate_btn.click(
        fn=change_background_with_gemini,
        inputs=[input_img, prompt_box],
        outputs=output_img
    )

if __name__ == "__main__":
    interface.launch(debug=True)


