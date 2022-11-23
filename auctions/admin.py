from xml.etree.ElementTree import Comment
from django.contrib import admin

from .models import Bids, Categories, Comments, Listings, User, WatchList
# Register your models here.
admin.site.register(User)
admin.site.register(Comments)
admin.site.register(Bids)
admin.site.register(WatchList)
admin.site.register(Listings)
admin.site.register(Categories)