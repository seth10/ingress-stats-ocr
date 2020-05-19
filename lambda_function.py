import pytesseract
import PIL.Image
import io
import os
from base64 import b64decode


LAMBDA_TASK_ROOT = os.environ.get('LAMBDA_TASK_ROOT', os.path.dirname(os.path.abspath(__file__)))
os.environ["PATH"] += os.pathsep + LAMBDA_TASK_ROOT
#os.environ["LD_LIBRARY_PATH"] = os.path.join(LAMBDA_TASK_ROOT, 'tessdata')
os.environ["TESSDATA_PREFIX"] = os.path.join(LAMBDA_TASK_ROOT, 'tessdata')

def lambda_handler(event, context):
  print os.getcwd()
  print LAMBDA_TASK_ROOT
  print os.listdir('.')
  print os.environ["LD_LIBRARY_PATH"]
  print os.environ["TESSDATA_PREFIX"]
  binary = b64decode(event['image64'])
  image = PIL.Image.open(io.BytesIO(binary))
  text = pytesseract.image_to_string(image)
  return {'text' : text}
