import re

class trimSyllabus:

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

