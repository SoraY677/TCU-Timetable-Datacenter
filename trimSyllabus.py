from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

class trimSyllabus:

  def __init__(self):
    self.LectureMaxNum = 200
    self.driver = webdriver.Chrome("chromedriver.exe")
    self.driver.get("https://websrv.tcu.ac.jp/tcu_web_v3/slbsskgr.do")


  def accessLectureListPage(self):
    #=========講義から選択する処理
    #キャンパス選択
    self.driver.find_element_by_name("value(campuscd)").send_keys("横浜キャンパス")
    # 検索をかけるボタン
    self.driver.find_element_by_id("skgr_search").click()
    #=========表示件数の変更処理
    # 件数のセレクトボタンを取得し最大件数(200件)に変更
    selectElement = Select(self.driver.find_element_by_name("maxDispListCount"))
    selectElement.select_by_value(str(self.LectureMaxNum))
    #**件数合計を返す
    return 5;

  # 講義のリストを丸ごと取得して返す
  # @param hitNum : 取得する件数
  def copyLectureListDomFromPage(self,hitNum:int):
    # 講義のリスト奇数と偶数それぞれ取得
    oddLectureList = self.driver.find_elements_by_class_name("column_odd")
    evenLectureList = self.driver.find_elements_by_class_name("column_even")
    
    #======= 取得した講義を合体して返す
    SumLectureList = []
    print(int(hitNum/2))
    for li in range(int(hitNum/2)):
      SumLectureList.append(oddLectureList[li].text)
      SumLectureList.append(evenLectureList[li].text)
    if hitNum % 2 == 1:  # 件数が奇数個だった場合は最後に偶数講義を加える
      SumLectureList.append(oddLectureList[int(hitNum/2)].text)
    
    return SumLectureList

  
  def __del__(self):
    print("5秒後にシステムを終了します")
    time.sleep(5)
    self.driver.close()
    self.driver.quit()

