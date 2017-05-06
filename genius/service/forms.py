from django import forms
from django.contrib.auth.models import User

class RoomSearch(forms.Form):
	description = forms.CharField(required=False)

class BookSearch(forms.Form):
	course = forms.CharField(required=False)

class TutorSearch(forms.Form):
	description = forms.CharField(required=False)

class AllSearch(forms.Form):
	title = forms.CharField(required=False)

class UserForm(forms.ModelForm):
	# encode password
	password = forms.CharField(widget=forms.PasswordInput)

	# infomation about my class
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password']

class LoginForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:

		model = User
		fields = ['username', 'password']
