from google.protobuf.json_format import MessageToJson
from google.cloud import vision
import os, io
import json

def google_ocr_call(Api_path,image_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = Api_path
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    # construct an iamge instance
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)  # returns TextAnnotation

    serialized = MessageToJson(response)

    data=json.loads(serialized)
    return data