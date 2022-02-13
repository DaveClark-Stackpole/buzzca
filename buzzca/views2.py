from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from datetime import datetime




# Call Main Login screen
def test(request):
	
	return render(request, "/templates/test4.html")
