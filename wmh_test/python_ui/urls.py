from django.conf.urls import include, url
from django.contrib import admin
from python_ui.view import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'python_UI.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	#url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$',Get_param),
    url(r'^solve/$',solve),
    url(r'^upload/$','upload.views.upload'),
    url(r'^download/$','upload.views.download'),
]
