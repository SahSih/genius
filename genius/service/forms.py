from django import forms

class RoomSearch(forms.Form):
	description = forms.CharField(required=False)
