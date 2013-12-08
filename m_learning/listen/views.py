from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from listen.models import Sound
from listen.tables import SoundTable
from django_tables2   import RequestConfig
from django.template import RequestContext
from django.http import HttpResponse

def basic (request): 
	# sound_obj = Sound.objects.all()
	# return render_to_response("index.html", request, {"sound": Sound.objects.order_by('?')[0]})
	# return render_to_response("index.html"
	# 			, request
	# 			, {"sound": Sound.objects.all()}
	# 			, context_instance=RequestContext(request))#[0]})

  sound = get_object_or_404(Sound, pk=4)
  return render(request, 'index.html', {'sound': sound})


def sounds(request):
    table = SoundTable(Sound.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'sounds.html', {'table': table})



