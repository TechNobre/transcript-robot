import logging
import os
from SettingsService import SettingsService
import speech_recognition as sr
import moviepy.editor as mp
import math

from TimeHelper import format_duration


logging.basicConfig(
    level = logging.DEBUG,
    format = '%(levelname)s %(message)s')
logger = logging.getLogger(__name__)

logger.info("[APP] Transcript Robot starting...")

settings = SettingsService()


video = mp.VideoFileClip(settings.in_movie)

# Round seconds to the nearest integer
total_seconds = math.ceil(video.audio.duration)

logger.info("[APP] Video loaded. '%s", format_duration(total_seconds))


file_audios = []

if settings.chunk_size:
    chunk_size = int(settings.chunk_size)

    count_chunks = 0
    current_time = 0
    while current_time < total_seconds:
        count_chunks += 1

        start = max(0, current_time - settings.overlap_duration)

        original_end = min(current_time + chunk_size, total_seconds)
        end = min(original_end + settings.overlap_duration, total_seconds)


        current_file =  os.path.join(settings.tmp_data_path, f'audio_{count_chunks:02}.wav')

        chunk = video.subclip(
            t_start = start,
            t_end = (None if end >= video.audio.duration else end))

        chunk.audio.write_audiofile(
            current_file,
            codec='pcm_s16le', # 'pcm_s16le' -> 16-bit / 'pcm_s32le' -> 32-bit wav
            bitrate='64k',
            fps=16000)

        file_audios.append(current_file)

        logger.info(
            "[APP][AUDIO][SPLIT] Audio extracted - Chunk(%s) - From: %s (%s) To: %s (%s) - Total: %s",
            count_chunks,
            format_duration(start),
            format_duration(current_time),
            format_duration(end),
            format_duration(original_end),
            format_duration(total_seconds))

        current_time += chunk_size

    logger.info(
        "[APP][AUDIO][SPLIT] Total chunks: %s - Total time: %s",
        count_chunks,
        total_seconds)


else:
    current_file =  os.path.join(settings.tmp_data_path, 'audio.wav')

    video.audio.write_audiofile(
        current_file,
        codec='pcm_s16le', # 'pcm_s16le' -> 16-bit / 'pcm_s32le' -> 32-bit wav
        bitrate='64k',
        fps=16000)

    file_audios.append(current_file)

    logger.info("[APP] Audio extracted. %s -> ", format_duration(total_seconds), current_file)


text_extracted = []

total_files = len(file_audios)
count_files = 0

for file in file_audios:
    count_files += 1

    file_audio = sr.AudioFile(file)

    # Use the audio file as the audio source
    r = sr.Recognizer()

    with file_audio as source:
        audio = r.record(source)
        text = r.recognize_google(
            audio,
            language = settings.in_movie_lang)

    logger.info("[APP][TRANSCRIPTION] Text extracted - File(%s/%s) - %s", count_files, total_files, file)
    text_extracted.append(text)
    text_extracted.append('\n')


logger.info("[APP] Text extracted:")
print('\n\n')

out_transcription = settings.get_out_transcription()
file = open(out_transcription, 'w')

for text in text_extracted:
    file.write(text)
    print(text)

file.close()

print('\n\n')
logger.info("[APP] Text saved to file: " + out_transcription)
