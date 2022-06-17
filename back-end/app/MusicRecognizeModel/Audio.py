import config
import gc
import multiprocessing
import os

from sqlalchemy.orm import scoped_session

from . import AudioDecoder
from . import Database
from . import Fingerprint


class Audio(object):
	db, db_engine = Database.initSession()

	def __init__(self, filepath, filename, filehash):
		self.filepath = filepath
		self.filename = filename
		self.filehash = filehash
		self.fs = None
		self.channels = None
		self.fingerprints = None
		self.id = None
		self.name = None

	@classmethod
	def initFromFile(cls, filepath):
		filepath = os.path.realpath(filepath)
		filehash = AudioDecoder.generateFileHash(filepath)
		filename = os.path.splitext(os.path.split(filepath)[1])[0]
		return cls(filepath, filename, filehash)

	def read(self):
		self.fs, self.channels = AudioDecoder.read(self.filepath)

	def getFingerprints(self):
		fingerprints = set()
		for channel in self.channels:
			arr = Fingerprint.getSpecgramArr(channel, self.fs)
			peaks = Fingerprint.getConstellationMap(arr)
			del arr
			fp = Fingerprint.getFBHashGenerator(peaks)
			del peaks
			# get unioin for different channel
			fingerprints |= set(fp)

		self.fingerprints = fingerprints
		del fingerprints
		gc.collect()
		return

	# use multiprocess
	def recognize(self):
		ss = scoped_session(self.db)
		dbs = ss()
		matches = []
		p = multiprocessing.Pool()
		result = p.map(_matchFingerprints, (data for data in self.fingerprints))
		p.close()
		p.join()
		for r in result:
			matches.extend(r)
		possibility = {}
		mostPossible = {"id": "", "name": "", "count": 0}
		largest = 0
		for song_id, offest_diff in matches:
			if song_id not in possibility:
				possibility[song_id] = dict()
			if offest_diff not in possibility[song_id]:
				possibility[song_id][offest_diff] = 0
			possibility[song_id][offest_diff] += 1
			if possibility[song_id][offest_diff] > largest:
				largest = possibility[song_id][offest_diff]
				mostPossible["id"] = song_id
				name = dbs.query(Database.Songs).filter_by(id=song_id).first().name
				mostPossible["name"] = name
				mostPossible["count"] = largest

		dbs.close()
		ss.remove()
		if mostPossible["count"] < config.min_match_num:
			return None
		return mostPossible

	def cleanup(self):
		del self.fingerprints
		del self.channels
		gc.collect()


def _matchFingerprints(data):
	fp, offset = data
	db, e = Database.initSession()
	ss = scoped_session(db)
	dbs = ss()
	matches = []
	try:
		for r in dbs.query(Database.Fingerprints).filter_by(fingerprint=fp).all():
			s = dbs.query(Database.Songs).filter_by(id=r.song_id).first()
			matches.append((str(s.id), str(abs(r.offset - offset))))
	finally:
		dbs.close()
		ss.remove()

	return matches
