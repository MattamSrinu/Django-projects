from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)


class Friend(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    college = models.CharField(max_length=100)
    address = models.TextField()
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)



