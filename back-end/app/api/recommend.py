import datetime
import json
import time

from flask import request, jsonify
import requests
from app.api import bp
import config
import os
from app.recommend_song import Recommender


@bp.route('/uploadSong', methods=['POST'])
def uploadSong():
    data = request.files.get('file')
    path = config.basedir + '/recommend_songs/'
    if not os.path.exists(path):
        os.mkdir(path)
    time_str = time.mktime(datetime.datetime.now().timetuple())
    file_name = str(int(time_str)) + '.mp3'
    music_path = path + file_name
    data.save(music_path)
    return file_name


@bp.route('/recommendSong', methods=['POST'])
def recommendSong():
    data = request.get_json()
    music_name = data.get("fileName")
    path = config.basedir + '/recommend_songs/'
    music_path = path + music_name
    recommender = Recommender(music_path)
    song_type, sim_songs = recommender.recommend_sim_songs()
    os.remove(music_path)
    return jsonify(sim_songs)
