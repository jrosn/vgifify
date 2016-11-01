from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.video_upload, name='video_upload'),

    url(
        r'^convert/(?P<video_id>\d+)$',
        views.convert
    ),

    url(
        r'^convert/(?P<video_id>\d+)$',
        views.convert,
        name='convert'
    ),

    url(
        r'^convert/result/(?P<result_id>\d+)$',
        views.convert_result,
        name='convert_result'
    ),

    url(
        r'^convert/result/(?P<result_id>\d+)/check$',
        views.convert_result_check,
        name='convert_result_check'
    ),

    url(
        r'^convert/result/(?P<result_id>\d+)/file$',
        views.convert_result_file,
        name='convert_result_file'
    ),
]
