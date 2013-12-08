import django_tables2 as tables
from meta.models import Artist

class ArtistTable(tables.Table):
    class Meta:
        model = Artist
        # add class="paleblue" to <table> tag
        # attrs = {"class": "paleblue"}