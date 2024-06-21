from django.db import models
import re
from datetime import date

class UsersManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        Name_REGEX = re.compile(r'^[a-zA-Z]+$')
        if len(postData['first_name']) <= 2 or not Name_REGEX.match(postData['first_name']):
            errors["first_name"] = "First name should be at least 2 characters"
            
        if len(postData['last_name']) <= 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if self.filter(email=postData['email']).exists():
            errors['email'] = "Email already exists. Please use a different email address."

        if not EMAIL_REGEX.match(postData['email']):   
            errors['email'] = "Invalid email address!"

        if len(postData['password']) <= 8:
            errors["password"] = "password should be at least 8 characters"

        if  postData['password'] != postData['Confirmpassword']:
            errors["Confirmpassword"] = "password didnt match"

        return errors
    

class Users(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    objects = UsersManager()




