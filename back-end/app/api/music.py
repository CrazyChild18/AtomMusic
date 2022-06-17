import datetime
import json
import time

from flask import request, jsonify
import requests
from app.api import bp
import config
# 安装检测环境后释放此注释，并在最后的函数中调用来开始检测
import test


# def is_contain_chinese(check_str):
#     """
#     判断字符串中是否包含中文
#     :param check_str: {str} 需要检测的字符串
#     :return: {bool} 包含返回True， 不包含返回False
#     """
#     for ch in check_str:
#         if u'\u4e00' <= ch <= u'\u9fff':
#             return True
#     return False


@bp.route('/getMusic', methods=['POST'])
def getMusicList():
    """初始化10个歌曲，并保存在列表中"""
    data = request.get_json()
    url = data.get("url")
    # 使用requests向第三方服务器发送请求
    res = requests.get(url).content
    data_res = json.loads(res)
    musicList = data_res["data"]
    musicIDList = []  # 用来存储初始化的10个音乐id
    musicNameList = []  # 用来储存初始化的10个音乐名字
    musicPicList = []  # 用来储存初始化10个音乐的封面地址
    musicWriterList = []  # 用来储存初始化10个音乐作者（存在一个歌曲多个作者情况）
    musicUrlList = []  # 用来储存初始化的10个音乐链接
    for musicItem in musicList[:10]:
        musicIDList.append(musicItem["id"])
        musicNameList.append(musicItem["name"])
        # musicUrlList.append(musicItem["mp3Url"])
        album = musicItem["album"]
        musicPicList.append(album["picUrl"])
        artists = album["artists"]
        writer = []
        for i in artists:
            writer.append(i["name"])
        musicWriterList.append(writer)
    requestUrl = "https://autumnfish.cn/song/url?id="
    for musicID in musicIDList:
        resUrl = requests.get(requestUrl + str(musicID)).content
        json_res = json.loads(resUrl)
        urlList = json_res["data"]
        for urlItem in urlList:
            musicUrlList.append(urlItem["url"])
    resultList = []
    for Id, Pic, Name, Writer, Url in zip(musicIDList, musicPicList, musicNameList, musicWriterList, musicUrlList):
        item = {"id": Id, "name": Name, "picUrl": Pic, "writer": Writer, "url": Url}
        resultList.append(item)
    return jsonify(resultList)
    # return jsonify(musicList)


@bp.route('/loginMusic', methods=['POST'])
def loginMusic():
    """网易云后台账户登录"""
    res = requests.get("https://autumnfish.cn/login/cellphone?phone=13910831098&password=liyunkai720").content
    jsonRes = json.loads(res)
    loginCode = jsonRes["code"]
    if loginCode == 200:
        result = "successful"
    else:
        result = jsonRes["msg"]
    return result


@bp.route('/getMusicDetail', methods=['POST'])
def getMusicDetail():
    """获取指定歌曲详情"""
    data = request.get_json()
    url = data.get("url")
    musicId = data.get("id")
    # 使用requests向第三方服务器发送请求
    res = requests.get(url + str(musicId)).content
    json_res = json.loads(res)
    songs = json_res["songs"]
    songsItem = songs[0]
    al = songsItem["al"]
    musicName = al["name"]  # 歌曲名称
    musicPic = al["picUrl"]  # 歌曲封面
    ar = songsItem["ar"]
    writers = []
    for i in ar:
        writers.append(i["name"])
    details = {"musicName": musicName, "musicPic": musicPic, "writers": writers}
    return jsonify(details)


@bp.route('/getMusicUrl', methods=['POST'])
def getMusicUrl():
    """获取指定歌曲链接"""
    data = request.get_json()
    url = data.get("url")
    musicId = data.get("id")
    print(musicId)
    # 使用requests向第三方服务器发送请求
    resUrl = requests.get(url + str(musicId)).content
    json_res = json.loads(resUrl)
    data = json_res["data"]
    res = data[0]
    result = res["url"]
    return result


@bp.route('/getMusiclyric', methods=['POST'])
def getMusiclyric():
    """获取指定歌曲歌词"""
    data = request.get_json()
    url = data.get("url")
    musicId = data.get("id")
    # 使用requests向第三方服务器发送请求
    resUrl = requests.get(url + str(musicId)).content
    json_res = json.loads(resUrl)
    lrc = json_res["lrc"]
    lyric = lrc["lyric"]
    return lyric


@bp.route('/searchHostList', methods=['POST'])
def getSearchHostList():
    """获取热搜列表"""
    url = 'https://autumnfish.cn/search/hot'

    # 使用requests向第三方服务器发送请求
    res_url = requests.get(url).content
    json_res = json.loads(res_url)
    result = json_res["result"]
    hots = result["hots"]
    return_list = []
    for item in hots:
        word = item["first"]
        return_list.append(word)
    return jsonify(return_list)


@bp.route('/searchWord', methods=['POST'])
def searchWord():
    """指定关键词搜索"""
    data = request.get_json()
    wordList = data.get("keyword")
    url = 'https://autumnfish.cn/cloudsearch?keywords='
    # 使用requests向第三方服务器发送请求
    res = requests.get(url + wordList).content
    json_res = json.loads(res)
    result = json_res["result"]
    songs = result["songs"]
    resultList = []
    num = 0
    for i in songs:
        if num < 10:
            item = {}
            item["musicName"] = i["name"]  # 储存音乐名字
            musicAuthor = i["ar"]
            if len(musicAuthor) > 1:
                item["musicArtist"] = musicAuthor[0]["name"] + "..."
            else:
                item["musicArtist"] = musicAuthor[0]["name"]
            item["id"] = i["id"]
            resultList.append(item)
            num = num + 1
            print(item["id"])
    return jsonify(resultList)


@bp.route('/uploadMusic', methods=['POST'])
def uploadMusic():
    data = request.files.get('file')
    path = config.basedir + '/recognizeMusicUser/'
    time_str = time.mktime(datetime.datetime.now().timetuple())
    fileName = str(int(time_str)) + '.mp3'
    musicPath = path + fileName
    data.save(musicPath)
    return fileName


@bp.route('/uploadWAVMusic', methods=['POST'])
def uploadWAVMusic():
    data = request.files.get('file')
    path = config.basedir + '/recognizeMusicUser/'
    time_str = time.mktime(datetime.datetime.now().timetuple())
    fileName = str(int(time_str)) + '.wav'
    musicPath = path + fileName
    data.save(musicPath)
    return fileName


@bp.route('/recognizeMusic', methods=['POST'])
def recognizeMusic():
    data = request.get_json()
    musicName = data.get("fileName")
    path = config.basedir + '/recognizeMusicUser/'
    musicPath = path + musicName
    ans = test.testRecognize(musicPath)  # 返回结果为音乐id，字符串类型
    res = requests.get("https://autumnfish.cn/song/detail?ids=" + str(ans)).content
    json_res = json.loads(res)
    songs = json_res["songs"]
    songsItem = songs[0]
    al = songsItem["al"]
    musicName = al["name"]  # 歌曲名称
    return str(musicName)
    # return jsonify(ans)
