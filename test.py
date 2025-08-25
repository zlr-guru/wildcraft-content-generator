import requests

# from wcraft import generate_images_using_storyboard

BASE_URL = "http://127.0.0.1:5000"

# # 1. Test generate_product_description
# url = f"{BASE_URL}/generate_product_description"
# payload = {
#     "image1_path": "C:\\Users\\GuruCharan\\Documents\\Wildcraft\\wcraft_vscode\\bag_1.jpg",
#     "image2_path": "C:\\Users\\GuruCharan\\Documents\\Wildcraft\\wcraft_vscode\\bag_2.jpg",
#     "google_api_key": "API_KEY"
# }
# r = requests.post(url, json=payload)
# print("generate_product_tags:", r.json())



# 2. Test generate_product_tags
url = f"{BASE_URL}/generate_product_tags"
payload = {
    "image1_path": "C:\\Users\\GuruCharan\\Documents\\Wildcraft\\wcraft_vscode\\bag_1.jpg",
    "image2_path": "C:\\Users\\GuruCharan\\Documents\\Wildcraft\\wcraft_vscode\\bag_2.jpg",
    "google_api_key": "AIzaSyAZcg46NcnId88vQsHzwwda6e1MaXLVEn4"
}
r = requests.post(url, json=payload)
print("generate_product_tags:", r.json())



# # 3. Test /generate_storyboard
# BASE_URL = "http://127.0.0.1:5000"

# res = requests.post(f"{BASE_URL}/generate_storyboard", json={
#     "google_api_key": "AIzaSyAZcg46NcnId88vQsHzwwda6e1MaXLVEn4",
#     "image1_path": "C:\\Users\\GuruCharan\\Documents\\Wildcraft\\wcraft_vscode\\bag_1.jpg",
#     "image2_path": "C:\\Users\\GuruCharan\\Documents\\Wildcraft\\wcraft_vscode\\bag_2.jpg",
#     "pitch": "Urban travel adventure",
#     "num_scenes": 1,
#     "style": "cinematic",
#     "language_name": "English",
#     "language_code": "en"
# })
# print("/generate_storyboard:", res.json())

# # 4. Test change_background
# import requests


# payload = {
#     "image_path": "C:\\Users\\GuruCharan\\Documents\\Wildcraft\\wcraft_vscode\\raincoat_1.jpg",  # Path to your local image file
#     "prompt": "change the background to a green screen",
#     "google_api_key": "AIzaSyArrj7KGsMy-CwNBwtGJmmmy1o6Lom6gNM"
# }

# response = requests.post(f"{BASE_URL}/change_background", json=payload)

# print("Status Code:", response.status_code)
# print("Response JSON:", response.json())



# payload = {
#     "api_key": "YOUR_GOOGLE_API_KEY",
#     "storyboard": "A cozy coffee shop with warm lighting"
# }

# res = requests.post(f"{BASE_URL}/generate_storyboard_images", json=payload)
# data = res.json()

# # Save first image to file
# if "images" in data:
#     img_bytes = bytes.fromhex(data["images"][0]["data"])
#     with open(data["images"][0]["filename"], "wb") as f:
#         f.write(img_bytes)



    