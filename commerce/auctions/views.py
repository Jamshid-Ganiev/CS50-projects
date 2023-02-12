from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Category, CustomUser, Auction, Bid, Comment, Watchlist
from .forms import AuctionForm

# Create your views here.

def index(request):
    auctions = Auction.objects.all()

    return render(request, "auctions/index.html", {"auctions": auctions})

def listing_details(request, auction_id):
    listing = Auction.objects.get(id=auction_id)
    comments = listing.comments.all()

    return render(request, "auctions/details.html", {"auction": listing, "comments": comments})


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
    
@login_required
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

@login_required
def toggle_watchlist(request, item_id):
    user = request.user
    item = get_object_or_404(Auction, id=item_id)

    try:
        watchlist = Watchlist.objects.get(user=user, item=item)
        if request.method == "POST":
            watchlist.delete()
            messages.success(request, "Item removed from your watchlist.")
        else:
            messages.warning(request, "Item is already in your watchlist.")
    except Watchlist.DoesNotExist:
        Watchlist.objects.create(user=user, item=item)
        messages.warning(request, "Item added to your watchlist.")

    return redirect('auctions:watchlist')
    
def view_watchlist(request):
    user = request.user
    watchlist = Watchlist.objects.filter(user=user)
    context = {
        'watchlist': watchlist,
        'messages': messages.get_messages(request),
    }

    return render(request, 'auctions/watchlist.html', context)

def view_categories(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories
    }

    return render(request, 'auctions/categories.html', context)

def view_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if category != '':
        listings = Auction.objects.filter(category=category)
        context = {
            'category': category,
            'listings': listings,
        }
    else:
        context = {
            'category': "No auctions for this category for now"
        }
    return render(request, 'auctions/category.html', context)

# CREATE DELETE EDIT Comment
def create_comment(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    if request.method == 'POST':
        user = request.user
        comment = request.POST.get('comment')
        if comment:
            Comment.objects.create(user=user, auction=auction, comment=comment)
            return redirect('auctions:details', auction_id=auction_id)
    return render(request, 'auctions/details.html', {'auction': auction})

def delete_comment(request, auction_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect('auctions:details', auction_id=auction_id)

def edit_comment(request, auction_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    auction = Auction.objects.get(id=auction_id)

    if request.user == comment.user:
        if request.method == 'POST':
            comment.comment = request.POST.get('comment')
            comment.save()
            return redirect('auctions:details', auction_id = auction_id)
    return render(request, 'auctions/edit_comment.html', {'comment': comment, 'auction': auction})