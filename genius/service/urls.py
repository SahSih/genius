from django.conf.urls import url
from . import views

app_name = "service"

urlpatterns =[
	# /service/
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^room/$',views.RoomView.as_view(), name='room'),
	url(r'^room/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
	url(r'^room/add/$', views.RoomCreate.as_view(), name='room-add'),

	url(r'^book/$',views.BookView.as_view(), name='book'),
	url(r'^book/(?P<pk>[0-9]+)/$', views.BookDetailView.as_view(), name='detail-book'),

]