from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Product(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    pub_date = models.DateTimeField(default=timezone.now)
    votes = models.ManyToManyField(User)
    image = models.ImageField(upload_to='images/products/')
    icon = models.ImageField(upload_to='images/products/icons/')
    body = models.TextField()
    hunter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title

    def summery(self):
        return self.body[:100] + '...'

    def pub_date_pretty(self):
        return self.pub_date.strftime("%d %B %Y")
