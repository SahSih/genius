from django.conf.urls import url
from . import views

app_name = "service"

urlpatterns =[
	# /service/
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^room/$',views.RoomView.as_view(), name='room'),
	url(r'^room/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),


]