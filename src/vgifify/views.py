import django_rq
import tempfile
import subprocess
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.core.files import File
from django.http import HttpResponse, Http404

from .forms import UploadVideoForm, ConvertForm
from .models import Video, GifImage


def video_upload(request):
    if request.method == "POST":
        form = UploadVideoForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Video(file=request.FILES['file'])
            instance.save()
            return redirect('convert', video_id=instance.id)
    else:
        form = UploadVideoForm()
        return render(request, 'index.html')


def convert(request, video_id):
    if request.method == "POST":
        form = ConvertForm(request.POST, request.FILES)
        if form.is_valid():
            result = GifImage(video_id=video_id)
            result.save()
            django_rq.enqueue(video_to_gif, gif_image_id=result.id, framerate=request.POST.get("framerate"))
            return redirect('convert_result', result_id=result.id)
    else:
        form = ConvertForm()
        return render(request, 'video.html', {'video_id': video_id})


def video_to_gif(gif_image_id, framerate):
    gif_image_obj = GifImage.objects.all().get(id=gif_image_id)

    video_djfile = gif_image_obj.video
    video_tmp_file = tempfile.NamedTemporaryFile()

    video_tmp_file.write(video_djfile.file.read())
    video_tmp_file.flush()

    gif_tmp_file = tempfile.NamedTemporaryFile(suffix=".gif")

    ffmpeg = ["ffmpeg", "-r", framerate, "-t", "00:00:10", "-y", "-i", video_tmp_file.name, gif_tmp_file.name]

    proc = subprocess.Popen(ffmpeg)
    try:
        out, err = proc.communicate(timeout=100)
    except TimeoutExpired:
        proc.kill()

    gif_tmp_file.seek(0)
    gif_image_obj.file.save('new', File(gif_tmp_file))

    gif_tmp_file.close()
    video_tmp_file.close()


def convert_result(request, result_id):
    result = get_object_or_404(GifImage, id=result_id)

    if not result:
        raise Http404()

    return render(request, 'gif_result.html', {'result_id': result_id})


def convert_result_file(request, result_id):
    result = get_object_or_404(GifImage, id=result_id)

    if not result.file:
        raise Http404()

    response = HttpResponse(
        result.file.read(),
        content_type='image/gif'
    )
    return response


def convert_result_check(request, result_id):
    result = get_object_or_404(GifImage, id=result_id)
    return HttpResponse(json.dumps({'ready': bool(result.file)}))
