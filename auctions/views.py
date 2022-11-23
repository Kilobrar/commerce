from asyncio.windows_events import NULL
from sre_parse import CATEGORIES
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Bids, Categories, Comments, User, Listings, WatchList


def index(request):
    activeListings = Listings.objects.all()
    return render(request, "auctions/index.html", {
        "listings": activeListings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def createListing(request):
    if request.method == "POST":
        title = request.POST["title"]
        startingBid = request.POST["startingBid"]
        description = request.POST["description"]
        url = request.POST["url"]
        categoryName = request.POST["category"]

        category = Categories.objects.get(category=categoryName)

        Listings.objects.create(title=title, startingBid=startingBid, description=description, image=url,category=category, user=request.user)
        return HttpResponseRedirect(reverse("index"))

    
    categories = Categories.objects.all()
    return render(request, "auctions/createListing.html", {
        "categories": categories
    })

def viewListing(request, listing_id, bidSuccess):
    listing = Listings.objects.get(pk=listing_id)
    comments = Comments.objects.filter(listing=listing_id)

    onTheWatchlist = True
    try:
        WatchList.objects.get(listing=listing, user=request.user)
    except:
        onTheWatchlist = False

    try:
        currentPrice = Bids.objects.get(listing = listing_id).amount
    except:
        currentPrice = listing.startingBid

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "onTheWatchlist": onTheWatchlist,
        "comments":comments,
        "currentPrice": currentPrice,
        "bid": bidSuccess
    })

@login_required
def comment(request, listing_id):
    if request.method == "POST":
        listing = Listings.objects.get(pk=listing_id)
        content = request.POST["comment"]

        Comments.objects.create(content=content, user=request.user, listing=listing)
        bidSuccess = NULL
    
    return HttpResponseRedirect(reverse("viewListing", args=(listing_id, bidSuccess)))

@login_required
def watchlist(request):
    listings = WatchList.objects.filter(user = request.user)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required
def addToWatchlist(request, listing_id):
    if request.method == "POST":
        listing = Listings.objects.get(pk=listing_id)
        WatchList.objects.create(listing=listing, user=request.user)

    return HttpResponseRedirect(reverse("watchlist"))

@login_required
def removeFromWatchlist(request, listing_id):
    if request.method == "POST":
        listing = Listings.objects.get(pk=listing_id)
        WatchList.objects.filter(listing=listing, user=request.user).delete()

    return HttpResponseRedirect(reverse("watchlist"))

def categories(request):
    categories = Categories.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def categoryListing(request, category_id):
    listings = Listings.objects.filter(category=category_id)
    category = Categories.objects.get(pk=category_id)
    return render(request, "auctions/categoryListing.html", {
        "listings": listings,
        "category": category
    })

@login_required
def placeBid(request, listing_id):
    if request.method == "POST":
        bid = int(request.POST["bid"])
        listing = Listings.objects.get(pk=listing_id)

        try:
            currentPrice = int(Bids.objects.get(pk=listing_id).amount)
        except:
            currentPrice = int(listing.startingBid)

        if bid > currentPrice:
            Bids.objects.filter(pk=listing_id).delete()
            bidInstance = Bids.objects.create(user=request.user, amount=bid)
            listing.bid = bidInstance
            listing.save()
            bidSuccess = "Success"
        else:
            bidSuccess= "Unsuccess"

        return HttpResponseRedirect(reverse("viewListing", args=(listing_id, bidSuccess)))


