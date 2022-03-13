from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from datetime import datetime
import os
import time
from buzzca.views_db import db_set

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


# Call Main Login screen
def test(request):
	# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	# BASE_DIR = BASE_DIR + '\\static\\buzzca'
	# # t=4/0
	# dir = BASE_DIR
	# p=8/0

	db, cur = db_set(request)

	a = 'Dave'
	b = 10

	cur.execute("""CREATE TABLE IF NOT EXISTS test_A(Id INT PRIMARY KEY AUTO_INCREMENT,var1 CHAR(80), int1 INT(30) )""")
	cur.execute('''INSERT INTO test_A(var1,int1) VALUES(%s,%s)''', (a,b))
	db.commit()
	db.close()


	t=int(time.time())
	request.session['TCURR'] = t

	return render(request, "test4.html",)
