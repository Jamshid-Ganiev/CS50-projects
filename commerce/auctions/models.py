from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(default="auctions/media/default_profile_pic.png")

class Bid(models.Model):
    amount = models.FloatField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): 
        return f"${self.amount} bid by {self.user} on {self.date}"

class Auction(models.Model):
    title = models.CharField(max_length=250)
    category = models.CharField(max_length=100, blank=True)
    image_url = models.CharField(max_length=200)
    starting_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name='auctions')
    description = models.TextField()

    def __str__(self): 
        return f"highest bid for <<{self.title}>> is ${self.starting_bid}"


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} for {self.auction.title}"