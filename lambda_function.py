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
import re


LAMBDA_TASK_ROOT = os.environ.get('LAMBDA_TASK_ROOT', os.path.dirname(os.path.abspath(__file__)))
os.environ["PATH"] += os.pathsep + LAMBDA_TASK_ROOT
os.environ["TESSDATA_PREFIX"] = os.path.join(LAMBDA_TASK_ROOT, 'tessdata')

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
units = {
  # alltime
  "Unique Portals Visited": "",
  "Portals Discovered": "",
  "Seer Points": "",
  "XM Collected": " XM",
  "Distance Walked": " km",
  "Resonators Deployed": "",
  "Links Created": "",
  "Control Fields Created": "",
  "Mind Units Captured": " MUs",
  "Longest Link Ever Created": " km",
  "Largest Control Field": " MUs",
  "XM Recharged": " XM",
  "Portals Captured": "",
  "Unique Portals Captured": "",
  "Mods Deployed": "",
  "Resonators Destroyed": "",
  "Portals Neutralized": "",
  "Enemy Links Destroyed": "",
  "Enemy Fields Destroyed": "",
  "Max Time Portal Held": " days",
  "Max Time Link Maintained": " days",
  "Max Link Length x Days": " km-days",
  "Max Time Field Held": " days",
  "Largest Field MUs x Days": " MU-days",
  "Unique Missions Completed": "",
  "Hacks": "",
  "Glyph Hack Points": "",
  "Longest Hacking Streak": " days",
  # now
  "Links Active": "",
  "Portals Owned": "",
  "Control Fields Active": "",
  "Mind Unit Control": " MUs",
  "Current Hacking Streak": " days",
}
diffText = {
  # alltime
  "Unique Portals Visited": "gained {:,} unique portal visits",
  "Portals Discovered": "discovered {:,} new portals",
  "Seer Points": "{:,} seer points gained",
  "XM Collected": "collected {:,} XM",
  "Distance Walked": "walked {:,} km",
  "Resonators Deployed": "deployed {:,} resonators",
  "Links Created": "created {:,} links",
  "Control Fields Created": "created {:,} fields",
  "Mind Units Captured": "captured {:,} MU",
  "Longest Link Ever Created": "set a record for longest link of {:,} km",
  "Largest Control Field": "set a record for largest field of {:,} MUs",
  "XM Recharged": "recharged {:,} XM",
  "Portals Captured": "captured {:,} portals",
  "Unique Portals Captured": "gained {:,} unique portal captures",
  "Mods Deployed": "deployed {:,} mods",
  "Resonators Destroyed": "destroyed {:,} resonators",
  "Portals Neutralized": "destroyed {:,} portals",
  "Enemy Links Destroyed": "destroyed {:,} links",
  "Enemy Fields Destroyed": "destroyed {:,} fields",
  "Max Time Portal Held": "set a record for holding a portal {:,} days",
  "Max Time Link Maintained": "set a record for maintaining a link {:,} days",
  "Max Link Length x Days": "set a record for {:,} km-days",
  "Max Time Field Held": "set a record for holding a field {:,} days",
  "Largest Field MUs x Days": "set a record for {:,} MU-days",
  "Unique Missions Completed": "completed {:,} missions",
  "Hacks": "performed {:,} hacks",
  "Glyph Hack Points": "gained {:,} glyph hack points",
  "Longest Hacking Streak": "set a record hack streak of {:,} days",
  # now
  "Links Active": "created {:,} links (now)",
  "Portals Owned": "captured {:,} portals (now)",
  "Control Fields Active": "created {:,} fields (now)",
  "Mind Unit Control": "captured {:,} MU (now)",
  "Current Hacking Streak": "increased my current hacking streak to {:,} days"
}

def lambda_handler(event, context):
  t = {}
  for screenshotName, image64 in json.loads(event['body']).items():
    binary = b64decode(image64)
    image = PIL.Image.open(io.BytesIO(binary))
    text = pytesseract.image_to_string(image)
    t[screenshotName] = text
  
  for i in t:
    t[i] = t[i].replace("—", "-").replace("MUS", "MUs").replace("\n\n", "\n").replace("C]", "0")
    # sometimes 0's are recorded as '8' or 'C]'
  
  valuesWithUnits = t['alltime1'].splitlines()[:19] + t['alltime2'].splitlines()[-9:] + t['now'].splitlines()

  textStats = "INGRESS STATS OCR\n\n" + "\n".join([label+": "+value for (label, value) in zip(labels, valuesWithUnits)])
  print textStats

  stats = dict(zip(labels, valuesWithUnits))


  dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
  table = dynamodb.Table('ingress-stats-ocr')

  response = table.query(
      KeyConditionExpression=Key('timestamp').eq('latest')
  )
  # print json.dumps(response)
  lastStats = response['Items'][0]


  # Sanity checks: check for any values that should be strictly increasing that have decreased.
  # A digit that should have been 0 before might have been previously recorded as 8.
  # All values except for the ones on the "NOW" tab (last 5 labels) should only increase.
  for label in labels[:-5]:
    lastStat = int(re.sub(r"[^\d]*", "", lastStats[label]))
    stat = int(re.sub(r"[^\d]*", "", stats[label]))
    if lastStat > stat:
      pass


  stats['timestamp'] = datetime.now(tz=dateutil.tz.gettz('US/Pacific')).isoformat()[:19].replace('T',' ')
  response = table.put_item(Item=stats)

  stats['timestamp'] = 'latest'
  response = table.put_item(Item=stats)


  diffStats = []
  for label in labels:
    lastStat = int(re.sub(r"[^\d]*", "", lastStats[label]))
    stat = int(re.sub(r"[^\d]*", "", stats[label]))
    diff = stat - lastStat
    if diff != 0:
      diffStats.append(diffText[label].format(diff))
  diffStats = ", ".join(diffStats)+"."
  diffStats = diffStats[0].capitalize() + diffStats[1:]
  if diffStats == ".":
    diffStats = "No change."
  diffStats = "Ingress Stats OCR Progress Report\n\n" + diffStats

  print diffStats
  return diffStats
