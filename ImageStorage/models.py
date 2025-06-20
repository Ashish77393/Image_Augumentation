from django.db import models


class ImageFile(models.Model):
    img = models.ImageField(upload_to='images/')
