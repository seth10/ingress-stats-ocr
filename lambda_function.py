import pytesseract
import PIL.Image
import io
import json
import os
from base64 import b64decode


LAMBDA_TASK_ROOT = os.environ.get('LAMBDA_TASK_ROOT', os.path.dirname(os.path.abspath(__file__)))
os.environ["PATH"] += os.pathsep + LAMBDA_TASK_ROOT
os.environ["TESSDATA_PREFIX"] = os.path.join(LAMBDA_TASK_ROOT, 'tessdata')

def lambda_handler(event, context):
  ret = {}
  for screenshotName, image64 in json.loads(event['body']).items():
    print screenshotName
    binary = b64decode(image64)
    image = PIL.Image.open(io.BytesIO(binary))
    text = pytesseract.image_to_string(image)
    ret[screenshotName] = text
  return ret
