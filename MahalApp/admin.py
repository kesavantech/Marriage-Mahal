from django.contrib import admin
from MahalApp.models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    readonly_fields = ('name', 'email', 'phone', 'message', 'created_at')
