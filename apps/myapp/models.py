from django.db import models
from datetime import datetime
import bcrypt, re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Userobjects(models.Manager):
    def reg_validator(self, request):

        errors = {}

        user = User.objects.filter(username=request.POST['username'])

        if len(user) > 0:
            errors['username'] = "An account with that username already exists"

        if len(request.POST['name']) < 3:
            errors['name'] = "Name must be at least 3 characters long"

        if len(request.POST['username']) < 2:
            errors['username'] = "Username must be at least 3 characters long"

        if len(request.POST['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"

        elif request.POST['password_confirmation'] != request.POST['password']:
            errors['password'] = "Passwords do not match"

        return errors

    def login_validator(self, request):
        errors = {}
        if len(request.POST['username']) < 1:
            errors['username'] = "Username cannot be blank"
        elif len(User.objects.filter(username = request.POST['username'])) < 1:
            errors['username']  = "Please register with us before trying to login"
        else:
            user = User.objects.get(username = request.POST['username'])
            if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                errors['password'] = "Your password was entered incorrectly, please try again"
            else:
                request.session['user_id'] = user.id
        return errors

class Wishlistobjects(models.Manager):
    def wishlist_validator(self, request):
        errors = {}
        if len(request.POST['item']) < 1:
            errors['item'] = "item title needs to be at least 1 characters long"
        if len(errors) > 1:
                items = wishlist.objects.create(item=request.POST['item'], created_on=request.POST['date'], planner_id=request.session['user_id'])
                user = User.objects.get(id=request.session['user_id'])
                user.joins.add(items)
        return errors

class User(models.Model):
    name= models.CharField(max_length=255)
    username= models.CharField(max_length=255)
    password= models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    objects = Userobjects()


class Wishlist(models.Model):
    item = models.CharField(max_length=255)
    description = models.CharField(max_length=4)
    created_on = models.DateField()
    planner = models.ForeignKey(User, related_name="items", on_delete=models.CASCADE)
    adds = models.ManyToManyField(User, related_name="adds")
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    objects = Wishlistobjects()