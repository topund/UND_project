from django.db import models
from django.contrib.auth.models import User
from managedb.models import Policy, StatusLeave, Policytype
from users.models import Profile, Remainleavedays, Suppervisor

class History(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    leaveday_begin = models.DateTimeField()
    leaveday_end = models.DateTimeField()
    policy = models.ForeignKey(Policytype, on_delete=models.CASCADE)
    policy_ref = models.ForeignKey(Remainleavedays, on_delete=models.CASCADE)
    explanation = models.CharField(default='',max_length=300)
    user_sup = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sup')
    sta_sup = models.ForeignKey(StatusLeave, on_delete=models.CASCADE, related_name='status_sup')
    user_hr = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_hr')
    sta_hr = models.ForeignKey(StatusLeave, on_delete=models.CASCADE, related_name='status_hr')
    sta_user = models.ForeignKey(StatusLeave, on_delete=models.CASCADE, related_name='status_user')

    # def __str__(self):
    #     return self.user
