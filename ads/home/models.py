from django.db import models

class Confirm(models.Model):
    username = models.TextField()
    name = models.TextField()
    email = models.TextField()
    password = models.TextField()
    otp = models.TextField()
    attempts = models.IntegerField(default=0)

class Password(models.Model):
    email = models.TextField()
    otp = models.TextField()
    confirmed = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)