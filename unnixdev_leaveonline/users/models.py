from django.db import models
from django.contrib.auth.models import User
from managedb.models import Department, Position, Policy, Statuswork, Sextype

class Suppervisor(models.Model):
    
    dep_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    sup_name = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("dep_name","sup_name"),)

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dep_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    pos_name = models.ForeignKey(Position, on_delete=models.CASCADE)
    status_work = models.ForeignKey(Statuswork, on_delete=models.CASCADE)
    sex = models.ForeignKey(Sextype, on_delete=models.CASCADE)
    line = models.CharField(default=None ,max_length=100)
    firstname = models.CharField(default=None ,max_length=100)
    lastname = models.CharField(default=None ,max_length=100) 
    nickname = models.CharField(default=None ,max_length=50) 
    dateofbirth = models.DateTimeField(default=None)
    dateofstart = models.DateTimeField(default=None)
    phone = models.CharField(default=None ,max_length=100)
    address = models.CharField(default=None ,max_length=500)
    
    class Meta:
        unique_together = (("user"),)

class Remainleavedays(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    remain_days = models.IntegerField(default=0)

    class Meta:
        unique_together = (("user","policy"),)

