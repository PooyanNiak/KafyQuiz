from django.db import models
from django.contrib.auth import get_user_model

class UserInfo(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="infos")

    @staticmethod
    def get(user):
        try:
            return UserInfo.objects.get(user=user)
        except:
            return UserInfo.objects.create(user=user)
        
class Question(models.Model):
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="questions")
    a = models.IntegerField(default=0)
    b = models.IntegerField(default=0)
    c = models.IntegerField(default=0)
    answer = models.BooleanField(default=False)
    remained = models.IntegerField(default=0)

class Submit(models.Model):
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="submits")
    value = models.CharField(max_length=128, blank=True, null=True)
    answer = models.BooleanField(default=False) 