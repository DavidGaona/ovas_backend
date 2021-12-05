from django.contrib import admin

# Register your models here.
from api.models import Ova, OvaUser

admin.site.site_header = 'Administración de Ovas'


class OvaAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'date', 'language', 'publisher', 'uploader', 'active', 'link',)
    list_filter = ('date', 'active', 'language', 'creator', 'subject')
    readonly_fields = ('id', 'date')
    sortable_by = 'date'
    search_fields = ('creator', 'language', 'subject', 'title')


admin.site.register(Ova, OvaAdmin)
admin.site.register(OvaUser)
