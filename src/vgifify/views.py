import django_rq
import tempfile
import subprocess
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.core.files import File
from django.http import HttpResponse, Http404

from .forms import UploadVideoForm
from .models import Video, GifImage


def video_upload(request):
    if request.method == "POST":
        form = UploadVideoForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Video(file=request.FILES['file'])
            instance.save()
            return redirect('video_to_gif_request', video_id=instance.id)
    else:
        form = UploadVideoForm()
        return render(request, 'index.html')


def video_to_gif(video_id, gif_image_id):
    gif_image_obj = GifImage.objects.all().get(id=gif_image_id)

    video_djfile = gif_image_obj.video
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
    gif_image_obj.file.save('new', File(gif_tmp_file))

    gif_tmp_file.close()
    video_tmp_file.close()


def video_to_gif_request(request, video_id):
    gif_image = GifImage(video_id=video_id)
    gif_image.save()
    django_rq.enqueue(video_to_gif, video_id=video_id, gif_image_id=gif_image.id)
    return redirect('gif_image_deffered', gif_image.id)


def gif_image_deffered(request, gif_image_id):
    return render(request, 'gif_result.html', {'gif_image_id': gif_image_id})


def gif_image_check(request, gif_image_id):
    gif_image = get_object_or_404(GifImage, id=gif_image_id)
    return HttpResponse(json.dumps({'ready': bool(gif_image.file)}))


def gif_image(request, gif_image_id):
    gif_image = get_object_or_404(GifImage, id=gif_image_id)

    if gif_image.file is None:
        raise Http404()

    response = HttpResponse(
        gif_image.file.read(),
        content_type='image/gif'
    )
    return response
