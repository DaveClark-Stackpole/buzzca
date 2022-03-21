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

# Call Main Login screen
def main(request):
	t=int(time.time())
	request.session['TCURR'] = t
	request.session['secondary_menu_color']='#A0AEB8'
	request.session['secondary_text_color'] ='#000000'
	request.session['main_menu_color'] ='#BCCAD5'
	return render(request, "main.html",)


# **********************************************************************Member Login Section  ****************************************************
def member_login_initial(request):
	request.session['login_check'] = 0
	request.session['redirect'] = 'member_login'
	return render(request,'redirect.html')
def member_login(request):
	if 'button1' in request.POST:
		login_name = request.POST.get("login_name")
		login_company = request.POST.get("login_company")
		login_password = request.POST.get("login_password")
		request.session["login_name"] = login_name
		request.session['login_company'] = login_company
		request.session["login_password"] = login_password
		request.session['redirect'] = 'member_login_check'     # Redirect back to check login validity
		return render(request,'redirect.html')
	elif 'button2' in request.POST:   #  This button is when password has been forgotten
		request.session['redirect'] = 'main'
		return render(request,'redirect.html')
	else:
		form = login_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	request.session["login_name"] = ""
	request.session["login_password"] = ""
	return render(request,'member_login.html', args)
def member_login_check(request):
	login_company = request.session['login_company']
	login_password = request.session['login_password']
	login_name = request.session['login_name']
	db, cur = db_set(request)
	cur.execute("""CREATE TABLE IF NOT EXISTS member_data(Id INT PRIMARY KEY AUTO_INCREMENT,name CHAR(80), company CHAR(80), email CHAR(80), type CHAR(80), password CHAR(80), verified INT(10))""")
	sql = "SELECT COUNT(*) FROM member_data where company = '%s' and name = '%s' and password = '%s'" %(login_company,login_name,login_password)
	cur.execute(sql)
	tmp = cur.fetchall()
	pwd_check = int(tmp[0][0])
	db.close()

	if pwd_check == 0:
		request.session['login_check'] = 1
	else:
		request.session['redirect'] = 'member'  # If login valid then go to login main page
		return render(request,'redirect.html')
	request.session['redirect'] = 'member_login'   # Login not valid so bounce back with message based on code number
	return render(request,'redirect.html')

# ********************************************************************** End of Login Section  ****************************************************



# **********************************************************************Member Signup Section  ****************************************************
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
	return render(request,'member_signup.html', args)
def member_register_check(request):
	login_company = request.session['login_company']
	login_email = request.session['login_email']
	login_name = request.session['login_name']
	db, cur = db_set(request)
	cur.execute("""CREATE TABLE IF NOT EXISTS member_data(Id INT PRIMARY KEY AUTO_INCREMENT,name CHAR(80), company CHAR(80), email CHAR(80), type CHAR(80), password CHAR(80), verified INT(10))""")
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
	pwd = 'password'
	t = 'admin'
	st=6
	db, cur = db_set(request)
	cur.execute('''INSERT INTO member_data(name,company,email,type,password,verified) VALUES(%s,%s,%s,%s,%s,%s)''', (login_name,login_company,login_email,t,pwd,v))
	db.commit()
	sql = "SELECT Id FROM member_data where name = '%s' and company = '%s' and email = '%s'" %(login_name,login_company,login_email)
	cur.execute(sql)
	tmp = cur.fetchall()
	id1 = int(tmp[0][0])
	db.close()
	b = "\r\n"
	link1 = request.session['server_link'] + 'member_validate/get/'+str(id1)
	message_subject = 'BuzzApp Registration'
	message3 = "Congratulations " + login_name + " You  have registered for BuzzApp with your company " + login_company
	message2 = "click the link to validate your membership:   " + link1
	toaddrs = [login_email]
	#toaddrs = ["dclark@stackpole.com","dave7995@gmail.com"]
	fromaddr = 'buzzappca@gmail.com'
	frname = 'Dave'
	server = SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('buzzappca@gmail.com', 'benny6868')
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
# ********************************************************************** End of Sign up Section  ****************************************************
