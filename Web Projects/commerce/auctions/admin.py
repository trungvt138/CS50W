from django.contrib import admin
from .models import Listing, Bid, User
# Register your models here.
 # Import your models here

# Register the Listing model
admin.site.register(Listing)

# If you want to manage Bids in the admin, you can also register the Bid model
admin.site.register(Bid)

admin.site.register(User)