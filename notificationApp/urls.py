from django.urls import path
from .views import VideoGamesListListView, UserVideoGamesListView, VideoGameDetailView, VideoGamesListUpdateView, VideoGamesListCreateView, VideoGamesListDeleteView
from . import views

urlpatterns = [
path("", VideoGamesListListView.as_view(), name = "home-notification"),
path("user/<str:username>/", UserVideoGamesListView.as_view(), name = "user-lists"),
path("user/<str:username>/search", UserVideoGamesListView.as_view(), name = "user-lists-search"),
path("game/<int:pk>/", VideoGameDetailView.as_view(), name = "videogame-detail"),
path("game/<int:pk>/<str:slug>/add/", views.videoGameAdd, name = "videogame-add"),
path("list/<int:list_id>/game/<int:game_pk>/update/", views.videoGameUpdate, name = "videogame-update"),
path("list/<int:list_id>/game/<int:game_pk>/delete/", views.videoGameDelete, name = "videogame-delete"),
path("game/<int:pk>/preference/", views.viewPreference, name = "videogame-preference"),
path("list/<int:pk>/", views.videoGamesListDetail, name = "videogameslist-detail"),
path("list/create/", VideoGamesListCreateView.as_view(), name = "videogameslist-create"),
path("list/<int:pk>/delete/", VideoGamesListDeleteView.as_view(), name = "videogameslist-delete"),
path("list/<int:pk>/update/", VideoGamesListUpdateView.as_view(), name = "videogameslist-update"),
path("about/", views.about, name = "about-notification"),
]