from django.db import models
from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    dep_name  = models.CharField(max_length=100)
    def __str__(self):
        return self.dep_name

class Position(models.Model):
    pos_name = models.CharField(max_length=100)
    def __str__(self):
        return self.pos_name

class Sextype(models.Model):
    sex_type = models.CharField(default=None ,max_length=20) 
    def __str__(self):
        return self.sex_type
    
class Statuswork(models.Model):
    status_work = models.CharField(default=None ,max_length=20) 
    def __str__(self):
        return self.status_work
        
class User(AbstractUser):
    dep_name = models.ForeignKey(Department, null=True, on_delete=models.CASCADE)
    pos_name = models.ForeignKey(Position, null=True, on_delete=models.CASCADE)
    status_work = models.ForeignKey(Statuswork, null=True, on_delete=models.CASCADE)
    sex = models.ForeignKey(Sextype, null=True, on_delete=models.CASCADE)
    
    line = models.CharField(blank=True ,max_length=100)
    nickname = models.CharField(blank=True ,max_length=50) 
    dateofbirth = models.DateTimeField(null=True, blank=True)
    dateofstart = models.DateTimeField(null=True, blank=True)
    phone = models.CharField(blank=True ,max_length=100)
    address = models.CharField(blank=True ,max_length=500)
    
    @property
    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name)