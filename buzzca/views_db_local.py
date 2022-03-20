from django.shortcuts import render_to_response
from django.template import loader
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from smtplib import SMTP
import MySQLdb


# Methods for opening database for all and returning db and cur

def db_set(request):  # Module to set DB settings to the one that works.  Whether local or Server
	db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="benny6868",db='buzzappc_buzzmysql')  # Local deployment	
	cursor = db.cursor()
	request.session['server_link']='http://127.0.0.1:8080/'
	return db, cursor


