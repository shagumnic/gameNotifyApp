from django.shortcuts import render, get_object_or_404, redirect
from .models import VideoGamesList, VideoGame
import requests
import json
import re
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.views.generic import (ListView,
								DetailView,
								UpdateView,
								DeleteView,
								CreateView)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from io import BytesIO
from django.core import files
import urllib.parse
import urllib
# Create your views here.

def home(request) :
	if request.user.is_authenticated :
		game_list = videogameslist.objects.filter(user = request.user)
		context = {
			"gameList" : game_list
		}
	else :
		context = {}
	return render(request, "notificationApp/home.html", context)

@login_required
def viewPreference(request, pk) :
	#check box, list of available genre, maybe replace it with sidebar
	#if method == "POST"
	#push all of those value into a list
	#loop through the list, add it to the url
	#give a choice (maybe) to change the date
	#give choice to export their steam wishlist
	try :
		user_list = request.user.videogameslist_set.get(id = pk)
	except VideoGamesList.DoesNotExist :
		messages.error(request, f'The list you tried to add to is not in your list!')
		return redirect("user_lists", username = request.user.username)

	context = {"resultGame" : [], "user_list" : user_list, "chosen_genres" : '', "dateAfter": "week", "page_size": 5}
	if request.method == "POST" :
		if request.POST.get("search_game") :
			search_game = urllib.parse.quote(request.POST.get("search_game"))
			url = "https://api.rawg.io/api/games?stores=1&search=" + search_game
			response = requests.request("GET", url)
			resultList = response.json()
			resultGame = resultList["results"]
			if resultList["next"] != None :
				url_next = urllib.parse.quote(resultList["next"])
			else :
				url_next = None
			context = {"resultGame" : resultGame, "user_list" : user_list, "chosen_genres" : '', "url_next": url_next}
		else :
			genres = ''
			genres_list = request.POST.getlist('genres[]')
			for genre in genres_list:
				genres += genre
				genres += ','
			genres = genres[:len(genres) - 1]
			today = datetime.today()
			today = today.strftime("%Y-%m-%d")
			if request.POST.get("day-after") == "week":
				dateAfter = datetime.today() + relativedelta(days=7)
			elif request.POST.get("day-after") == "month":
				dateAfter = datetime.today() + relativedelta(months=1)
			elif request.POST.get("day-after") == "six_months":
				dateAfter = datetime.today() + relativedelta(months=6)
			elif request.POST.get("day-after") == "year":
				dateAfter = datetime.today() + relativedelta(years=1)
			dateAfter = dateAfter.strftime("%Y-%m-%d")
			page_size = 5 #5, 10, 20
			if request.POST.get("page_size") == "5":
				page_size = 5
			elif request.POST.get("page_size") == "10":
				page_size = 10
			elif request.POST.get("page_size") == "20":
				page_size = 20
			elif request.POST.get("page_size") == "30":
				page_size = 30
			url = "https://api.rawg.io/api/games?dates=%s,%s&ordering=released&page=1&page_size=" % (today, dateAfter)
			url = url + str(page_size) + "&stores=1"

			if len(genres) != 0 :
				url = url + "&genres=" + genres
			response = requests.request("GET", url)
			resultList = response.json()
			resultGame = resultList["results"]
			if resultList["next"] != None :
				url_next = urllib.parse.quote(resultList["next"])
			else :
				url_next = None
			context = {"resultGame" : resultGame, "user_list" : user_list, "chosen_genres" : genres, "dateAfter": request.POST.get("day-after"),
			 "page_size": page_size, "url_next": url_next}
		return render(request, "notificationApp/viewPreference.html", context)
	else :
		if request.GET.get('url_next') :
			url = request.GET.get('url_next')
			response = requests.request("GET", url)
			resultList = response.json()
			resultGame = resultList["results"]
			if resultList["next"] != None :
				url_next = urllib.parse.quote(resultList["next"])
			else :
				url_next = None
			if request.GET.get('genres') :
				chosen_genres = request.GET.get('genres')
			else :
				chosen_genres = ''

			if request.GET.get('page_size') != None :
				page_size = int(request.GET.get("page_size"))
			else :
				page_size = None
			context = {"resultGame": resultGame, "user_list" : user_list, "chosen_genres": chosen_genres, "dateAfter": request.GET.get("day-after"),
			 "page_size": None, "url_next": url_next}
	return render(request, "notificationApp/viewPreference.html", context)

def about(request):
    return render(request, 'notificationApp/about.html', {'title': 'About'})

class VideoGamesListListView(ListView) :
	model = VideoGamesList
	paginate_by = 5
	ordering = ["id"]

class UserVideoGamesListView(LoginRequiredMixin, ListView) :
	model = VideoGamesList
	template_name = 'notificationApp/user_lists.html'
	paginate_by = 5

	def get_queryset(self) :
		user = get_object_or_404(User, username = self.kwargs.get('username'))
		object_list = VideoGamesList.objects.filter(user = user)
		name = self.request.GET.get('search_list')
		if (name != None ):
			object_list = object_list.filter(name__icontains = name).order_by("name")
		else:
			object_list = object_list.order_by("name")
		return object_list

class VideoGameDetailView(LoginRequiredMixin, DetailView) :
	model = VideoGame

@login_required
def videoGameAdd(request, pk, slug) : #game_list from the viewNews pass on above
	try :
		user_list = request.user.videogameslist_set.get(id = pk)
	except VideoGamesList.DoesNotExist :
		messages.error(request, f'The list you tried to add to is not in your list!')
		return redirect("user_lists", username = request.user.username)
	if request.method == "POST" :
		if len(user_list.videogame_set.filter(slug = slug)) > 1 :
			messages.error(request, f'The game you\'re trying to add is already there')
			user_list.videogame_set.filter(slug = slug)[1].delete()
			return redirect("videogameslist-detail", pk = user_list.id)
		if request.POST.get("newItem") :
			user_game = user_list.videogame_set.get(id = int(request.POST.get("newItem")))
			if request.POST.get("discount") == "notified" and request.POST.get("released") == "notified":
				user_game.isDiscount = True
				if request.POST.get("chosen_discount_rate") :
					chosen_discount_rate = user_game.discountrate_set.create(chosen_discount_percent = int(request.POST.get("chosen_discount_rate")))
					chosen_discount_rate.save()
				user_game.isReleased = True
			elif request.POST.get("discount") == "notified" :
				user_game.isDiscount = True
				if request.POST.get("chosen_discount_rate") :
					chosen_discount_rate = user_game.discountrate_set.create(chosen_discount_percent = int(request.POST.get("chosen_discount_rate")))
					chosen_discount_rate.save()
				user_game.isReleased = False
			elif request.POST.get("released") == "notified" :
				user_game.isDiscount = False
				user_game.isReleased = True
			else :
				user_game.isDiscount = False
				user_game.isReleased = False
			user_game.save()
			messages.success(request, f'The game {user_game.name} has been add to your list!')
			return redirect("videogame-detail", pk = user_game.id)
		elif request.POST.get("cancel") :
			newGame = user_list.videogame_set.get(id = int(request.POST.get("cancel")))
			newGame.delete()
			return redirect("user-lists", username = request.user.username)
	if request.user.videogameslist_set.all().first() == None :
		messages.error("You haven't created any list yet")
		return redirect("videogameslist-create")
	url = "https://api.rawg.io/api/games/" + slug
	response = requests.request("GET", url)
	resultGame = json.loads(response.text)
	index = 0
	while index < len(resultGame["stores"]) and resultGame["stores"][index]["store"]["name"] != "Steam" :
		index += 1
	if index < len(resultGame["stores"]) :
		steamId = re.findall("\d+", resultGame["stores"][index]["url"])[0]
		url = "http://store.steampowered.com/api/appdetails?cc=us&appids=" + steamId
		response = requests.request("GET", url)
		resultSteam = json.loads(response.text)
		img_url = resultSteam[steamId]["data"]["header_image"]
		
	else :
		steamId = ''
		img_url = resultGame["background_image"]
	genres = ""
	for genre in resultGame["genres"] :
		genres += genre["name"]
		genres += ", "
	genres = genres[:len(genres)-2]
	img = requests.get(img_url)
	if img.status_code != requests.codes.ok :
		img = None

	fp = BytesIO()
	fp.write(img.content)
	file_name = slug + '.jpg'
	if resultGame["released"] != None :
		released_date = datetime.strptime(resultGame["released"], "%Y-%m-%d").date()
	else :
		released_date = None
	tags = ''
	for tag in resultGame["tags"] :
		tags += tag["name"]
		tags += ", "
	tags = tags[:len(tags)-2]
	newGame = user_list.videogame_set.create(steamId = steamId, slug = slug, name = resultGame["name"], released_date = released_date,\
		genres = genres, rating = resultGame["metacritic"], description = resultGame["description_raw"], tags = tags)
	newGame.preview_image.save(file_name, files.File(fp))
	if newGame.released_date <= date.today() :
		newGame.isReleased = False
	newGame.save()
	context = {"newGame" : newGame} #place_holder, a dictionary or list contains all of the neccessary information
	return render(request, 'notificationApp/videoGameAdd.html', context)

@login_required
def videoGameDelete(request, list_id, game_pk) :
	try :
		user_list = request.user.videogameslist_set.get(id = list_id)
		user_game = user_list.videogame_set.get(id = game_pk)
	except VideoGame.DoesNotExist :
		messages.error(request, f'The game you tried to delete is not in your list!')
		return redirect("user-lists", username = request.user.username)
	if request.method == "POST" :
		user_game.delete()
		messages.success(request, f'The game has been deleted from your list!')
		return redirect("videogameslist-detail", pk = list_id)
	else :
		return render(request, "notificationApp/videoGameDelete.html", {"game" : user_game})

@login_required
def videoGameUpdate(request, list_id, game_pk) :
	try :
		user_list = request.user.videogameslist_set.get(id = list_id)
		user_game = user_list.videogame_set.get(id = game_pk)
	except VideoGame.DoesNotExist :
		messages.error(request, f'The game you tried to update is not in your list!')
		return redirect("user-lists", username = request.user.username)
	if request.method == "POST" :
		#Still have to get the data that want to update
		if request.POST.get("discount") == "notified" and request.POST.get("released") == "notified":
			if user_game.isDiscount == True :
				if request.POST.get("chosen_discount_rate") :
					chosen_discount_rate = user_game.discountrate_set.all().first()
					chosen_discount_rate.chosen_discount_percent = int(request.POST.get("chosen_discount_rate"))
					chosen_discount_rate.save()
			else :
				if request.POST.get("chosen_discount_rate") :
					chosen_discount_rate = user_game.discountrate_set.create(chosen_discount_percent = int(request.POST.get("chosen_discount_rate")))
					chosen_discount_rate.save()
			user_game.isDiscount = True
			user_game.isReleased = True
		elif request.POST.get("discount") == "notified" :
			if user_game.isDiscount == True :
				if request.POST.get("chosen_discount_rate") :
					chosen_discount_rate = user_game.discountrate_set.all().first()
					chosen_discount_rate.chosen_discount_percent = int(request.POST.get("chosen_discount_rate"))
					chosen_discount_rate.save()
			else :
				if request.POST.get("chosen_discount_rate") :
					chosen_discount_rate = user_game.discountrate_set.create(chosen_discount_percent = int(request.POST.get("chosen_discount_rate")))
					chosen_discount_rate.save()
			user_game.isDiscount = True
			user_game.isReleased = False
		elif request.POST.get("released") == "notified" :
			user_game.isDiscount = False
			user_game.isReleased = True
		else :
			user_game.isDiscount = False
			user_game.isReleased = False
		user_game.save()
		
		messages.success(request, f'The game has been updated!')
		return redirect("videogame-detail", pk = user_game.id)
	return render(request, "notificationApp/videoGameUpdate.html", {"game" : user_game})

@login_required
def videoGamesListDetail(request, pk) :
	try :
		public_list = VideoGamesList.objects.get(id = pk)
	except VideoGamesList.DoesNotExist :
		messages.error(request, f'The list you tried to access does not exist!')
		return redirect("user-lists", username = request.user.username)
	if public_list.isPublic or public_list.user == request.user:
		game_list = []
		public_game_list = public_list.videogame_set.all()
		for game in public_game_list.all() :
			game_list.append(game)
		paginator = Paginator(game_list, 5)
		page_number = request.GET.get("page")
		page_obj = paginator.get_page(page_number)
		return render(request, 'notificationApp/videoGamesListDetail.html', {'page_obj':page_obj, 'public_list' : public_list})
	messages.error(request, f'The list you tried to access is not public')
	return redirect("home-notification")

class VideoGamesListCreateView(LoginRequiredMixin, CreateView) :
	model = VideoGamesList
	fields = ['name', 'isPublic']

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class VideoGamesListUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView) :
	model = VideoGamesList
	fields = ['name', 'isPublic']
	template_name = "notificationApp/videogameslist_update.html"
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)
	def test_func(self) :
		list = self.get_object()
		if self.request.user == list.user :
			return True
		return False

class VideoGamesListDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView) :
	model = VideoGamesList
	success_url = '/' #try to redirect it back to the user
	def test_func(self) :
		list = self.get_object()
		if self.request.user == list.user :
			return True
		return False