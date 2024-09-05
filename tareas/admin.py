from django.contrib import admin
from .models import Tareas
# Register your models here.

class Tareasadmin(admin.ModelAdmin):
    readonly_fields=('created', )
admin.site.register(Tareas, Tareasadmin)