from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View, TemplateView, ListView, RedirectView
from .models import Room, Book, Restaurant, Tutor, RestaurantReview
from django.views.generic.edit import FormMixin
from .forms import RoomSearch, BookSearch, TutorSearch, UserForm, LoginForm, AllSearch
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from itertools import chain 
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.
# Original: IndexView(FormMixin, generic.TemplateView)

class IndexView(generic.TemplateView):
	template_name = 'service/index.html'

# TODO: write result for q
class SearchResultView(FormMixin, ListView):
	template_name = 'service/result.html'
	context_object_name = 'all'
	form_class = AllSearch 

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query:
			room_by_title = Room.objects.filter(title__icontains=query)
			room_by_description = Room.objects.filter(description__icontains=query)
			room_by_location = Room.objects.filter(location__icontains=query)
			book_by_title = Book.objects.filter(title__icontains=query)
			book_by_course = Book.objects.filter(course__icontains=query)
			book_by_location = Book.objects.filter(location__icontains=query)
			restaurant_by_title = Restaurant.objects.filter(title__icontains=query)
			restaurant_by_description = Restaurant.objects.filter(description__icontains=query)
			restaurant_by_location = Restaurant.objects.filter(location__icontains=query)
			tutor_by_title = Tutor.objects.filter(title__icontains=query)
			tutor_by_description = Tutor.objects.filter(description__icontains=query)
			tutor_by_location =  Tutor.objects.filter(location__icontains=query)
			global all
			all = sorted(chain(room_by_title, room_by_description, room_by_location, book_by_title, book_by_course, book_by_location, restaurant_by_title, restaurant_by_description, restaurant_by_location, tutor_by_title, tutor_by_description, tutor_by_location), reverse=True)
		return all

class RoomView(FormMixin, ListView):
	template_name = 'service/room.html'
	context_object_name = 'all_rooms'
	form_class = RoomSearch
	# all_users = User.objects.all()

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query:
			all_rooms = Room.objects.filter(title__icontains=query)
		else:
			all_rooms = Room.objects.all()
		return all_rooms

# PersonalRooms shows specific rooms that authenticated user created
class PersonalView(ListView):
	template_name = 'service/user.html'
	context_object_name = 'all'

	def get_queryset(self):
		queryR = Room.objects.filter(user=self.request.user)
		queryB = Book.objects.filter(user=self.request.user)
		queryF = Restaurant.objects.filter(user=self.request.user)
		queryT = Tutor.objects.filter(user=self.request.user)
		all = sorted(chain(queryR, queryB, queryF, queryT), reverse=True)
		return all

class DetailView(generic.DetailView):
	model = Room
	template_name = 'service/detail.html'

class RoomCreate(CreateView):
	model = Room
	fields = ['title', 'description', 'price' , 'photo']

	def form_valid(self, form):
		room = form.save(commit=False)
		room.user = self.request.user
		return super(RoomCreate, self).form_valid(form)

class RoomDelete(DeleteView):
	model = Room
	success_url = reverse_lazy('service:personal-rooms')
class BookDelete(DeleteView):
	model = Book
	success_url = reverse_lazy('service:personal-rooms')
class RestaurantDelete(DeleteView):
	model = Restaurant
	success_url = reverse_lazy('service:personal-rooms')
class TutorDelete(DeleteView):
	model = Tutor
	success_url = reverse_lazy('service:personal-rooms')

class BookView(FormMixin, ListView):
	template_name = 'service/book.html'
	context_object_name = 'all_books'
	form_class = BookSearch

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query:
			all_books = Book.objects.filter(course__icontains=query)
		else:
			all_books = Book.objects.all()
		return all_books

class BookCreate(CreateView):
	model = Book
	fields = ['title', 'course', 'price' , 'photo']

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

class RestaurantView(ListView):
	template_name = 'service/restaurant.html'
	context_object_name = 'all_restaurants'
	# form_class = RoomSearch
	# # all_users = User.objects.all()

	def get_queryset(self):
		all_restaurants = Restaurant.objects.all()
		return all_restaurants

# create detail-restaurant.html
class RestaurantDetailView(generic.DetailView):
	model = Restaurant
	template_name = 'service/detail-restaurant.html'

	# def get_queryset(self):
	# 	all_reviews = Review.objects.all()
	# 	return all_reviews
	def get_context_data(self, **kwargs):
		context = super(RestaurantDetailView, self).get_context_data(**kwargs)
		context['description'] = RestaurantReview.description
		return context


class RestaurantCreate(CreateView):
	model = Restaurant
	fields = ['title', 'description', 'location', 'photo']

	def form_valid(self, form):
		restaurant = form.save(commit=False)
		restaurant.user = self.request.user
		return super(RestaurantCreate, self).form_valid(form)

class TutorView(FormMixin, ListView):
	template_name = 'service/tutor.html'
	context_object_name = 'all_tutors'
	form_class = TutorSearch
	# # all_users = User.objects.all()

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query:
			all_tutors = Tutor.objects.filter(description__icontains=query)
		else:
			all_tutors = Tutor.objects.all()
		return all_tutors

# create detail-tutor.html
class TutorDetailView(generic.DetailView):
	model = Tutor
	template_name = 'service/detail-tutor.html'

class TutorCreate(CreateView):
	model = Tutor
	fields = ['title', 'location', 'description', 'tutor_photo']

	def form_valid(self, form):
		tutor = form.save(commit=False)
		tutor.user = self.request.user
		return super(TutorCreate, self).form_valid(form)

def review(request, pk):
  restaurant = get_object_or_404(Restaurant, pk=pk)
  review = RestaurantReview(user = request.user, title = request.POST["title"], description = request.POST["description"], restaurant = restaurant)
  review.save()
  return HttpResponseRedirect(reverse('service:detail-restaurant', args=(restaurant.id,)))
