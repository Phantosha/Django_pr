from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(BaseUserAdmin):
    # Поля, отображаемые в списке пользователей
    list_display = ('username', 'email', 'first_name', 'last_name', 'rating', 'gender', 'is_staff')

    # Поля для фильтрации
    list_filter = ('is_staff', 'is_active', 'gender')

    # Поля для поиска
    search_fields = ('username', 'first_name', 'last_name', 'rating')

    # Добавляем кастомные поля в форму редактирования пользователя
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email', 'phone', 'birth_date', 'gender', 'avatar')}),
        (_('Petanque stats'), {'fields': ('rating', 'games_played', 'wins', 'rating_history')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Поля, которые будут в форме создания нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'rating'),
        }),
    )

    # Поля только для чтения (например, рейтинг можно сделать только для чтения)
    readonly_fields = ('rating_history', 'date_joined', 'last_login')

    # Порядок сортировки
    ordering = ('-rating', 'username')


# Регистрируем модель User с нашим классом администрирования
admin.site.register(User, UserAdmin)
