import datetime
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Room(models.Model):
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=500, default="description")
	price = models.IntegerField(default=0)
	pub_date = models.DateTimeField(default=timezone.now)
	room_photo = models.FileField()

	def __str__(self):
		return self.title
	def get_absolute_url(self):
		return reverse('service:detail', kwargs={'pk': self.pk})
