from django.contrib import admin
from .models import Auction, Bid, CustomUser, Comment, Category

# Register your models here.
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(CustomUser)
admin.site.register(Comment)
admin.site.register(Category)