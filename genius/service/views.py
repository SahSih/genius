from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View, TemplateView, ListView
from .models import Room, Book
from django.views.generic.edit import FormMixin
from .forms import RoomSearch, BookSearch
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

class BookView(FormMixin, ListView):
	template_name = 'service/book.html'
	context_object_name = 'all_books'
	form_class = BookSearch

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query:
			all_books = Book.objects.filter(title__icontains=query)
		else:
			all_books = Book.objects.all()
		return all_books

class BookDetailView(generic.DetailView):
	model = Book
	template_name = 'service/detail-book.html'




