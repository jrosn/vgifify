from django.db import models


class Video(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField()


class GifImage(models.Model):
    IN_PROGRESS_STATUS = 'IP'
    OK_STATUS = 'OK'
    ERROR_STATUS = 'ER'
    STATUSES = (
        (IN_PROGRESS_STATUS, "In progress"),
        (OK_STATUS, "OK"),
        (ERROR_STATUS, "Error")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUSES)
    video = models.ForeignKey(Video)
    file = models.FileField()
