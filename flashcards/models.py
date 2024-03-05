from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Deck(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    mod_date = models.DateTimeField(auto_now=True)
    #author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    front = models.CharField(max_length=100)
    back = models.CharField(max_length=100)
    def __str__(self):
        return self.front
    def getFront(self):
        return self.front
    def getBack(self):
        return self.back

def create_deck(name):
    return Deck.objects.create(name=name, mod_date=timezone.now())

