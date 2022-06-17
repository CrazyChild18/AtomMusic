from pydub import AudioSegment
from hashlib import sha256
import config
import numpy as np
import os
from .logs import logError, logInfo


def generateFileHash(filepath, blockSize=2 ** 16):
	sha = sha256()
	with open(filepath, "rb") as f:
		while True:
			buffer = f.read(blockSize)
			if not buffer:
				break
			sha.update(buffer)
	return sha.hexdigest().upper()


def encodeAudio(filepath, tempDir="reformatAudio"):
	dir = os.path.realpath(tempDir)
	logInfo("Encode Audio with ffmpeg......")
	if not os.path.exists(dir):
		os.makedirs(dir)
	path = os.path.join(dir, generateFileHash(filepath)[:6:] + config.audio_extension)
	os.system(" ".join(["ffmpeg", "-loglevel", "quiet", "-i", "\"%s\"" % filepath, "-y", "-acodec", "mp3", "-ar",
						str(config.audio_frame_rate), "\"%s\"" % path]))
	return path


def read(filepath):
	try:
		filename, extension = os.path.splitext(filepath)
		audiofile = AudioSegment.from_file(filepath)

		# set all audio file frame rate with a default value and same extensions
		if audiofile.frame_rate != config.audio_frame_rate or extension != config.audio_extension:
			audiofile = AudioSegment.from_file(encodeAudio(filepath))
		data = np.fromstring(audiofile.raw_data, np.int32)
		channels = []
		# Get data for different channel
		for channel in range(audiofile.channels):
			channels.append(data[channel::audiofile.channels])
	except:
		logError("AudioDecoder Read Failed")
		return 0, 0

	return audiofile.frame_rate, channels


def readDir(filesdir):
	for root, dirs, files in os.walk(filesdir):
		for file in files:
			filename, exten = os.path.splitext(os.path.split(file)[1])
			if exten in config.support_audio:
				try:
					fh = generateFileHash(os.path.join(root, file))
				except:
					continue
				yield os.path.join(root, file), filename, fh
		if not config.search_subdirectories:
			break
