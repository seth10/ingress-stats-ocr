#-*- coding: utf-8 -*-

import pytesseract
import PIL.Image
import io
import os
from base64 import b64decode
import json
from datetime import datetime
import dateutil.tz
import boto3
from boto3.dynamodb.conditions import Key


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
  combinedData = (alltime + "\n" + now).splitlines()

  labels = [
    # alltime
    "Unique Portals Visited",
    "Portals Discovered",
    "Seer Points",
    "XM Collected",
    "Distance Walked",
    "Resonators Deployed",
    "Links Created",
    "Control Fields Created",
    "Mind Units Captured",
    "Longest Link Ever Created",
    "Largest Control Field",
    "XM Recharged",
    "Portals Captured",
    "Unique Portals Captured",
    "Mods Deployed",
    "Resonators Destroyed",
    "Portals Neutralized",
    "Enemy Links Destroyed",
    "Enemy Fields Destroyed",
    "Max Time Portal Held",
    "Max Time Link Maintained",
    "Max Link Length x Days",
    "Max Time Field Held",
    "Largest Field MUs x Days",
    "Unique Missions Completed",
    "Hacks",
    "Glyph Hack Points",
    "Longest Hacking Streak",
    # now
    "Links Active",
    "Portals Owned",
    "Control Fields Active",
    "Mind Unit Control",
    "Current Hacking Streak"
  ]
  stats = dict(zip(labels, combinedData))
  textStats = "INGRESS STATS OCR\n\n" + "\n".join([label+": "+value for (label, value) in zip(labels, combinedData)])

  stats['timestamp'] = datetime.now(tz=dateutil.tz.gettz('US/Pacific')).isoformat()[:19].replace('T',' ')

  dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
  table = dynamodb.Table('ingress-stats-ocr')


  response = table.put_item(Item=stats)

  stats['timestamp'] = 'latest'
  response = table.put_item(Item=stats)

  response = table.query(
      KeyConditionExpression=Key('timestamp').eq('latest')
  )
  # print response['Items'][0]['alltime']
  # print response['Items'][0]['now']
  # print json.dumps(response)
  print response['Items'][0]

  print textStats
  return textStats
