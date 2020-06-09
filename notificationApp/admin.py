from django.contrib import admin
from .models import VideoGamesList, VideoGame, DiscountRate, RedditNews
# Register your models here.
admin.site.register(VideoGamesList)
admin.site.register(VideoGame)
admin.site.register(DiscountRate)
admin.site.register(RedditNews)