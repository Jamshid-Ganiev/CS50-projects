from django.shortcuts import redirect, render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import CustomUser, Auction, Bid, Comment
from .forms import AuctionForm


def index(request):
    auctions = Auction.objects.all()

    return render(request, "auctions/index.html", {"auctions": auctions})

def listing_details(request, listing_id):
    listing = Auction.objects.get(id=listing_id)

    return render(request, "auctions/details.html", {"auction": listing})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
            user = CustomUser.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
    

def create_listing(request):
    template_name = 'auctions/create_listing.html'

    if request.method == 'GET':
        form = AuctionForm()
        return render(request, template_name, {'form': form})

    if request.method == 'POST':
        form = AuctionForm(request.POST)

        if form.is_valid():
            listing = form.save(commit=False)
            listing.save()
            return redirect('auctions:index')

        return render(request, template_name, {'form': form})
    