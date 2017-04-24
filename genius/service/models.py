import datetime
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class Room(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	title = models.CharField(max_length=30)
	description = models.CharField(max_length=255)
	price = models.IntegerField(default=0)
	pub_date = models.DateTimeField(default=timezone.now)
	room_photo = models.FileField()
	location = models.CharField(max_length=100, default='place')

	def __str__(self):
		return self.title
	def get_absolute_url(self):
		return reverse('service:detail', kwargs={'pk': self.pk})

class Book(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	title = models.CharField(max_length=100)
	course = models.CharField(max_length=50)
	price = models.IntegerField(default=0)
	book_photo = models.FileField()
	location = models.CharField(max_length=100, default='place')

	def __str__(self):
		return self.title
	def get_absolute_url(self):
		return reverse('service:detail-book', kwargs={'pk': self.pk})

class Restaurant(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100)
	location = models.CharField(max_length=100)
	description = models.CharField(max_length=255, default="null")
	restaurant_photo = models.FileField()

	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('service:detail-restaurant', kwargs={'pk': self.pk})

class Tutor(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100)
	location = models.CharField(max_length=100)
	description = models.CharField(max_length=255)
	tutor_photo = models.FileField()

	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('service:detail-tutor', kwargs={'pk': self.pk})

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, blank=True)
	location = models.CharField(max_length=30, blank=True)
	birthday = models.DateField(null=True, blank=True)

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_profile(sender, instance, created, **kwargs):
# 	if created:
# 		profile = Profile(user=instance)
#         profile.save()

# # @receiver(post_save, sender=User)
# # def save_user_profile(sender, instance, **kwargs):
# # 	instance.profile.save()
