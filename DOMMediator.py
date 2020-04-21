from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import re
'''
画面の各ページにおける画面遷移処理
'''

# セレニウムのドライバを起動

driver = webdriver.Chrome("chromedriver.exe")


def openSyllabusPage():
    '''
    シラバスページを開く
    '''
    driver.get("https://websrv.tcu.ac.jp/tcu_web_v3/slbsskgr.do")


def trans200LectureListPageAfterCampusSelecte(campusName):
    '''
    キャンパス指定して講義リストのページ(1ページ目)遷移後200件表示にする
    campusName : 選ぶキャンパス名(世田谷キャンパス等々力キャンパス/横浜キャンパス)
    '''
    # ======キャンパスセレクト
    selectCampus = Select(driver.find_element_by_name("value(campuscd)"))
    selectCampus.select_by_visible_text(campusName)

    # ====== 検索をかけるボタンをクリック
    driver.find_element_by_id("skgr_search").click()
    time.sleep(2)  # 遷移を休ませる

    # ====== 200件表示にする
    selectLectureNum = Select(
        driver.find_element_by_name("maxDispListCount"))
    selectLectureNum.select_by_value("200")


def gatherLectureParts():
    '''
    <td></td>タグに囲まれた各講義情報を集めて二次元配列にして返す
    @return resultLectureList:各講義の配列
    '''
    # 講義のリスト奇数と偶数それぞれ取得
    oddLectureList = driver.find_elements_by_xpath(
        "//tr[@class='column_odd']/td")
    evenLectureList = driver.find_elements_by_xpath(
        "//tr[@class='column_even']/td")

    lectureColumNum = 6  # １講義のカラム数

    # ======= 取得した講義を合体して返す
    resultLectureList = []
    # 一行ごとの処理
    for li in range(int(len(evenLectureList) / lectureColumNum)):
        oddLectureLine = []
        evenLectureLine = []
        # カラムごとの処理
        for ci in range(lectureColumNum):
            # li * lectureColumNum + ci => 着目している行の着目しているカラム
            oddLectureLine.append(
                oddLectureList[li * lectureColumNum + ci].text)
            evenLectureLine.append(
                evenLectureList[li * lectureColumNum + ci].text)

        resultLectureList.append(oddLectureLine)
        resultLectureList.append(evenLectureLine)

    # もし偶数の講義が一つだけあまってしまったら
    if len(oddLectureList) > len(evenLectureList):
        # 余った講義の配列を結果に加える
        tmp = [oddLectureList[len(oddLectureList) - lectureColumNum  + i].text for i in range(lectureColumNum)]
        resultLectureList.append(tmp)

    return resultLectureList


def changeLectrueListPage():
    '''
    次の講義リストページへ画面遷移する
    '''
    nextPage = driver.find_elements_by_xpath(
        "//tr[@class='link']/td/div[@class='right']/span[2]/a")
    nextPage[int(len(nextPage) / 2) - 1].click()
    time.sleep(2)


def isArriveFinalLecturePage():
    '''
    講義リストの最終ページにたどり着いたかどうかを判する
    '''
    # 総件数を含んだ全文の取得
    originText: str = (driver.find_element_by_xpath(
        "//tr[@class='link']/td/div[@class='right']/span[1]").text)
    # ***-yyy件表示/xxx件中 を yyyとxxx の計算結果整形する処理
    pageCurrent, pageMax = originText.split('/')
    pageCurrent = pageCurrent.replace(
        re.search('.*-', pageCurrent).group(0), '')
    pageCurrent = pageCurrent.replace('件表示', '')
    pageMax = pageMax.replace('件中', '')

    # 最終ページまでいった
    if (int(pageMax) - int(pageCurrent) == 0):
        return True
    return False


def __del__():
    '''
    selleniumを正常終了する
    '''
    driver.close()
    driver.quit()
