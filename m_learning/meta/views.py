from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from meta.models import Artist
from meta.tables import ArtistTable
from django_tables2   import RequestConfig


# def index(request):
#     queryset = Artist.objects.all()
#     table = ArtistTable(queryset)

#     return render("index.html", {"table": table})

    # return render(request, "artists.html", {"artists": Artist.objects.all()})

def artists(request):
    table = ArtistTable(Artist.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'artists.html', {'table': table})

# def simple_list(request):
#     queryset = Simple.objects.all()
#     table = SimpleTable(queryset)


# def view_artist(request, slug):   
#     return render_to_response('view_artist.html', {
#         'post': get_object_or_404(Artist, slug=slug)
#     })

# Create your views here.
