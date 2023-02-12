from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(default="auctions/media/default_profile_pic.png")


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self): 
        return self.name


class Auction(models.Model):
    title = models.CharField(max_length=250, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=250)
    description = models.TextField(max_length=500, blank=True, default="")
    starting_bid = models.IntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self): 
        return f"{self.title}"
    

class Bid(models.Model):
    auction =models.ForeignKey(Auction, on_delete=models.CASCADE, default=None)
    amount = models.CharField(max_length=9)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self): 
        return f"${self.amount} for {self.auction.title} by {self.user} on {self.date}"


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(max_length=500, default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} for {self.auction.title}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Auction, on_delete=models.CASCADE, default=None)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item.title