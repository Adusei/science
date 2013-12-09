from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from listen.models import Sound
from listen.tables import SoundTable
from django_tables2   import RequestConfig
from django.template import RequestContext
from django.http import HttpResponse


def basic (request): 
  rand_pk = Sound.objects.order_by('?')[0].id
  sound = get_object_or_404(Sound, pk=rand_pk)
  return render(request, 'index.html', {'sound': sound})


def sounds(request):
    table = SoundTable(Sound.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'sounds.html', {'table': table})

def search(request): # http://www.djangobook.com/en/2.0/chapter07.html
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            books = Book.objects.filter(title__icontains=q)
            return render(request, 'search_results.html',
                {'books': books, 'query': q})
    return render(request, 'search_form.html',
        {'error': error})

