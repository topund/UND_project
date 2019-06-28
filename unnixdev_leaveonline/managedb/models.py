from django.db import models
# from django.conf import settings
from django.contrib.auth.models import User

class Department(models.Model):
    dep_name  = models.CharField(max_length=100)
    def __str__(self):
        return self.dep_name

class Position(models.Model):
    pos_name = models.CharField(max_length=100)
    def __str__(self):
        return self.pos_name

class Policytype(models.Model):
    policy_name = models.CharField(max_length=100)
    policy_key = models.CharField(max_length=100)
    class Meta:
        unique_together = (("policy_key"),)
    def __str__(self):
        return self.policy_name

class StatusLeave(models.Model):
    sta_name = models.CharField(max_length=100)
    def __str__(self):
        return self.sta_name

class Policy(models.Model):
    policy_name = models.ForeignKey(Policytype, on_delete=models.CASCADE)
    dep_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    pos_name = models.ForeignKey(Position, on_delete=models.CASCADE)
    numofleave = models.IntegerField(default=0)

    class Meta:
        unique_together = (("policy_name","dep_name","pos_name"),)

    def __str__(self):
        return f'Type: {self.policy_name} |Dep: {self.dep_name} |Pos: {self.pos_name}'

class Sextype(models.Model):
    sex_type = models.CharField(default=None ,max_length=20) 
    def __str__(self):
        return self.sex_type
    
class Statuswork(models.Model):
    status_work = models.CharField(default=None ,max_length=20) 
    def __str__(self):
        return self.status_work