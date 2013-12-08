from django.db import models

class Sound(models.Model):
    title = models.CharField(max_length=100, unique=True,)
    sc_id = models.IntegerField(max_length=100, unique=True,)

    def __unicode__(self):
        # return '%s' % self.name
        return self