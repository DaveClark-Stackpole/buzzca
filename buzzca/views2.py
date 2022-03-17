from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from datetime import datetime
# from django.core.context_processors import csrf

from django.template.context_processors import csrf


from buzzca.forms import login_Form
import os
import time
from buzzca.views_db import db_set
import MySQLdb

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


# Call Main Login screen
def main(request):
	# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	# BASE_DIR = BASE_DIR + '\\static\\buzzca'
	# # t=4/0
	# dir = BASE_DIR
	# p=8/0



	# db, cur = db_set(request)

	# a = 'Dave'
	# b = 10
	# cur.execute("""CREATE TABLE IF NOT EXISTS test_A(Id INT PRIMARY KEY AUTO_INCREMENT,variable_A VARCHAR(80), number_A INT(30))""")
	# cur.execute('''INSERT INTO test_A(variable_A,number_A) VALUES(%s,%s)''', (a,b))
	# db.commit()
	# db.close()


	t=int(time.time())
	request.session['TCURR'] = t

	request.session['secondary_menu_color']='#A0AEB8'
	request.session['secondary_text_color'] ='#000000'
	request.session['main_menu_color'] ='#BCCAD5'
	return render(request, "main.html",)

def member_login(request):


	if 'button1' in request.POST:

		login_name = request.POST.get("login_name")
		login_password = request.POST.get("login_password")
		e=3/0
		request.session["login_name"] = login_name
		request.session["login_password"] = login_password
		request.session['main_login_verify'] = 1
		
		login_initial(request,login_name)
		return main(request)
		
	elif 'button2' in request.POST:
		ee=3/0
		request.session["password_lost_route1"] = "main_log.html"
		return render(request,'login/reroute_lost_password.html')

	else:
		form = login_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	request.session["login_name"] = ""
	request.session["login_password"] = ""

	return render(request,'member_login.html', args)


