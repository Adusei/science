from django.db import models
import django_tables2 as tables
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS


class Sound(models.Model):
    title = models.CharField(max_length=255, unique=False) #This should be fixed in the insert...
    sc_id = models.IntegerField(max_length=100, unique=True)
    # THIS IS JUST SO I CAN GET THE RECOMMENDER WORKING #
    jd_fav_flag = models.BooleanField(default=0)
    jd_follows_like_count = models.IntegerField(max_length=100, unique=False, default=None)

    # duration_mins = models.DecimalField(decimal_places=5,max_digits=5)
    # ranker = models.DecimalField(decimal_places=5,max_digits=5,null=True, default=None)

    def __unicode__(self):
        # return '%s' % self.name
        return self

class SoundTable(tables.Table):
    class Meta:
        model = Sound 


