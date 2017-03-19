from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View, TemplateView, ListView
from .models import Room
from django.views.generic.edit import FormMixin
from .forms import RoomSearch
# Create your views here.

class IndexView(generic.TemplateView):
	template_name = 'service/index.html'
	

class RoomView(FormMixin, ListView):
	template_name = 'service/room.html'
	context_object_name = 'all_rooms'
	form_class = RoomSearch

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query:
			all_rooms = Room.objects.filter(description__icontains=query)
		else:
			all_rooms = Room.objects.all()
		return all_rooms

class DetailView(generic.DetailView):
	model = Room
	template_name = 'service/detail.html'

class RoomCreate(CreateView):
	model = Room
	fields = ['title', 'description', 'price' , 'room_photo']




