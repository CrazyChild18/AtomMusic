import os
import time
from . import Audio
from .logs import logInfo, logWarn, logError


def parsePath(args):
	path = "".join(args)
	if path[0] == "\"" and path[-1] == "\"":
		path = path[1:-1:]
	return os.path.realpath(path)


def recognizeAudio(path):
	filepath = parsePath(path)
	logInfo("Recognize Song")
	records_audio = Audio.Audio.initFromFile(filepath)
	logInfo("Start read records audio data......")
	records_audio.read()
	logInfo("Success")
	logInfo("Start get records audio fingerprints......")
	time_start = time.time()
	records_audio.getFingerprints()
	time_end = time.time()
	logInfo("Success! (Time cost: %d sec, total number: %s ) " % (time_end - time_start, len(records_audio.fingerprints)))
	logInfo("Recognize......")
	t1 = time.time()
	result = records_audio.recognize()
	t2 = time.time()
	if result is None:
		logInfo("Can not find any song fit this audio")
		return
	logInfo("Most Possible: %s (fingerprints match: %s), using %d sec" % (result["name"], result["count"], t2 - t1))
	return result["name"]
