from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class VideoGamesList(models.Model) :
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	name = models.CharField(max_length = 200)
	isPublic = models.BooleanField(default = True)

	def __str__(self) :
		return self.name

	def get_absolute_url(self) :
		return reverse('videogameslist-detail', kwargs= {'pk' : self.pk})

class VideoGame(models.Model) :
	steamId = models.CharField(max_length= 200)
	slug = models.CharField(max_length= 200)
	name = models.CharField(max_length = 200)
	concurrentPlayers = models.IntegerField(null = True)
	released_date = models.DateField(null = True)
	genres = models.CharField(max_length = 200 )
	rating = models.IntegerField(null = True)
	description = models.TextField()
	preview_image = models.ImageField(max_length = 200, null = True, upload_to = 'game_pics')
	isDiscount = models.BooleanField(default = True)
	isReleased = models.BooleanField(default = True)
	videogameslist = models.ForeignKey(VideoGamesList, on_delete = models.CASCADE)
	tags = models.CharField(max_length = 200, null = True)
	def __str__(self):
		return self.name

class DiscountRate(models.Model) :
	videoGame = models.ForeignKey(VideoGame, on_delete = models.CASCADE)
	initial = models.CharField(max_length = 200, null = True)
	final = models.CharField(max_length=200, null = True)
	discount_percent = models.IntegerField(null = True)
	chosen_discount_percent = models.IntegerField(null = True)

	def __str__(self):
		return str(self.chosen_discount_percent)

class RedditNews(models.Model) :
	videoGame = models.ForeignKey(VideoGame, on_delete = models.CASCADE)
	redditUrl = models.CharField(max_length = 200)
	redditName = models.CharField(max_length = 200)
	redditDescription = models.TextField()

	def __str__(self) :
		return self.redditName