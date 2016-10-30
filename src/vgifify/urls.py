from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.video_upload, name='video_upload'),

    url(
        r'^video_to_gif_request/(?P<video_id>\d+)$',
        views.video_to_gif_request,
        name='video_to_gif_request'
    ),
]
