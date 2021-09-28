from django.db import models

# Create your models here.

class Permission(models.Model):
    name = models.CharField(max_length=200)

class Role(models.Model):
    name = models.CharField(max_length=200)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return str(self.name)


class User(models.Model):
    user_id = models.CharField(max_length=30,primary_key=True)
    name=models.CharField(max_length=200)
    email_id=models.CharField(max_length=200,unique=True)
    address=models.CharField(max_length=200,null=True)
    password=models.CharField(max_length=200)
    role=models.ForeignKey(Role,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return str(self.user_id)

    

    
