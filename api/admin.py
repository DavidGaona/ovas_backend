from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group
from api.models import Ova, OvaUser, Score, Subject

admin.site.site_header = 'Administración de Ovas'


class OvaAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'date', 'language', 'publisher', 'uploader', 'active', 'link',)
    list_filter = ('active', 'language',)
    readonly_fields = ('id',)
    sortable_by = 'date'
    search_fields = ('creator', 'language', 'subject', 'title',)


admin.site.register(Ova, OvaAdmin)


class OvaUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'cedula', 'is_active', 'last_login', 'date_joined')
    list_filter = ('is_active',)
    readonly_fields = ('id', 'last_login', 'date_joined')
    exclude = ('is_staff', 'groups', 'user_permissions', 'is_superuser', 'password')


admin.site.register(OvaUser, OvaUserAdmin)


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'ova_id', 'score',)
    readonly_fields = ('id', 'user_id', 'ova_id', 'score',)


admin.site.register(Score, ScoreAdmin)

admin.site.register(Subject)
