from django import forms

class RoomSearch(forms.Form):
	description = forms.CharField(required=False)
	
class BookSearch(forms.Form):
	title = forms.CharField(required=False)
