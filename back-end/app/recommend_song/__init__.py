# 此模块功能
# 给定任意歌曲的音频文件
# 预测其种类, 得到其频谱图
# 将其频谱图转换为特征向量，并求出其平均特征向量
# 导入已有数据集的平均特征向量矩阵
# 求待推荐音频与已知数据集中音频的相似度
# 取相似度最高的作为推荐

# 所有数据保存在 目录 cf_data 下
# model_files 模型文件目录
#   final_data.pkl 歌曲信息文件
# average_feature_arrays
#   数据集的平均特征向量存放目录
# prediction_track 待预测歌曲产生的信息的目录


import os
from app.recommend_song import get_genre, get_feature_vector, recommend


class Recommender(object):
    """docstring for Recommendation
    推荐管理类
    """

    def __init__(self, music_path):
        super(Recommender, self).__init__()
        if not os.path.exists(music_path):
            raise RuntimeError("Track path not exists: {}".format(music_path))
        self.path_track = music_path
        base_path_track = os.path.basename(music_path)
        self.song_id = base_path_track.split(".")[0]
        self.get_genre = get_genre.GetGenre(self.path_track)
        self.get_feature_vector = get_feature_vector.GetFeatureVector(self.song_id)
        self.make_recommendation = recommend.MakeRecommendation(self.song_id)

    def recommend_sim_songs(self):
        track_genre = self.get_genre.analyse_track()
        track_genre_name, confidence = track_genre
        self.get_feature_vector.get_feature()
        return track_genre, self.make_recommendation.recommend(track_genre_name.lower())
