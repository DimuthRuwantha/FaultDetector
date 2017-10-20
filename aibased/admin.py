from django.contrib import admin
from .models import TrainingLog, PreFaults

# Register your models here.

admin.site.register(TrainingLog)
admin.site.register(PreFaults)
