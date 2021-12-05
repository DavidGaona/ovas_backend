from django.contrib import admin

# Register your models here.
from api.models import Ova, OvaUser

admin.site.register(Ova)
admin.site.register(OvaUser)
