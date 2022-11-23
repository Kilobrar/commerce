from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import IntegerField
from django.core.validators import MaxValueValidator, MinValueValidator

class User(AbstractUser):
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.username}"

class Categories(models.Model):
    category = models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.category}"

class Bids(models.Model):
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")

    def __str__(self):
        return f"{self.user}: {self.amount}"


class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    bid = models.ForeignKey(Bids, on_delete=models.SET_NULL, related_name="listing", null=True)
    startingBid = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.URLField(blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.title} ({self.category})"

class Comments(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comment")

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="watchlist")




