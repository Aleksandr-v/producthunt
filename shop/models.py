from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Good(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/goods/')
    description = models.TextField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Card(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    good = models.ForeignKey(Good, on_delete=models.CASCADE, related_name='cards')
    quantity = models.PositiveIntegerField()
