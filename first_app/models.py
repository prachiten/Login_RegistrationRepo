from django.db import models
from datetime import date,datetime
import re

# Create your models here.
class UserManager(models.Manager):
    def create_validator(self,reqPost):
        errors={}
        given_date = datetime.strptime(reqPost['birthday'], '%Y-%m-%d').date()
        datediff = (datetime.today().date() - given_date).days

        useremail=User.objects.filter(email=reqPost['email'])
        if len(useremail)>=1:
            errors['unique']="Email already taken"
        if len(reqPost['first_name'])<2:
            errors['firstname']="firstname must be at least 2 characters"
        if len(reqPost['last_name'])<2:
            errors['lastname']="lastname must be at least 2 characters"
        if len(reqPost['password'])<8:
            errors['password']="passwords must be at least 8 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPost['email']):
            errors['email'] = ("Invalid email address!")
        if (reqPost['password']!=reqPost['confirm_password']):
            errors['confirmpassword']="password and confirm password should match"
        if (datediff<=0):
            errors['birthday']="Date should be in past"
        if(datediff<4757):
            errors['13yruser']="user must be at least 13 yr old"
        return errors


class User(models.Model):
    first_name=models.TextField()
    last_name=models.TextField()
    email=models.TextField()
    password=models.TextField()
    confirm_password=models.TextField()
    birthday=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
