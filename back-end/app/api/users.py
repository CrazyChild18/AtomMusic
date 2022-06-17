import json
from datetime import datetime
import io
import re
import requests
from PIL import Image
from flask import request, jsonify, url_for, app, make_response
from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import User, Like, History
from sqlalchemy import true, extract
import os
import config
from werkzeug.security import generate_password_hash, check_password_hash


@bp.route('/users', methods=['POST'])
def create_user():
    """注册一个新用户"""
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')

    message = {}
    if 'username' not in data or not data.get('username', None):
        message['username'] = 'Please provide a valid username.'
    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' not in data or not re.match(pattern, data.get('email', None)):
        message['email'] = 'Please provide a valid email address.'
    if 'password' not in data or not data.get('password', None):
        message['password'] = 'Please provide a valid password.'

    if User.query.filter_by(username=data.get('username', None)).first():
        message['username'] = 'Please use a different username.'
    if User.query.filter_by(email=data.get('email', None)).first():
        message['email'] = 'Please use a different email address.'
    if message:
        return bad_request(message)

    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users', methods=['GET'])
def get_users():
    """返回所有用户的集合"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@bp.route('/getUserDetail', methods=['POST'])
@token_auth.login_required
def get_user():
    """返回一个用户"""
    data = request.get_json()
    userID = data.get("userId")
    return jsonify(User.query.get_or_404(userID).to_dict(include_email=true))


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    """修改一个用户"""
    user = User.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')

    message = {}
    if 'username' in data and not data.get('username', None):
        message['username'] = 'Please provide a valid username.'

    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' in data and not re.match(pattern, data.get('email', None)):
        message['email'] = 'Please provide a valid email address.'

    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        message['username'] = 'Please use a different username.'
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        message['email'] = 'Please use a different email address.'

    if message:
        return bad_request(message)

    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/users/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    """删除一个用户"""
    pass


@bp.route('/changeUserBasicInfo', methods=['POST'])
@token_auth.login_required
def changeUserBasicInfo():
    """修改用户基本信息"""
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    id = data.get("id")
    username = data.get("username")
    email = data.get("email")
    sex = data.get("gender")
    phone = data.get("phone")
    getUser = User.query.get_or_404(id)
    getUser.username = username
    getUser.email = email
    getUser.sex = sex
    getUser.phone = phone
    db.session.commit()
    return "successful"


@bp.route('/changePassword', methods=['POST'])
@token_auth.login_required
def changePassword():
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    id = data.get("id")
    password = data.get("newPassword")
    currentPassword = data.get("currentPassword")
    user = User.query.get_or_404(id)
    if not check_password_hash(user.password_hash, currentPassword):
        return 'passwordError'
    else:
        user.password_hash = generate_password_hash(password)
        db.session.commit()
        return 'successful'


@bp.route('/changeLocation', methods=['POST'])
@token_auth.login_required
def changeLocation():
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    id = data.get("id")
    locationName = data.get("currentLocationName")
    user = User.query.get_or_404(id)
    user.location = locationName
    db.session.commit()
    return "successful"


@bp.route('/changeAboutMe', methods=['POST'])
@token_auth.login_required
def changeAboutMe():
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    id = data.get("id")
    content = data.get("content")
    user = User.query.get_or_404(id)
    user.about_me = content
    db.session.commit()
    return 'successful'


@bp.route('/changeAvatar', methods=['POST'])
@token_auth.login_required
def changeAvatar():
    data = request.files.get('file')
    id = request.form.get('id')
    path = config.basedir + '/avatar/'
    avatar_name = str(id) + '.jpg'
    user = User.query.get_or_404(id)
    user.avatar = avatar_name
    db.session.commit()
    avatarPath = path + avatar_name
    data.save(avatarPath)
    return "successful"


@bp.route('/getUserAvatar', methods=['POST'])
@token_auth.login_required
def getUserAvatar():
    data = request.get_json()
    picName = data.get("picName")
    if picName is None:
        picName = 'default.jpg'
    path = config.basedir + '/avatar/'
    img_local_path = path + picName
    with open(img_local_path, 'rb') as f:
        a = f.read()
    '''对读取的图片进行处理'''
    img_stream = io.BytesIO(a)
    img = Image.open(img_stream)
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


@bp.route('/setMusicLike', methods=['POST'])
@token_auth.login_required
def setMusicLike():
    data = request.get_json()
    userID = data.get('userID')
    musicID = data.get('musicID')
    like = Like()
    like.userID = userID
    like.musicID = musicID
    db.session.add(like)
    db.session.commit()
    return 'successful'


@bp.route('/setMusicDislike', methods=['POST'])
@token_auth.login_required
def setMusicDislike():
    data = request.get_json()
    userID = data.get('userID')
    musicID = data.get('musicID')
    like = Like.query.filter_by(userID=userID, musicID=musicID).first()
    db.session.delete(like)
    db.session.commit()
    return 'successful'


@bp.route('/queryMusicLike', methods=['POST'])
@token_auth.login_required
def queryMusicLike():
    data = request.get_json()
    userID = data.get('userID')
    musicID = data.get('musicID')
    like = Like.query.filter_by(userID=userID, musicID=musicID).first()
    if not like:
        return "False"
    else:
        return "True"


@bp.route('/recordHistory', methods=['POST'])
@token_auth.login_required
def recordHistory():
    data = request.get_json()
    userID = data.get('userID')
    musicID = data.get('musicID')
    history = History.query.filter_by(musicID=musicID, userID=userID).first()
    if not history:
        newHistory = History()
        newHistory.musicID = musicID
        newHistory.userID = userID
        newHistory.count = 1
        newHistory.time = datetime.utcnow()
        db.session.add(newHistory)
        db.session.commit()
    else:
        history.count = history.count + 1
        history.time = datetime.utcnow()
        db.session.commit()
    return 'successful'


@bp.route('/countTime', methods=['POST'])
@token_auth.login_required
def countTime():
    data = request.get_json()
    userID = data.get('userId')
    user = User.query.get_or_404(userID)
    timeNow = datetime.utcnow()
    createTime = user.create_time
    time = timeNow - createTime
    days = time.days
    # print(days)
    return jsonify(days)


@bp.route('/getHistoryAndCount', methods=['POST'])
@token_auth.login_required
def getHistoryAndCount():
    data = request.get_json()
    userID = data.get('userId')
    history_list = History.query.filter_by(userID=userID).order_by(History.count.desc()).limit(5).all()
    # print(history_list)
    musicList = []
    countList = []
    resultList = {}
    for history in history_list:
        countList.append(history.count)
        musicID = history.musicID
        res = requests.get("https://autumnfish.cn/song/detail?ids=" + str(musicID)).content
        json_res = json.loads(res)
        songs = json_res["songs"]
        songsItem = songs[0]
        al = songsItem["al"]
        musicName = al["name"]  # 歌曲名称
        musicList.append(musicName)
    resultList["musicList"] = musicList
    resultList["countList"] = countList
    return jsonify(resultList)


@bp.route('/getPerDayAmount', methods=['POST'])
@token_auth.login_required
def getPerDayAmount():
    data = request.get_json()
    userID = data.get('userId')
    history_0 = History.query.filter(extract('day', History.time) == datetime.now().day, userID == userID).all()
    history_1 = History.query.filter(extract('day', History.time) == datetime.now().day - 1, userID == userID).all()
    history_2 = History.query.filter(extract('day', History.time) == datetime.now().day - 2, userID == userID).all()
    history_3 = History.query.filter(extract('day', History.time) == datetime.now().day - 3, userID == userID).all()
    history_4 = History.query.filter(extract('day', History.time) == datetime.now().day - 4, userID == userID).all()
    history_0_count = len(history_0)
    history_1_count = len(history_1)
    history_2_count = len(history_2)
    history_3_count = len(history_3)
    history_4_count = len(history_4)
    history_count_list = [history_0_count, history_1_count, history_2_count, history_3_count, history_4_count]
    history_dat_list = [datetime.now().day, datetime.now().day - 1, datetime.now().day - 2, datetime.now().day - 3,
                        datetime.now().day - 4]
    result = [history_count_list, history_dat_list]
    return jsonify(result)


@bp.route('/getLikeAndHistory', methods=['POST'])
@token_auth.login_required
def getLikeAndHistory():
    data = request.get_json()
    userID = data.get('userId')
    history = History.query.filter_by(userID=userID).all()
    history_num = len(history)
    musicIDList = []
    for h in history:
        musicIDList.append(h.musicID)
    like_num = 0
    for id in musicIDList:
        like = Like.query.filter_by(musicID=id).all()
        like_num = like_num + len(like)
    likeMusicInHistory = {'value': like_num, 'name': 'Like Part'}
    historyMusic = {'value': history_num, 'name': 'Total Number in History'}
    result = [likeMusicInHistory, historyMusic]
    return jsonify(result)


@bp.route('/accDuration', methods=['POST'])
@token_auth.login_required
def update_Accumulation_Duration():
    data = request.get_json()
    userID = data.get('userID')
    new = data.get('counter')
    print(userID, new)
    getUser = User.query.get_or_404(userID)
    getUser.accumulate_duration += int(new)
    db.session.commit()
    convert(getUser.accumulate_duration)
    return '累积时长更新成功'


def convert(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    res = "{0}:{1:02d}:{2:02d}".format(h, m, s)
    print(res)
    return res


@bp.route('/cleanDuration', methods=['POST'])
@token_auth.login_required
def Clean_Duration():
    data = request.get_json()
    userID = data.get('userID')
    getUser = User.query.get_or_404(userID)
    getUser.accumulate_duration = 0
    db.session.commit()
    return '清除时长成功'
