from django.db import models


class Feedback(models.Model):
    full_name = models.CharField(max_length=221)
    position = models.CharField(max_length=221)
    avatar = models.ImageField(upload_to='feedback/')
    message = models.TextField()

    def __str__(self):
        return self.full_name
