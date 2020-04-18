from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

class trimSyllabus:

  def __init__(self):
    self.onePageLectureMaxNum = 200
    self.LectureCurrentNum = 0

    # 指定のページにアクセスし、必要な情報を入手しておく
    self.driver = webdriver.Chrome("chromedriver.exe")
    self.driver.get("https://websrv.tcu.ac.jp/tcu_web_v3/slbsskgr.do")
    self.accessLectureListPage()
    self.sumLectureNum = self.findSumLectureNum()

  def accessLectureListPage(self):
    '''
    講義のリストページに遷移する
    @return 件数の合計
    '''
    #=========講義から選択する処理
    #キャンパス選択
    self.driver.find_element_by_name("value(campuscd)").send_keys("横浜キャンパス")
    # 検索をかけるボタン
    self.driver.find_element_by_id("skgr_search").click()
    #=========表示件数の変更処理
    # 件数のセレクトボタンを取得し最大件数(200件)に変更
    selectElement = Select(self.driver.find_element_by_name("maxDispListCount"))
    selectElement.select_by_value(str(self.onePageLectureMaxNum))

  def findSumLectureNum(self):
    '''
    件数を取得して整形して返す
    @return sumLectureNum : 講義数
    '''
    originText: str = (self.driver.find_element_by_xpath("//tr[@class='link']/td/div[@class='right']/span[1]").text)
    parseText:str = originText.split('/')[1]  # "xxx件中"に限定
    parseText = parseText.replace('件中', '')
    sumLectureNum = int(parseText)
    return sumLectureNum
    
  def copyLectureListDomFromPage(self, hitNum: int):
    '''
    講義のリストを1ページ丸ごと取得して返す
    @param hitNum : 取得する件数
    @return SumLectureList: 取得した講義リストのすべて 
    '''
    # 講義のリスト奇数と偶数それぞれ取得
    oddLectureList = self.driver.find_elements_by_class_name("column_odd")
    evenLectureList = self.driver.find_elements_by_class_name("column_even")
    
    #======= 取得した講義を合体して返す
    SumLectureList = []
    for li in range(int(hitNum / 2)):
      SumLectureList.append(self.parseLecture(oddLectureList[li].text))
      SumLectureList.append(self.parseLecture(evenLectureList[li].text))
    if hitNum % 2 == 1:  # 件数が奇数個だった場合は最後に偶数講義を加える
      SumLectureList.append(self.parseLecture(oddLectureList[int(hitNum/2)].text))
    
    return SumLectureList

  def extendLectureList(self):
    '''
    全ての件数ぶんの講義の配列を取得し、結合する
    @return extendLectureList/List:講義全てを結合した配列
    '''
    sumLectureNum = self.findSumLectureNum()

    extendLectureList = []
    # 本来のページ数-1まで探索
    pageNum = int((sumLectureNum - 1) / 200)
    for pi in range(pageNum):
      extendLectureList.extend(self.copyLectureListDomFromPage(self.onePageLectureMaxNum))
      nextPage = self.driver.find_elements_by_xpath("//tr[@class='link']/td/div[@class='right']/span[2]/a")
      nextPage[int(len(nextPage) / 2) - 1].click()
      time.sleep(2) # 待機しないとエラー起こす

    # 200に満たない件数分を取得
    lastPageLectureNum = sumLectureNum % 200
    extendLectureList.extend(self.copyLectureListDomFromPage(lastPageLectureNum))

    return extendLectureList

  def parseLecture(self, lectureLine:str):
    # 開講期間 曜日・時限が二つある場合は改行されるのでそれを省く
    parseLine = lectureLine.split(" ")

    parseResult = {}
    parseResult["code"] = parseLine[1]
    parseResult["name"] = parseLine[2]
    parseResult["target"] = parseLine[3]
    parseResult["time"] = parseLine[4].split("\n")
    parseResult["instructor"] = []
    for ii in range(5, len(parseLine)):
      parseResult["instructor"].append(parseLine[ii])
    return parseResult

  def __del__(self):
    print("5秒後にシステムを終了します")
    time.sleep(5)
    self.driver.close()
    self.driver.quit()

