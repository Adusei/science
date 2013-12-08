import django_tables2 as tables
from listen.models import Sound

class SoundTable(tables.Table):
    class Meta:
        model = Sound
        attrs = {"class": "paleblue"}