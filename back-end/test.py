from app.MusicRecognizeModel.utils import logInfo, logError, recognizeAudio, parsePath
from app.MusicRecognizeModel import Database

# recPath = "testData/testRecords/temp.mp3"


def testDBConnect():
	isConnect, errCode, errMsg = Database.checkDatabase()
	logError(isConnect, errCode, errMsg)


def testRecognize(path):
	print(path)
	logInfo(parsePath(path))
	resullt = recognizeAudio(path)
	return resullt


if __name__ == '__main__':
	# testDBConnect()
	testRecognize(str)
