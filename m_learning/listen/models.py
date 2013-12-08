from django.db import models

class Sound(models.Model):
    title = models.CharField(max_length=100, unique=True)
    sc_id = models.IntegerField(max_length=100, unique=True)
    duration_mins = models.DecimalField(decimal_places=5,max_digits=5)
    jd_following_fav_count = models.IntegerField()
    ranker = models.DecimalField(decimal_places=5,max_digits=5)

    def __unicode__(self):
        # return '%s' % self.name
        return self


