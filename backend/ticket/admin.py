from django.contrib import admin
from .models import ticket, estimate


@admin.register(ticket)
class TicketAdmin(admin.ModelAdmin):
    
    list_display = (
        'id', 'summary', 'type', 'priority', 'pokerid',
        'finalEstimate', 'import_type'
    )
    list_filter = ('type', 'priority', 'import_type', 'pokerid')
    search_fields = ('summary', 'key', 'ticket')
    ordering = ('-id',) 
    readonly_fields = () 
    fieldsets = (
        ("Ticket Info", {
            "fields": ("pokerid", "key", "summary", "description", "priority", "type", "import_type")
        }),
        ("Estimates", {
            "fields": ("finalEstimate",)
        }),
        ("Extra", {
            "fields": ("ticket",)
        }),
    )


@admin.register(estimate)
class EstimateAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'ticket', 'user', 'estimate', 'estimate_date')
    list_filter = ('estimate_date', 'estimate')
    search_fields = ('ticket__summary', 'user__username')
    ordering = ('-estimate_date',)

