import csv

def generateCSV(twoDimentionList:list,filePath: str):
  '''
  csvを生成する
  @param filePath
  @param twoDimentionList:二次元配列
  '''
  with open(filePath, "w",newline ="",encoding = "utf_8") as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(twoDimentionList)