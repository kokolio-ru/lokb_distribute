from django.db import models

# Create your models here.


class Status(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Patient(models.Model):
    name = models.CharField(max_length=100)
    diagnosis = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(null=True)
    doctor_comment = models.TextField(null=True, blank=True)
    important = models.BooleanField(default=False)
    distributed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Room(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Position(models.Model):
    title = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
