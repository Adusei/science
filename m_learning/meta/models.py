from django.db import models
import django_tables2 as tables
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True,)
    fb_id = models.CharField(max_length=100, unique=True,null=True,default=None)
    sc_id = models.CharField(max_length=100, unique=True,null=True,default=None)
    ra_id = models.CharField(max_length=100, unique=True,null=True,default=None)

    # slug = models.SlugField(max_length=100, unique=True)
    # timestamp = models.DateTimeField(db_index=True, auto_now_add=True)

    def __unicode__(self):
        # return '%s' % self.name
        return self

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    fb_id = models.CharField(max_length=100, unique=True,null=True,default=None)
    ra_id = models.CharField(max_length=100, unique=True,null=True, default=None)
    description = models.CharField(max_length=100, unique=True,null=True,default=None)

    # slug = models.SlugField(max_length=100, unique=True)
    # timestamp = models.DateTimeField(db_index=True, auto_now_add=True)

    def __unicode__(self):
        return '%s' % self.name

class Artist_to_genre(models.Model):
    ## Fix this!
    artist_id = models.IntegerField(max_length=100)
    genre_id = models.IntegerField(max_length=100)

    def __unicode__(self):
        return '%s' % self.name

class ArtistTable(tables.Table):
    class Meta:
        model = Artist 






# class Artist_to_genre(models.Model):
#     def __unicode__(self):
#         return '%s' % self.artit_id


    # @permalink
    # def get_absolute_url(self):
    #     return ('view_blog_post', None, { 'slug': self.slug })
