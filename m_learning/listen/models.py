from django.db import models
import django_tables2 as tables
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS


class Sound(models.Model):
    title = models.CharField(max_length=100, unique=True)
    sc_id = models.IntegerField(max_length=100, unique=True)
   	# duration_mins = models.DecimalField(decimal_places=5,max_digits=5)
    # ranker = models.DecimalField(decimal_places=5,max_digits=5)

    def __unicode__(self):
        # return '%s' % self.name
        return self

class SoundTable(tables.Table):
    class Meta:
        model = Sound 

