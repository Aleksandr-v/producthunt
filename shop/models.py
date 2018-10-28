from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit

class Good(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()

    image = ProcessedImageField(upload_to='images/goods/',
                                   processors=[ResizeToFit(209, 119)],
                                   format='JPEG',
                                   options={'quality': 100})
    image_thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFit(60, 40)],
                                      format='JPEG',
                                      options={'quality': 100})

    def __str__(self):
        return self.name

class Card(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    good = models.ForeignKey(Good, on_delete=models.CASCADE, related_name='cards')
    quantity = models.PositiveIntegerField()
