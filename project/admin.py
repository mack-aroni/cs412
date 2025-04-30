from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(PocketProfile)
admin.site.register(Card)
admin.site.register(OwnedBy)
admin.site.register(PocketFriend)
admin.site.register(PocketFriendRequest)
admin.site.register(TradeRequest)