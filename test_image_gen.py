from xmlrpc import client
from PIL import Image

storyboard_text =  {'storyboard': '```json\n{\n  "scenario": "Alex, a young urban explorer, navigates the bustling heart of a city square with an effortless cool. The sleek, dark green backpack is a natural extension of their confident stride, its durable fabric catching the glint of the afternoon sun. With a quick, intuitive glance at their phone for directions, Alex looks up, a subtle smile playing on their lips, ready to embrace the city\'s hidden gems. The backpack\'s comfort and stylish design are evident as they weave through the vibrant crowd, embodying the spirit of an urban adventure.",\n  "scenes": [\n    {\n      "title": "Urban Explorer\'s Flow",\n      "description": "A young adult, Alex, moves confidently through a sun-drenched, bustling city square. Their dark green backpack sits comfortably on their back, its modern design complementing their casual yet stylish urban attire. Alex briefly consults their phone for directions, then looks up with an air of anticipation and a relaxed smile, ready to continue exploring. The scene emphasizes the backpack\'s seamless integration into their active, urban lifestyle, highlighting its comfort and aesthetic appeal amidst the vibrant city backdrop."\n    }\n  ],\n  "genre": "Pop",\n  "mood": "Bright",\n  "music": "An upbeat, rhythmic track featuring a driving synth bassline, crisp percussive accents, and an uplifting, melodic synth lead that evokes a sense of optimistic discovery.",\n  "language": {\n    "name": "English",\n    "code": "en"\n  },\n  "characters": [\n    {\n      "name": "Alex",\n      "description": [\n        "Young adult, mid-20s to early 30s, exuding an air of quiet confidence and curiosity.",\n        "Dressed in a muted, stylish bomber jacket over a simple t-shirt, dark tailored jeans, and modern, comfortable sneakers. The dark green backpack is a prominent accessory, worn casually.",\n        "Voice is not heard, but their posture and facial expressions suggest a calm and self-assured demeanor."\n      ]\n    }\n  ],\n  "settings": [\n    {\n      "name": "Bustling City Square",\n      "description": [\n        "A vibrant, sun-drenched open-air city square, characterized by a mix of modern glass buildings and classic stone architecture.",\n        "The atmosphere is energetic and lively, filled with the soft hum of conversation, the distant sounds of traffic, and occasional street musician melodies. Sunlight casts long shadows and highlights textures.",\n        "Sensory details include the feeling of a light breeze, the faint scent of street food, and the visual tapestry of diverse people moving through the space."\n      ]\n    }\n  ]\n}\n```'}

import requests

url = "http://127.0.0.1:5000/generate_storyboard_image"
payload = {
    "storyboard": storyboard_text,
    "num_images": 1,
    "api_key": "api_key"  # optional if already set in env
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
try:
    print("Response JSON:", response.json())
except Exception:
    print("Raw Response:", response.text)


# # Example storyboard
# # Call function
# images = generate_images_using_storyboard(storyboard_text)

# print(f"Generated {len(images)} images")

# # Save them to disk
# for idx, img in enumerate(images):
#     img.save(f"generated_image_{idx+1}.png")
#     print(f"Saved generated_image_{idx+1}.png")


# import requests

# # Flask API URL
# url = "http://127.0.0.1:5000/change_background"

# story = {'storyboard': '```json\n{\n  "scenario": "Ava, a young architect, is on a self-guided tour of a modern art district. She pauses, pulls out her camera from her Wildcraft Evo 35 backpack, resting on a concrete bench, and frames a shot of a vibrant mural. The city\'s pulse vibrates around her, a blend of traffic, street performers, and distant chatter. She smiles, appreciating the unexpected beauty in the urban landscape. She zips her backpack shut, puts it on, and continues her adventure.",\n  "scenes": [\n    {\n      "title": "Urban Canvas",\n      "description": "Ava finds inspiration in unexpected street art."\n    }\n  ],\n  "genre": "Alternative & Punk",\n  "mood": "Happy",\n  "music": "Upbeat indie rock with a driving rhythm, featuring bright guitar riffs and a positive melody.",\n  "language": {\n    "name": "English",\n    "code": "en"\n  },\n  "characters": [\n    {\n      "name": "Ava",\n      "description": [\n        "Mid-20s, athletic build, dark hair pulled back in a messy bun.",\n        "Casual but stylish, wearing a lightweight jacket, dark jeans, and sneakers. Backpack is olive green and looks new.",\n        "Friendly and warm, with a hint of excitement in her voice."\n      ]\n    }\n  ],\n  "settings": [\n    {\n      "name": "Art District Street",\n      "description": [\n        "A vibrant street filled with colorful murals and modern architecture.",\n        "Energetic and bustling, with a mix of people and sounds.",\n        "The air is slightly dusty with the scent of street food."\n      ]\n    }\n  ]\n}\n```'}

# api_key = "AIzaSyAZcg46NcnId88vQsHzwwda6e1MaXLVEn4"
# storyboard_text = story
# images = generate_images_using_storyboard(api_key=api_key, storyboard =storyboard_text)



# # Save generated images
# for idx, img in enumerate(images):
#     img.save(f"scene_{idx+1}.png")

# from google import genai
# from google.genai import types

# client = genai.Client()

# response = client.models.generate_images(
#     model='imagen-4.0-generate-preview-06-06',
#     prompt='Robot holding a red skateboard',
#     config=types.GenerateImagesConfig(
#         number_of_images=4,
#     )
# )

# for i, generated_image in enumerate(response.generated_images, start=1):
#     pil_image = generated_image.image
#     file_name = f"generated_image_{i}.png"
#     pil_image.save(file_name)
#     print(f"Saved: {file_name}")
