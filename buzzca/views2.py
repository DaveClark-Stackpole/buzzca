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
def member_signup_initial(request):
	request.session['registration_check'] = 0
	request.session['redirect'] = 'member_signup'
	return render(request,'redirect.html')

def member_signup(request):
	if 'button1' in request.POST:
		login_name = request.POST.get("login_name")
		login_company = request.POST.get("login_company")
		login_email = request.POST.get("login_email")
		request.session['login_name'] = login_name
		request.session['login_company'] = login_company
		request.session['login_email'] = login_email

		request.session['redirect'] = 'member_register_check'
		return render(request,'redirect.html')

		# member_preregister(request,login_name,login_company,login_email)  # Module to register name, company and email in db but leave unverified until email verification.



	elif 'button2' in request.POST:
		request.session['redirect'] = 'main'
		return render(request,'redirect.html')
	else:
		form = login_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	request.session["login_name"] = ""
	request.session["login_password"] = ""
	request.session['test8'] = 1
	return render(request,'member_signup.html', args)

def member_register_check(request):
	login_company = request.session['login_company']
	login_email = request.session['login_email']
	login_name = request.session['login_name']
	db, cur = db_set(request)
	cur.execute("""CREATE TABLE IF NOT EXISTS member_data(Id INT PRIMARY KEY AUTO_INCREMENT,name CHAR(80), company CHAR(80), email CHAR(80), type CHAR(80), verified INT(10))""")
	sql = "SELECT COUNT(*) FROM member_data where company = '%s'" %(login_company)
	cur.execute(sql)
	tmp = cur.fetchall()
	company_count = int(tmp[0][0])
	sql = "SELECT COUNT(*) FROM member_data where email = '%s'" %(login_email)
	cur.execute(sql)
	tmp = cur.fetchall()
	company_email = int(tmp[0][0])
	db.close()

	if company_count > 0:
		request.session['registration_check'] = 1
	elif company_email > 0:
		request.session['registration_check'] = 2
	else:
		request.session['redirect'] = 'member_preregister'
		return render(request,'redirect.html')

	request.session['redirect'] = 'member_signup'
	return render(request,'redirect.html')

def member_preregister(request):
	login_company = request.session['login_company']
	login_email = request.session['login_email']
	login_name = request.session['login_name']
	v = 0
	t = 'admin'
	db, cur = db_set(request)
	cur.execute('''INSERT INTO member_data(name,company,email,type,verified) VALUES(%s,%s,%s,%s,%s)''', (login_name,login_company,login_email,t,v))
	db.commit()
	db.close()
	return render(request,'member_preregister.html') 





