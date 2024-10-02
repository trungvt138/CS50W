from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True, null=False)
    last_name = models.CharField(max_length=50, blank=True, null=False)

class Listing(models.Model):
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.owner.username})"

    def current_bid(self):
        """Returns the current highest bid."""
        highest_bid = self.bids.order_by('-amount').first()
        return highest_bid.amount if highest_bid else self.starting_bid

class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-amount']  # Default ordering by highest bid

    def __str__(self):
        return f"{self.amount} by {self.bidder.username} on {self.auction.title}"

class Comment(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.commenter.username} on {self.auction.title}"
