from django.contrib import admin
from .models import Tournament, Match, TournamentParticipant

@admin.register(Tournament)  # Более элегантный способ регистрации
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'format', 'start_date', 'is_active', 'is_completed')
    list_filter = ('format', 'system', 'is_active')
    search_fields = ('name', 'location')
    readonly_fields = ('created_at', 'updated_at')

# Другие модели можно зарегистрировать так же
admin.site.register(Match)
admin.site.register(TournamentParticipant)
