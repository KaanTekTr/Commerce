from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.expressions import F


class Bid(models.Model):
    bid_price = models.IntegerField(default=0)
    bid_count = models.IntegerField(default=1)
    bid_user = models.ForeignKey('User', on_delete=models.CASCADE, null=True , related_name="bid")

    def __str__(self):
        return f"Bid {self.id}: {self.bid_price}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    image_url = models.URLField(blank=True)
    category = models.CharField(default="Not Specified", blank=True, max_length=64)
    user = models.ForeignKey('User', on_delete=CASCADE, null=False ,related_name="listings")
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="listing")
    is_closed = models.BooleanField(default=False)
    # comment = models.ForeignKey(Comment, on_delete=CASCADE, null=True, related_name="listing")
    comment = models.ManyToManyField('Comment', blank=True, related_name="listing")

    def __str__(self):
        return f"Listing {self.id}: {self.title} by {self.user.username}"

class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watchlist_user")

class Comment(models.Model):
    comment_text = models.CharField(max_length=30)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="comment")
    # listing = models.ForeignKey(Listing, on_delete=CASCADE, null=True, related_name="comment")

    def __str__(self):
        return f"{self.comment_user.username}: {self.comment_text}"

