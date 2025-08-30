from django.contrib import admin
from .models import ApiKeys


@admin.register(ApiKeys)
class ApiKeysAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'cloudsite', 'apikey')
    list_filter = ('cloudsite',)
    search_fields = ('user__email', 'cloudsite', 'apikey')
    ordering = ('-id',)

    fieldsets = (
        ("API Key Info", {
            "fields": ("user", "cloudsite", "apikey")
        }),
    )
    
    readonly_fields = ('apikey',)

