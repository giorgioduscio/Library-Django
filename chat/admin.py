from django.contrib import admin
from .models import Room, Message

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    search_fields =['name']
    ordering =['-created_at']
    list_display =['id', 'name', 'created_at']
    list_filter =['created_at']
    list_editable =['name']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    search_fields =['text']
    ordering =['-created_at']
    list_display =['id', 'text', 'created_at', 'user__username', 'room__name']
    list_filter =['created_at', 'user__username', 'room__name']
    list_editable =['text']
    
