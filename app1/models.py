from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email address"
        if User.objects.filter(email = postData['email']).exists():
            errors['email'] = "Email already exists."
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm']:
            errors['confirm'] = "Passwords do not match"
        return errors
    
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class PaintingManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['title']) < 2:
            errors["title"] = "Title is required and should be at least 2 characters"
        if len(postData['description']) < 10:
            errors["description"] = "Description is required and should be at least 5 characters"
        if float(postData['price']) <= 0 :
            errors["price"] = "Price should be greater than 0"
        if int(postData['quantity']) <= 0 :
            errors["quantity"] = "Quantity should be greater than 0"
        return errors
    
class Painting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price=models.FloatField()
    painted_by = models.ForeignKey(User, related_name="paintings",on_delete = models.CASCADE)
    quantity=models.IntegerField()
    users_who_purchased = models.ManyToManyField(User, related_name="purchased_paintings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def purchased(self):
        return self.users_who_purchased.count() 
    objects = PaintingManager()
# Create your models here.
