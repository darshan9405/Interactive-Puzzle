from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    took_test = False

class question(models.Model):
    question_text = models.CharField(max_length=400)
    pub_date = models.DateTimeField("date published")
    answer = models.CharField(max_length=400,default="Default Answer")

class submissions(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timeStart = models.DateTimeField()
    timeEnd = models.DateTimeField()
    score = 0
