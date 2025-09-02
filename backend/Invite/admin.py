from django.contrib import admin
from .models import Invite

@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
   
    list_display = ('id', 'pokerboard', 'host', 'guest', 'role', 'accept')
    list_filter = ('role', 'accept', 'pokerboard')
    search_fields = ('guest', 'host__email', 'pokerboard__id')
    ordering = ('-id',)
    fieldsets = (
        ("Invite Info", {
            "fields": ("pokerboard", "host", "guest", "role")
        }),
        ("Status", {
            "fields": ("accept",)
        }),
    )
 
