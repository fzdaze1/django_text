from django.db import models


class Queries(models.Model):
    # Уникальный запрос, который будет выступать как PK
    query = models.CharField(max_length=255, unique=True)
    # Путь к видеофайлу, если оно создано
    video_path = models.CharField(max_length=500, default='')

    def __str__(self):
        return self.query
