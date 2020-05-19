#-*- coding: utf-8 -*-

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
  t = {}
  for screenshotName, image64 in json.loads(event['body']).items():
    binary = b64decode(image64)
    image = PIL.Image.open(io.BytesIO(binary))
    text = pytesseract.image_to_string(image)
    t[screenshotName] = text
  
  for i in t:
    t[i] = t[i].replace("—", "-").replace("MUS", "MUs").replace("\n\n", "\n")
  
  now = t['now']
  alltime = t['alltime1']
  duplicateLength = 1
  while alltime.rfind(t['alltime2'][:duplicateLength]) > -1:
    duplicateLength += 1
  alltime += t['alltime2'][duplicateLength-1:]


  return "NOW\n{}\n\nALL TIME\n{}".format(now, alltime)
