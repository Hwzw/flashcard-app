from django.urls import path
from . import views
from django.urls import include

app_name = 'flashcards'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DeckView.as_view(), name="viewdeck"),
    path("<int:deck_id>/addcards/addcard", views.addcard, name="addcard"),
    path("<int:deck_id>/addcards/<int:card_id>/deletecard/", views.deletecard, name="deletecard"),
    path("viewcreatedeck/", views.CreateDeckView.as_view(), name="viewcreatedeck"),
    path("<int:deck_id>/addcards/", views.AddCardsView.as_view(), name="addcards"),
    path("viewcreatedeck/createdeck", views.createdeck, name="createdeck"),
]
