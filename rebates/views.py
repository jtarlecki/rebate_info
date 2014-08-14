from django.shortcuts import render_to_response

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def start(request):
	return render_to_response('start.html')
	
def about(request):
	return render_to_response('about.html')
	
# def api_home(request):
	# return HttpResponseRedirect(reverse('api_home'),)