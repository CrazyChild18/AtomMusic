import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'), encoding='utf-8')
UPLOAD_FOLDER = '../front-end/public/avatar/'

sqlalchemy_address = 'sqlite:///' + os.path.join(basedir, 'musicData.db')
# 0不输出, 1输出ERROR, 2输出WARNING、ERROR, 3输出INFO、WARNING、ERROR
log_level = 3
audio_extension = ".mp3"
audio_frame_rate = 44100
# 多线程的时候用的线程数
multi_thread_num = 128
# 插入数据量
sqlite_insert_num = 20000
support_audio = [".mp3", ".wav"]
search_subdirectories = True
# Size of the FFT window
fft_window_size = 4096
# the ratio of overlapping area of a window size
fft_overlap_ratio = 0.5
# fingerprint_number = 15
# higher the value is less the number of peak is. less accuracy
minimun_peak_amplitude = 10  # 20
peak_neighborhood_size = 20  # 25
# important: find correct target zone will hugely effect the result
time_constraint_condition = (9, 200)  # (min,max) (9,200)
# freqs_constraint_condition = (min, max)  # not use. unneccessary
fanout_factor = 15  # 20
# max 64(using sha256)
fingerprint_cutoff = 0
# minimum match num for song recognize
min_match_num = 1


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'atom.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
