from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse

class Product(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    pub_date = models.DateTimeField(default=timezone.now)
    votes = models.ManyToManyField(User)
    image = models.ImageField(upload_to='images/products/')
    icon = models.ImageField(upload_to='images/products/icons/')
    body = models.TextField()
    hunter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

    def summery(self):
        return self.body[:100] + '...'

    def pub_date_pretty(self):
        return self.pub_date.strftime("%d %B %Y")

    class Meta:
        ordering = ('-pub_date',)

class CommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(parent=None)

class Comment(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name='childrens', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    receiver = models.ForeignKey(User, on_delete=None, related_name='recived_comments', blank=True, null=True)
    content = models.TextField('Комментарий')
    pub_date = models.DateTimeField('Дата комментария', default=timezone.now)

    objects = models.Manager() # The default manager.
    first_level = CommentManager() # Get all comments without parents.

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.content[0:200]

    @property
    def get_col_length(self):
        if self.parent is not None:
            return 10
        return 12

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
