import django_rq
import tempfile
import subprocess

from django.shortcuts import render, redirect
from django.core.files import File
from django.http import HttpResponse

from .forms import UploadVideoForm
from .models import Video, GifImage


def video_upload(request):
    if request.method == "POST":
        form = UploadVideoForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Video(file=request.FILES['file'])
            instance.save()
            print(instance.id)
            return redirect('video_to_gif_request', video_id=instance.id)
    else:
        form = UploadVideoForm()
        return render(request, 'upload_video.html', {'form': form})


def video_to_gif(video_id, gif_image_id):
    video_djfile = Video.objects.all().get(id=video_id)
    video_tmp_file = tempfile.NamedTemporaryFile()

    video_tmp_file.write(video_djfile.file.read())
    video_tmp_file.flush()

    gif_tmp_file = tempfile.NamedTemporaryFile(suffix=".gif")

    ffmpeg = ["ffmpeg", "-t", "00:00:10", "-y", "-i", video_tmp_file.name, gif_tmp_file.name]

    proc = subprocess.Popen(ffmpeg)
    try:
        out, err = proc.communicate(timeout=100)
    except TimeoutExpired:
        proc.kill()

    gif_tmp_file.seek(0)
    GifImage.objects.all().get(id=gif_image_id).file.save(
        'new',
        File(gif_tmp_file)
    )

    gif_tmp_file.close()
    video_tmp_file.close()


def video_to_gif_request(request, video_id):
    gif_image = GifImage(video_id=video_id)
    gif_image.save()
    django_rq.enqueue(video_to_gif, video_id=video_id, gif_image_id=gif_image.id)
    return HttpResponse("AAAAAAAAAAAAAAAAAAAAAAaaa")
