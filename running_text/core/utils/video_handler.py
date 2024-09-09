import cv2
import numpy as np
import transliterate
from django.http import FileResponse, Http404
from django.core.files.storage import default_storage
from django.utils.encoding import smart_str
from django.conf import settings
import os


def transliterate_only_letters(text):
    translit_ru = transliterate.get_translit_function('ru')

    return translit_ru(text, reversed=True)


def create_video_opencv(message: str):
    if len(message) > 50:
        file_title = message[:50]
    elif len(message) == 0:
        file_title = 'empty-video'
    else:
        file_title = message

    file_title_transliterated = transliterate_only_letters(message)
    width, height = 100, 100
    fps = 24
    duration = 3
    num_frames = duration * fps

    video_folder = os.path.join(settings.BASE_DIR, 'media/videos')
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)

    video_path = os.path.join(video_folder, f"{file_title_transliterated}.mp4")

    if os.path.exists(video_path):
        return {'title': file_title_transliterated, 'path': f"videos/{file_title_transliterated}.mp4"}

    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(
        *'mp4v'), fps, (width, height))

    frame = np.zeros((height, width, 3), dtype=np.uint8)

    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 1
    font_thickness = 1
    font_color = (255, 255, 255)

    text_size = cv2.getTextSize(message, font, font_scale, font_thickness)
    text_width = text_size[0][0]

    initial_speed = (width + text_width) / (duration * fps)
    x, y = width, height // 2

    for _ in range(num_frames):
        frame.fill(0)
        cv2.putText(frame, message, (int(x), y), font,
                    font_scale, font_color, font_thickness)
        out.write(frame)
        x -= initial_speed
    out.release()
    print(file_title_transliterated)
    return {'title': file_title_transliterated, 'path': f"videos/{file_title_transliterated}.mp4"}


def download_video(request, video_title):
    file_title_transliterated = transliterate.slugify('ъ' + video_title)
    video_path = os.path.join(
        settings.BASE_DIR, f'media/videos/{file_title_transliterated}.mp4')

    if not os.path.exists(video_path):
        raise Http404("Видео не найдено.")

    video_file = default_storage.open(
        f"videos/{file_title_transliterated}.mp4", 'rb')

    # Отправляем файл на скачивание
    response = FileResponse(video_file, content_type='video/mp4')
    response['Content-Disposition'] = f'attachment; filename="{smart_str(video_title)}.mp4"'
    return response
