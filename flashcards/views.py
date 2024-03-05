from django.shortcuts import render
from django.http import HttpResponse
from .models import Deck, Card
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .forms import DeckForm
import requests, json
from django.core import serializers
from django.http import JsonResponse

# Create your views here.


class IndexView(generic.ListView):
    template_name = "flashcards/index.html"
    context_object_name = "latest_deck_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Deck.objects.order_by("-mod_date")[:5]
    



class DeckView(generic.DetailView):
    model = Deck
    template_name = "flashcards/deck.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cards = self.object.card_set.all()
        context['card_list'] = serializers.serialize('json', cards)
        return context





class CreateDeckView(generic.CreateView):
    model = Deck
    form_class = DeckForm  # this should be a valid form class
    template_name = 'flashcards/createdeck.html'
    success_url = '/flashcards/'
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

class AddCardsView(generic.CreateView):
    model = Card
    fields = ['front', 'back']
    template_name = 'flashcards/addcards.html'
    success_url = '/flashcards/'
    

    def form_valid(self, form):
        form.instance.deck = Deck.objects.get(pk=self.kwargs['deck_id'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deck'] = Deck.objects.get(pk=self.kwargs['deck_id'])
        return context

def addcard(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    front = request.POST["front"]
    back = request.POST["back"]
    card = Card(deck=deck, front=front, back=back)
    card.save()
    return HttpResponseRedirect(reverse("flashcards:addcards", args=(deck.id,)))

def createdeck(request):
    if request.method == "POST":
        print("The form is being submitted")
        form = DeckForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print("The form is valid")
            deck = form.save()
            return HttpResponseRedirect(reverse("flashcards:addcards", args=(deck.id,)))
    else:
        form = DeckForm()
    return render(request, "flashcards/addcard.html", {"form": form, "deck": deck})

def deletecard(request, deck_id, card_id):
    print("deleting card")
    card = get_object_or_404(Card, pk=card_id)
    card.delete()
    return HttpResponseRedirect(reverse("flashcards:addcards", args=(deck_id,)))