
"""buzzca URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
		https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
		1. Add an import:  from my_app import views
		2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
		1. Add an import:  from other_app.views import Home
		2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
		1. Import the include() function: from django.urls import include, path
		2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from buzzca.views2 import main, member_login,member_signup,member_signup_initial,member_preregister,member_register_check, member_validate
from buzzca.views2 import member_login_check,member_login_initial


urlpatterns = [
		url(r'^$',main),
		url(r'^main',main),

		# Login and Registration  ***************************************************************************
		url(r'^member_login/', member_login),
		url(r'^member_login_initial/', member_login_initial),
		url(r'^member_login_check/', member_login_check),
		url(r'^member_signup/', member_signup),
		url(r'^member_signup_initial/', member_signup_initial),
		url(r'^member_register_check/', member_register_check),
		url(r'^member_preregister/', member_preregister),
		url(r'^member_validate/get/(?P<index>\d+)/$', member_validate),

		# ***************************************************************************************************






]