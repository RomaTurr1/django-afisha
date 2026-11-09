from django.contrib import admin
from .models import Category, Event


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'event_date', 'location', 'price', 'is_finished')
    list_filter = ('category', 'is_finished', 'event_date')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'event_date'
