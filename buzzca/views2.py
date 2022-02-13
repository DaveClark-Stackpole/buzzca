from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from datetime import datetime

from django.core.context_processors import csrf
import smtplib
from smtplib import SMTP


# Call Main Login screen
def test(request):
	
	return render(request, "test4.html")
