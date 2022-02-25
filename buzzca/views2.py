from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from datetime import datetime


import os
import time

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


# Call Main Login screen
def test(request):
	# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	# # BASE_DIR = BASE_DIR + '\\static\\buzzca'
	# # t=4/0
	# dir = BASE_DIR
	# p=8/0
	t=int(time.time())
	request.session['TCURR'] = t

	return render(request, "test4.html",)
