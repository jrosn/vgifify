from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.video_upload, name='video_upload'),

    url(
        r'^video_to_gif_request/(?P<video_id>\d+)$',
        views.video_to_gif_request,
        name='video_to_gif_request'
    ),

    # url(
    #     r'^result/(?P<gif_image_id>\d+)$',
    #     views.gif_image_deffered,
    #     name='gif_image_deffered'
    # ),

    url(
        r'^result/(?P<gif_image_id>\d+)/check$',
        views.gif_image_check,
        name='gif_image_check'
    ),

    url(
        r'^result/(?P<gif_image_id>\d+)/gif$',
        views.gif_image,
        name='gif_image'
    ),
]
