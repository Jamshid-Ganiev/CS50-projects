from django.forms import ModelForm
from .models import Auction, Bid, Comment


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'category', 'image_url', 'starting_bid', 'description']