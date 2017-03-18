from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View, TemplateView
from .models import Room
# Create your views here.

class IndexView(generic.TemplateView):
	template_name = 'service/index.html'
	

class RoomView(generic.ListView):
	template_name = 'service/room.html'
	context_object_name = 'all_rooms'

	def get_queryset(self):
		return Room.objects.all()




