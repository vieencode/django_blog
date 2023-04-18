from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager 
from django.contrib.auth.models import User 

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, 
               self).get_queryset()\
               .filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'), 
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, 
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, 
                              choices=STATUS_CHOICES,
                              default='draft')
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()
    likes = models.IntegerField(default=0)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title 

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                        args=[self.publish.year, 
                              self.publish.month,
                              self.publish.day, 
                              self.slug
                             ])
    
    def read_time(self):
        words = len(self.body.split(' '))
        words_per_min = 250
        if words <= words_per_min:
            return 1
        else:
            return int(round(words / words_per_min, 0))
