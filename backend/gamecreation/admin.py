from django.contrib import admin
from .models import PokerBoard, pokermember


@admin.register(PokerBoard)
class PokerBoardAdmin(admin.ModelAdmin):
   
    list_display = ('pokerid', 'game_name', 'game_description')
    search_fields = ('game_name', 'game_description')
    ordering = ('-pokerid',)


@admin.register(pokermember)
class PokerMemberAdmin(admin.ModelAdmin):
  
    list_display = ('id', 'poker', 'member', 'role', 'accept')
    list_filter = ('role', 'accept')
    search_fields = ('member__email', 'poker__game_name')
    ordering = ('-id',)
    autocomplete_fields = ('poker', 'member')
