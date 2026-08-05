import base64

import requests


FACEPP_API_KEY = "edEq6oq-Eqf3Sq4sfszoXpRQ9FHRRQGx"
FACEPP_API_SECRET = "Ky2HfeEgU58UvJkmCt5nIe97DMEeswRy"
FACEPP_COMPARE_URL = "https://api-us.faceplusplus.com/facepp/v3/compare"
DEFAULT_REMOTE_IMAGE_PATH = "http://localhost:8000"


class FaceApiCompareService:
    def encode_image_to_base64(self, image_path):
        with open(image_path, 'rb') as img_file:
            image_content = img_file.read()
            base64_image = base64.b64encode(image_content).decode('utf-8')
        return base64_image

    def compare_images(self, image_base64_1, image_base64_2):
        payload = {
            "api_key": FACEPP_API_KEY,
            "api_secret": FACEPP_API_SECRET,
            "image_base64_1": image_base64_1,
            "image_base64_2": image_base64_2,
        }
        response = requests.post(FACEPP_COMPARE_URL, data=payload)
        if response.json().get('error_message'):
            return "Error: {}".format(response.json().get('error_message'))
        response_json = response.json()
        return response_json.get('confidence', 0)


def compare_uploaded_images(image_file1, image_url_path):
    if not (image_file1 and image_url_path):
        return {'error': 'Missing image data in request'}, 400

    image_base64_1 = base64.b64encode(image_file1.read()).decode('utf-8')
    image_file2_url = DEFAULT_REMOTE_IMAGE_PATH + image_url_path
    image_file2_path = r"D:\DEV\Django\Nostalgia\media\image\image_file2.jpg"
    image_base64_2 = ""
    response = requests.get(image_file2_url)
    if response.status_code == 200:
        with open(image_file2_path, "wb") as file_handle:
            file_handle.write(response.content)
        with open(image_file2_path, "rb") as file_handle:
            image_base64_2 = base64.b64encode(file_handle.read()).decode('utf-8')
    if not image_base64_2:
        return {'error': 'Failed to download the Profile image file'}, 500

    service = FaceApiCompareService()
    result = service.compare_images(image_base64_1, image_base64_2)
    return {'result': result}, 200