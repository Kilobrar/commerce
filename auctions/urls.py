from unicodedata import name
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("<int:listing_id>/viewListing/<str:bidSuccess>", views.viewListing, name="viewListing"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    path("<int:listing_id>/placeBid", views.placeBid, name="placeBid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/addToWatchlist", views.addToWatchlist, name="addToWatchlist"),
    path("<int:listing_id>/removeFromWatchlist", views.removeFromWatchlist, name="removeFromWatchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.categoryListing, name="categoryListing")
]

urlpatterns += staticfiles_urlpatterns()
