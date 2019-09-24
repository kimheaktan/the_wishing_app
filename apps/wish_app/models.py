from django.db import models
from django.contrib import messages
from django.contrib.messages import get_messages
import re




class UserManager(models.Manager):
    def reg_valid(self, request):
        if len(request.POST['password']) < 8:
            messages.error(request, "Password must consist of at least 7 characters")

        if request.POST["password"] != request.POST["password_confirm"]:
            messages.error(request, "Password must match confirm password")

        if len(request.POST["first_name"]) < 3:
            messages.error(request, "First Name must be at least 3 characters")

        if len(request.POST["last_name"]) < 3:
            messages.error(request, "Last Name must be at least 3 characters")

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(request.POST['email']):
            messages.error(request,'Invalid email address!')


        storage = messages.get_messages(request)
        storage.used = False
        return len(storage) == 0

class WishManager(models.Manager):
    def wish_valid(self, request):
        if len(request.POST['wish']) < 1:
            messages.error(request, 'A wish must be provided')

        if len(request.POST['wish']) < 3:
            messages.error(request, "A wish must consist of at least 3 characters")

        if len(request.POST['description'])  < 1:
            messages.error(request, "A description must be provided")

        if len(request.POST['description']) < 3:
            messages.error(request,'A description must consister of at least 3 characters')


        storage = messages.get_messages(request)
        storage.used = False
        return len(storage) == 0

class NewWishManager(models.Manager):
    def new_wish_valid(self, request):

        if len(request.POST['new_wish']) < 3:
            messages.error(request, "A new wish must consist of at least 3 characters ")

        if len(request.POST['new_description']) < 3:
            messages.error(request, "A new description must be at least 3 characters")
            

        storage = messages.get_messages(request)
        storage.used = False
        return len(storage) == 0

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255) 
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wish(models.Model):
    wish = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    isGranted = models.BooleanField(default=False)
    wisher = models.ForeignKey(User,related_name='created_wishes')
    likers = models.ManyToManyField(User, related_name='liked_wishes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    objects = WishManager()

class NewWish(models.Model):
    objects = NewWishManager()
 




