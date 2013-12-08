from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True,)
    fb_id = models.CharField(max_length=100, unique=True,null=True,default=None)
    sc_id = models.CharField(max_length=100, unique=True,null=True,default=None)
    ra_id = models.CharField(max_length=100, unique=True,null=True,default=None)

    # slug = models.SlugField(max_length=100, unique=True)
    # timestamp = models.DateTimeField(db_index=True, auto_now_add=True)

    def __unicode__(self):
        return '%s' % self.name

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    fb_id = models.CharField(max_length=100, unique=True,null=True,default=None)
    ra_id = models.CharField(max_length=100, unique=True,null=True, default=None)
    description = models.CharField(max_length=100, unique=True,null=True,default=None)

    # slug = models.SlugField(max_length=100, unique=True)
    # timestamp = models.DateTimeField(db_index=True, auto_now_add=True)

    def __unicode__(self):
        return '%s' % self.name

# class Artist_to_genre(models.Model):
#     artist_id = models.CharField(max_length=100, unique=True)
#     artist_id = models.CharField(max_length=100, unique=True)

#     slug = models.SlugField(max_length=100, unique=True)
#     timestamp = models.DateTimeField(db_index=True, auto_now_add=True)

#     def __unicode__(self):
#         return '%s' % self.name









# class Artist_to_genre(models.Model):
#     def __unicode__(self):
#         return '%s' % self.artit_id


    # @permalink
    # def get_absolute_url(self):
    #     return ('view_blog_post', None, { 'slug': self.slug })
