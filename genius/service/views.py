from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View, TemplateView, ListView, RedirectView
from .models import Room, Book
from django.views.generic.edit import FormMixin
from .forms import RoomSearch, BookSearch, UserForm, LoginForm
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User

# Create your views here.

class IndexView(generic.TemplateView):
	template_name = 'service/index.html'
	

class RoomView(FormMixin, ListView):
	template_name = 'service/room.html'
	context_object_name = 'all_rooms'
	form_class = RoomSearch
	# all_users = User.objects.all()

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query:
			all_rooms = Room.objects.filter(description__icontains=query)
		else:
			all_rooms = Room.objects.all()
		return all_rooms

# PersonalRooms shows specific rooms that authenticated user created
class PersonalRoomView(ListView):
	template_name = 'service/user-room.html'
	context_object_name = 'all_rooms'

	def get_queryset(self):
		query = Room.objects.filter(user=self.request.user)
		return query

class DetailView(generic.DetailView):
	model = Room
	template_name = 'service/detail.html'

class RoomCreate(CreateView):
	model = Room
	fields = ['title', 'description', 'price' , 'room_photo']

	def form_valid(self, form):
		room = form.save(commit=False)
		room.user = self.request.user
		return super(RoomCreate, self).form_valid(form)

class RoomDelete(DeleteView):
	model = Room
	success_url = reverse_lazy('service:personal-rooms')

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

class BookCreate(CreateView):
	model = Book
	fields = ['title', 'course', 'price' , 'book_photo']

	def form_valid(self, form):
		book = form.save(commit=False)
		book.user = self.request.user
		return super(BookCreate, self).form_valid(form)

class BookDetailView(generic.DetailView):
	model = Book
	template_name = 'service/detail-book.html'

class UserFormView(View):
	form_class = UserForm
	template_name = 'service/registration_form.html'

	# build-in functions GET and POST
	# display blank form, new user never signed up for an account :)
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	# register the user
	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():

			# create object from the form, but not save to db yet
			user = form.save(commit=False)

			# cleaned - normalized data
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			# returns User object if credentials are correct
			user = authenticate(username=username, password=password)

			if user is not None:

				if user.is_active:
					login(request, user)
					return redirect('service:index')

		return render(request, self.template_name, {'form': form})

class LogoutView(RedirectView):
	permanent = False
	query_string = True

	def get_redirect_url(self):
		logout(self.request)
		return reverse_lazy('service:index')

# log in function for login form
class LoginView(View):
	form_class = LoginForm
	template_name = 'service/login_form.html'

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('service:index')

		return render(request, self.template_name, {'form': form})





