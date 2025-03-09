from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name', 
        'phone_number', 'address', 'nationality', 'specialty', 
        'experience_years', 'language', 'is_staff', 'is_active'
    )
    list_filter = (
        'is_staff', 'is_active', 'language', 'nationality'  # Ajoutez nationality ici
    )
    search_fields = (
        'username', 'email', 'specialty', 'phone_number', 'address', 'nationality'  # Ajoutez les champs ici
    )
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('specialty', 'experience_years', 'language', 'cv', 'phone_number', 'address', 'nationality')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('specialty', 'experience_years', 'language', 'cv', 'phone_number', 'address', 'nationality')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)