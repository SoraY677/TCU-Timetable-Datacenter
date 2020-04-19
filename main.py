from trimSyllabus import trimSyllabus
import jsonGenerator

trimsyllabus = trimSyllabus()
jsonGenerator.generateJson("data/LectureList.json", trimsyllabus.extendLectureList())
del trimsyllabus