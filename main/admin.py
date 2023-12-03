from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Student

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('user_type',)


class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('user_type',),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions',
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_type'),
          }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.site_header = "RUNASA C.A.R.E.S Admin"
admin.site.site_title = "RUNASA C.A.R.E.S Admin Area"
admin.site.index_title = "Welcome to the RUNASA C.A.R.E.S Super Admin Area"

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Student)