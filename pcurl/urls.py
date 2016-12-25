from django.conf.urls import url
from pcurl.views import psearch
urlpatterns = [
	url(r'^$', psearch),]
