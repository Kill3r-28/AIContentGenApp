from django.contrib import admin
from .models import UserRequestTrack

@admin.register(UserRequestTrack)
class UserRequestTrackAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'timestamp',
        'difficulty',
        'question_type',
        'topic',
        'subtopic',
        'question_count',
        'input_token',
        'output_token',
    )
    list_filter = (
        'difficulty',
        'question_type',
        'topic',
        'subtopic',
        'timestamp',
    )
    search_fields = (
        'user__username',
        'question_type',
        'topic',
        'subtopic',
    )
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)

