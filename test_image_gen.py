from wcraft import generate_images_using_storyboard
from PIL import Image

# # Example storyboard
# storyboard_text =  {'storyboard': '```json\n{\n  "scenario": "Alex, a young urban explorer, navigates the bustling heart of a city square with an effortless cool. The sleek, dark green backpack is a natural extension of their confident stride, its durable fabric catching the glint of the afternoon sun. With a quick, intuitive glance at their phone for directions, Alex looks up, a subtle smile playing on their lips, ready to embrace the city\'s hidden gems. The backpack\'s comfort and stylish design are evident as they weave through the vibrant crowd, embodying the spirit of an urban adventure.",\n  "scenes": [\n    {\n      "title": "Urban Explorer\'s Flow",\n      "description": "A young adult, Alex, moves confidently through a sun-drenched, bustling city square. Their dark green backpack sits comfortably on their back, its modern design complementing their casual yet stylish urban attire. Alex briefly consults their phone for directions, then looks up with an air of anticipation and a relaxed smile, ready to continue exploring. The scene emphasizes the backpack\'s seamless integration into their active, urban lifestyle, highlighting its comfort and aesthetic appeal amidst the vibrant city backdrop."\n    }\n  ],\n  "genre": "Pop",\n  "mood": "Bright",\n  "music": "An upbeat, rhythmic track featuring a driving synth bassline, crisp percussive accents, and an uplifting, melodic synth lead that evokes a sense of optimistic discovery.",\n  "language": {\n    "name": "English",\n    "code": "en"\n  },\n  "characters": [\n    {\n      "name": "Alex",\n      "description": [\n        "Young adult, mid-20s to early 30s, exuding an air of quiet confidence and curiosity.",\n        "Dressed in a muted, stylish bomber jacket over a simple t-shirt, dark tailored jeans, and modern, comfortable sneakers. The dark green backpack is a prominent accessory, worn casually.",\n        "Voice is not heard, but their posture and facial expressions suggest a calm and self-assured demeanor."\n      ]\n    }\n  ],\n  "settings": [\n    {\n      "name": "Bustling City Square",\n      "description": [\n        "A vibrant, sun-drenched open-air city square, characterized by a mix of modern glass buildings and classic stone architecture.",\n        "The atmosphere is energetic and lively, filled with the soft hum of conversation, the distant sounds of traffic, and occasional street musician melodies. Sunlight casts long shadows and highlights textures.",\n        "Sensory details include the feeling of a light breeze, the faint scent of street food, and the visual tapestry of diverse people moving through the space."\n      ]\n    }\n  ]\n}\n```'}
# # Call function
# images = generate_images_using_storyboard(storyboard_text)

# print(f"Generated {len(images)} images")

# # Save them to disk
# for idx, img in enumerate(images):
#     img.save(f"generated_image_{idx+1}.png")
#     print(f"Saved generated_image_{idx+1}.png")


import requests

# Flask API URL
url = "http://127.0.0.1:5000/change_background"

# Request payload
payload = {
    "image_path": "image_path",
    "prompt": "Add a mountain bike in the background"
}

# Send POST request
response = requests.post(url, json=payload)

# Print the result
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
