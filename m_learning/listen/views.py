from django.shortcuts import render,render_to_response
from listen.models import Sound



# Create your views here.

def basic(request):
	return render_to_response("index.html", request)#, {"sound": Sound.objects.all()})

