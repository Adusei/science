from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from meta.models import Artist
from meta.tables import ArtistTable
from django_tables2   import RequestConfig

def artists(request):
    table = ArtistTable(Artist.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'artists.html', {'table': table})



