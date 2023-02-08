from django import forms
from .models import Auction, Bid, Comment


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'category', 'image_url', 'starting_bid', 'description']