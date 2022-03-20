from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from datetime import datetime
# from django.core.context_processors import csrf

from django.template.context_processors import csrf

import smtplib
from smtplib import SMTP

from buzzca.forms import login_Form
import os
import time
from buzzca.views_db import db_set
import MySQLdb

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


# Call Main Login screen
def main(request):
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
		request.session['redirect'] = 'member_register_check'     # Redirect back to check registration validity
		return render(request,'redirect.html')

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
		request.session['redirect'] = 'member_preregister'  # If registration valid then write to database and bounce back with message
		return render(request,'redirect.html')

	request.session['redirect'] = 'member_signup'   # Registration not valid so bounce back with message based on code number
	return render(request,'redirect.html')

def member_preregister(request):
	login_company = request.session['login_company']
	login_email = request.session['login_email']
	login_name = request.session['login_name']

	login_email=str(login_email)

	

	v = 0
	t = 'admin'
	st=6
	db, cur = db_set(request)
	cur.execute('''INSERT INTO member_data(name,company,email,type,verified) VALUES(%s,%s,%s,%s,%s)''', (login_name,login_company,login_email,t,v))
	db.commit()

	sql = "SELECT Id FROM member_data where name = '%s' and company = '%s' and email = '%s'" %(login_name,login_company,login_email)
	cur.execute(sql)
	tmp = cur.fetchall()
	id1 = int(tmp[0][0])

	db.close()

	# st = 6db, cur = db_set(request)/0


	b = "\r\n"
	ctr = 0


	link1 = request.session['server_link'] + 'member_validate/get/'+str(id1)
	message_subject = 'BuzzApp Registration'
	message3 = "Congratulations " + login_name + " You  have registered for BuzzApp with your company " + login_company
	message2 = "click the link to validate your membership:   " + link1

	toaddrs = [login_email]
	#toaddrs = ["rbiram@stackpole.com","rzylstra@stackpole.com","lbaker@stackpole.com","dmilne@stackpole.com","sbrownlee@stackpole.com","pmurphy@stackpole.com","pstreet@stackpole.com","kfrey@stackpole.com","asmith@stackpole.com","smcmahon@stackpole.com","gharvey@stackpole.com","ashoemaker@stackpole.com","jreid@stackpole.com"]
	fromaddr = 'wecloud47@gmail.com'
	frname = 'Dave'
	server = SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('StackpolePMDS@gmail.com', 'stacktest6060')
	message = "From: %s\r\n" % frname + "To: %s\r\n" % ', '.join(toaddrs) + "Subject: %s\r\n" % message_subject + "\r\n" 
	message = message+message_subject + "\r\n\r\n" + "\r\n\r\n" + message3 + "\r\n\r\n" + message2
	server.sendmail(fromaddr, toaddrs, message)
	server.quit()


	return render(request,'member_preregister.html') 

def member_validate(request, index):
	v = 1
	db, cur = db_set(request)
	sql =( 'update member_data SET verified="%s" WHERE Id="%s"' % (v,index))
	cur.execute(sql)
	db.commit()
	db.close()

	request.session['redirect'] = 'main'
	return render(request,'redirect.html')