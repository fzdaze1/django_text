
from django.shortcuts import render
from .forms import QueryCreateForm
from .models import Queries
from .utils.video_handler import create_video_opencv, transliterate_only_letters
from django.http import FileResponse, Http404
from django.core.files.storage import default_storage
import os
from django.conf import settings
from django.utils.encoding import smart_str


def video_view(request):
    if request.method == 'POST':
        form = QueryCreateForm(request.POST)
        query_text = request.POST.get('query')
        try:
            query_instance = Queries.objects.get(query=query_text)
            download_url = f"/download_video/{query_instance.query}"
            return render(request, 'main.html', {
                'form': form,
                'download_url': download_url,
                'video_created': False,
                'video_exists': True
            })
        except Queries.DoesNotExist:
            if form.is_valid():
                query_instance = Queries(query=query_text)
                video_info = create_video_opencv(query_instance.query)
                query_instance.video_path = video_info['path']
                query_instance.save()
                download_url = f"/download_video/{query_instance.query}"
                return render(request, 'main.html', {
                    'form': form,
                    'download_url': download_url,
                    'video_created': True,
                    'video_exists': False
                })
    form = QueryCreateForm()
    return render(request, 'main.html', {'form': form, 'video_created': False, 'video_exists': False})


def download_video_view(request, video_title):
    try:
        query_instance = Queries.objects.get(query=video_title)
    except Queries.DoesNotExist:
        raise Http404("Видео не найдено.")
    video_path = os.path.join(
        settings.BASE_DIR, f'media/{query_instance.video_path}')
    print(video_path)
    if not os.path.exists(video_path):
        raise Http404("Видео не найдено.")
    video_file = default_storage.open(query_instance.video_path, 'rb')
    response = FileResponse(video_file, content_type='video/mp4')
    response['Content-Disposition'] = f'attachment; filename="{smart_str(transliterate_only_letters(video_title))}.mp4"'
    return response
