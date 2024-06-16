import os
import logging
import datetime
from dotenv import load_dotenv

load_dotenv() # Load .env file

logger = logging.getLogger(__name__)

class SettingsService:
    def __init__(self):

        self.__create_folders()
        self.__set_variables()

        logger.info("[CONFIG][PATHS][DATA] '%s'", self.data_path)
        logger.info("[CONFIG][PATHS][IN DATA] '%s'", self.in_data_path)
        logger.info("[CONFIG][PATHS][OUT DATA] '%s'", self.out_data_path)
        logger.info("[CONFIG][PATHS][TMP DATA] '%s'", self.tmp_data_path)


        logger.info("[CONFIG][FILES][IN MOVIE] '%s'", self.in_movie)
        logger.info("[CONFIG][FILES][IN MOVIE LANG] '%s'", self.in_movie_lang)

        if self.__out_transcription is None:
            logger.info("[CONFIG][FILES][OUT TRANSCRIPTION] 'transcript-{yyyyMMddHHmmss}.txt'")
        else:
            logger.info("[CONFIG][FILES][OUT TRANSCRIPTION] '%s'", self.get_out_transcription())

        logger.info("[CONFIG][CHUNK][SIZE] Size: '%s' - Overlap: '%s'", self.chunk_size, self.overlap_duration)


    def __create_folders(self):
        # Define the base path starting from the root directory. E.g. '\'
        self.data_path = os.path.join(os.path.sep)
        self.data_path = os.path.join(self.data_path, 'data')
        self.in_data_path = os.path.join(self.data_path, 'in-data')
        self.out_data_path = os.path.join(self.data_path, 'out-data')
        self.tmp_data_path = os.path.join(self.data_path, 'tmp-data')


        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
            logger.debug("[CONFIG][PATHS][DATA] '%s' created", self.data_path)

        if not os.path.exists(self.in_data_path):
            os.makedirs(self.in_data_path)
            logger.debug("[CONFIG][PATHS][IN DATA] '%s' created", self.in_data_path)

        if not os.path.exists(self.out_data_path):
            os.makedirs(self.out_data_path)
            logger.debug("[CONFIG][PATHS][OUT DATA] '%s' created", self.out_data_path)

        if not os.path.exists(self.tmp_data_path):
            os.makedirs(self.tmp_data_path)
            logger.debug("[CONFIG][PATHS][TMP DATA] '%s' created", self.tmp_data_path)


    def __set_variables(self):
        self.in_movie = os.environ.get('IN_MOVIE')
        if self.in_movie is None or self.in_movie == '':
            self.in_movie = os.path.join(self.in_data_path, 'movie.mp4')
        else:
            self.in_movie = os.path.join(self.in_data_path, self.in_movie)

        if not os.path.exists(self.in_movie):
            logger.error("[CONFIG][FILES][IN MOVIE] File not found: '%s'", self.in_movie)
            exit(1)

        self.__out_transcription = os.environ.get('OUT_TRANSCRIPT')

        self.in_movie_lang = os.environ.get('IN_MOVIE_LANG', 'en-US')

        self.chunk_size = os.environ.get('CHUNK_SIZE')
        if self.chunk_size is None or self.chunk_size == '':
            self.chunk_size = None
        self.overlap_duration = max(int(os.environ.get('OVERLAP_DURATION', 2)), 0)



    def get_out_transcription(self):
        if self.__out_transcription is None:
            date = datetime.datetime.now()
            formatted_date = date.strftime('%Y%m%d%H%M%S')
            return os.path.join(self.out_data_path, f'transcript-{formatted_date}.txt')
        else:
            return os.path.join(self.out_data_path, self.__out_transcription)
