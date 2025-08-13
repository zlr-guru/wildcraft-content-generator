import requests

base_url = "http://127.0.0.1:5000"

# Test /generate_product_description
res = requests.post(f"{base_url}/generate_product_description", json={
    "image1_path": "image_path",
    "image2_path": "image_path"
})
print("/generate_product_description:", res.json())
print("*"*30)
# Test /generate_product_tags
res = requests.post(f"{base_url}/generate_product_tags", json={
    "image1_path": "image_path",
    "image2_path": "image_path"
})
print("/generate_product_tags:", res.json())
print("*"*30)

# Test /generate_storyboard
res = requests.post(f"{base_url}/generate_storyboard", json={
    "image1_path": "image_path",
    "image2_path": "image_path",
    "pitch": "Urban travel adventure",
    "num_scenes": 1,
    "style": "cinematic",
    "language_name": "English",
    "language_code": "en"
})
print("/generate_storyboard:", res.json())

# Test /generate_storyboard
res = requests.post(f"{base_url}/generate_storyboard", json={
    "image1_path": "image_path",
    "image2_path": "image_path",
    "pitch": "Urban travel adventure",
    "num_scenes": 1,
    "style": "cinematic",
    "language_name": "English",
    "language_code": "en"
})
print("/generate_storyboard:", res.json())
