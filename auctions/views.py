from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

# main page where all the auctions are listed
def index(request):
    # if a new auction has been created
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        user = User.objects.get(pk=request.user.id)
        bid = Bid()
        bid.bid_price = request.POST.get("bid")
        bid.bid_count = 1
        bid.bid_user = user
        bid.save()
        # bid = request.POST.get("bid")
        image_url = request.POST.get("image url")
        category = request.POST.get("category")
        
        listing = Listing(title=title, description=description, bid=bid, image_url=image_url, category=category, user=user)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    #end
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.exclude(is_closed = True).all()
    })

def categories(request):
    return render(request, "auctions/categories.html")

def category(request, category_name):
    return render(request, "auctions/category.html", {
        "listings": Listing.objects.filter(is_closed = False, category = category_name),
        "category_name": category_name
    })

# for a specific item
def item(request, item_no):
    item = Listing.objects.get(id=item_no)
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
    if request.method == "POST":

        # if bid is changed
        if "bid" in request.POST:
            new_bid = int(request.POST.get("bid"))
            if new_bid <= item.bid.bid_price or new_bid == None:
                return render(request, "auctions/item.html", {
                    "message" : "Bid must be higher than the current price",
                    "item": item
                })
            else:
                bid = item.bid
                bid.bid_price = new_bid
                bid.bid_count = bid.bid_count + 1
                bid.bid_user = user
                bid.save()
                #item.save()
        
        # if auction is closed
        elif "close" in request.POST:
            item.is_closed = True
            item.save()
            return render(request, "auctions/item.html", {
                "item": item
            })
        
        # if added/removed watchlist
        elif "watchlist" in request.POST:
            flag = True
            for listing in user.watchlist.all():
                if (item.id == listing.id):
                    user.watchlist.remove(item)
                    flag = False
                    w_message = "Item removed from watchlist"
            if (flag == True):
                user.watchlist.add(item)
                w_message = "Item added to watchlist"
            return render(request, "auctions/item.html", {
                "item": item,
                "w_message": w_message
            })

        # if comment is added
        elif "comment" in request.POST:
            comment = Comment()
            comment_text = request.POST.get("comment")
            comment_user = user
            comment.comment_text = comment_text
            comment.comment_user = comment_user
            comment.save()
            item.comment.add(comment)

    return render(request, "auctions/item.html", {
        "item": item
    })

# create listing
def create(request):    
    return render(request, "auctions/create.html")

# watchlist
def watchlist(request):
    user = User.objects.get(pk=request.user.id)
    return render(request, "auctions/watchlist.html", {
        "watchlist": user.watchlist.all()
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
