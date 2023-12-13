from django.contrib import admin
from userauths.models import User

# Register your models here.

class Admin(admin.ModelAdmin):
    list_display = ['username', 'email', 'about']

admin.site.register(User, Admin)
