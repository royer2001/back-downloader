import os
from pytubefix import YouTube
from pytubefix.cli import on_progress
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Ruta de la carpeta temp_videos dentro de MEDIA_ROOT
TEMP_VIDEOS_DIR = os.path.join(settings.MEDIA_ROOT, 'temp_videos')

# Asegurarse de que la carpeta exista
os.makedirs(TEMP_VIDEOS_DIR, exist_ok=True)

@api_view(['POST'])
def generate_video_link(request):
    print(settings.MEDIA_ROOT)

    url = request.data.get('url')
    if not url:
        return Response({'error': 'URL is required'}, status=400)

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        ys = yt.streams.get_audio_only()

        # Definir el nombre y la ruta del archivo en la carpeta temp_videos
        video_name = f"{yt.title}.m4a"
        video_path = os.path.join(TEMP_VIDEOS_DIR, video_name)
        print(video_path)

        # Descargar el video en la ruta especificada
        ys.download(output_path=TEMP_VIDEOS_DIR, filename=video_name)

        # Obtener el URL público para el video
        video_url = request.build_absolute_uri(f'/media/temp_videos/{video_name}')

        # Obtener el thumbnail y el título
        thumbnail_url = yt.thumbnail_url
        title = yt.title

        return Response({
            'url': video_url,
            'title': title,
            'thumbnail_url': thumbnail_url
        })

    except Exception as e:
        return Response({'error': str(e)}, status=500)
