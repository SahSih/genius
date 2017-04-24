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
	url(r'^book/add/$', views.BookCreate.as_view(), name='book-add'),

	url(r'^register/$', views.UserFormView.as_view(), name='register'),
	url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
	url(r'^login/$', views.LoginView.as_view(), name='login'),

	url(r'^user/$', views.PersonalView.as_view(), name='personal-rooms'),
	url(r'^user/(?P<pk>[0-9]+)/delete/$', views.RoomDelete.as_view(), name='room-delete'),

	url(r'^restaurant/$',views.RestaurantView.as_view(), name='restaurant'),
	url(r'^restaurant/add/$', views.RestaurantCreate.as_view(), name='restaurant-add'),
	url(r'^restaurant/(?P<pk>[0-9]+)/$', views.RestaurantDetailView.as_view(), name='detail-restaurant'),

]