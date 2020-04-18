import json

def generateJson(filePath,jsonStr):
  with open(filePath, "w",1,"utf-8") as writer:
    json.dump(jsonStr, writer,ensure_ascii=False)
