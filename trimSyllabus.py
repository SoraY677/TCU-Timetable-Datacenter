from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import re


class trimSyllabus:

    def __init__(self):
        self.onePageLectureMaxNum = 200

        # 指定のページにアクセスし、必要な情報を入手しておく
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.driver.get("https://websrv.tcu.ac.jp/tcu_web_v3/slbsskgr.do")
        self.accessLectureListPage("横浜キャンパス")
        self.sumLectureNum = self.findSumLectureNum()

    def accessLectureListPage(self, category):
        '''
        講義のリストページに遷移する
        @return 件数の合計
        '''
        # =========講義から選択する処理
        # キャンパス選択
        selectCategory = Select(
            self.driver.find_element_by_name("value(campuscd)"))
        selectCategory.select_by_visible_text(category)
        # 検索をかけるボタン
        self.driver.find_element_by_id("skgr_search").click()
        # =========表示件数の変更処理
        # 件数のセレクトボタンを取得し最大件数(200件)に変更
        selectLectureNum = Select(
            self.driver.find_element_by_name("maxDispListCount"))
        selectLectureNum.select_by_value(str(self.onePageLectureMaxNum))

    def findSumLectureNum(self):
        '''
        件数を取得して整形して返す
        @return sumLectureNum : 講義数
        '''
        originText: str = (self.driver.find_element_by_xpath(
            "//tr[@class='link']/td/div[@class='right']/span[1]").text)
        parseText: str = originText.split('/')[1]  # "xxx件中"に限定
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
        oddLectureList = self.driver.find_elements_by_xpath("//tr[@class='column_odd']/td")
        evenLectureList = self.driver.find_elements_by_xpath("//tr[@class='column_even']/td")
        # ======= 取得した講義を合体して返す
        SumLectureList = []
        for li in range(int(hitNum / 2)):
            lectureel = [oddLectureList[i].text for i in range(6 * (li), 6 * (li + 1))]
            SumLectureList.append(self.parseLecture(lectureel))
            lectureel = [evenLectureList[i].text for i in range(6 * (li),6 * (li+1))]
            SumLectureList.append(self.parseLecture(lectureel))

        if hitNum % 2 == 1:  # 件数が奇数個だった場合は最後に偶数講義を加える
            lectureel = [oddLectureList[i].text for i in range(6 * (hitNum - 1), 6 * (hitNum))]
            SumLectureList.append(self.parseLecture(lectureel))

        return SumLectureList

    def extendLectureList(self):
        '''
        全ての件数ぶんの講義の配列を取得し、結合する
        @return extendLectureList/List:講義全てを結合した配列
        '''
        sumLectureNum = self.findSumLectureNum()

        extendLectureList = []
        # 本来のページ数-1まで探索
        pageNum = int((sumLectureNum - 1) / self.onePageLectureMaxNum)
        for pi in range(pageNum):
            extendLectureList.extend(
                self.copyLectureListDomFromPage(self.onePageLectureMaxNum))
            nextPage = self.driver.find_elements_by_xpath(
                "//tr[@class='link']/td/div[@class='right']/span[2]/a")
            nextPage[int(len(nextPage) / 2) - 1].click()
            time.sleep(2)  # 待機しないとエラー起こす

        # 200に満たない件数分を取得
        lastPageLectureNum = sumLectureNum % 200
        extendLectureList.extend(
            self.copyLectureListDomFromPage(lastPageLectureNum))

        return extendLectureList

    def parseLecture(self, lectureLine: list):
        print(lectureLine)
        # 開講期間 曜日・時限が二つある場合は改行されるのでそれを省く
        parseResult = {}
        parseResult["code"] = lectureLine[1]
        #===============
        parseResult["name"] = lectureLine[2] 
        # ===============
        if lectureLine[3] != "":
          parseResult["targetyear"] = re.search("\d*", lectureLine[3]).group(0)
        # ===============
          parseResult["targetdepart"] = lectureLine[3].replace(re.search("学.*", lectureLine[3]).group(0), "")  # xxxx年度yy学科うんたら => xxxx年度yy
          parseResult["targetdepart"] = parseResult["targetdepart"].replace(re.search(parseResult["targetyear"] + "年度", lectureLine[3]).group(0), "")  # xxxx年度yy => yy
        else:
          parseResult["targetyear"] = ""
          parseResult["targetdepart"] = ""
        # ==============
        parseResult["time"] = []
        for timeel in lectureLine[4].split("\n"):
            timeblockList = timeel.split("　")
            timeblock = {}  # parseResult["time"]に追加する用
            timeblock["period"] = timeblockList[0]
            if len(timeblockList) < 3:  # 通年の場合(おそらく)
                timeblock["dow"] = ""
                timeblock["thclass"] = ""
            else:
                timeblock["dow"] = timeblockList[1][0]
                timeblock["thclass"] = timeblockList[2][0].translate(str.maketrans({
                    "１": "1",
                    "２": "2",
                    "３": "3",
                    "４": "4",
                    "５": "5"
                }))
            parseResult["time"].append(timeblock)

        # ==============
        parseResult["instructor"] = lectureLine[5].split("\n")

        return parseResult

    def __del__(self):
        self.driver.close()
        self.driver.quit()
