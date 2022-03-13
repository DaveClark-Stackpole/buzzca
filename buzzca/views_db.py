from django.shortcuts import render_to_response
from django.template import loader
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from smtplib import SMTP
import MySQLdb

def net1(request):
	request.session["local_switch"] = 0
	request.session["local_toggle"] = "/trakberry"
	# ###this
	# request.session["local_switch"] = 1
	# request.session["local_toggle"] = ""
	return
# Methods for opening database for all and returning db and cur


def db_set(request):  # Module to set DB settings to the one that works.  Whether local or Server

	db = MySQLdb.connect(host="127.0.0.1",user="buzzappc_buzzapp",passwd="benny6868",db='buzzappc_buzzmysql')
	cursor = db.cursor()
	# sql = "SELECT * from testtest" 
	# cursor.execute(sql)
	# tmp2 = cursor.fetchall()
	# request.session["local_toggle"]="/trakberry"
	return db, cursor


