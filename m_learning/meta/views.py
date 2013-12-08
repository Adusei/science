from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from meta.models import Artist

def index(request):
    return render_to_response('index.html', {
        'artist': Artist.objects.all()[:5]
    })

def view_artist(request, slug):   
    return render_to_response('view_artist.html', {
        'post': get_object_or_404(Artist, slug=slug)
    })

# Create your views here.
