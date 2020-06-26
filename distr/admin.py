from django.contrib import admin
from .models import Patient, Status, Room, Position

admin.site.register(Patient)
admin.site.register(Status)
admin.site.register(Room)
admin.site.register(Position)
