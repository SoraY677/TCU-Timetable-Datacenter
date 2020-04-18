import json

def generateJson(filePath,jsonStr):
  with open(filePath, "w",1,"utf-8") as writer:
    json.dump(jsonStr, writer,indent = 2,ensure_ascii=False)
