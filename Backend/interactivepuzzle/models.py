from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
import datetime


class CustomUser(AbstractUser):
    took_test = models.BooleanField(default=False)
    accuracy = models.FloatField(default=0)
    lives = models.IntegerField(default=3)


class question(models.Model):
    question_title = models.CharField(max_length=500)
    question_text = models.CharField(max_length=800)
    question_description = models.CharField(max_length=4000)
    clues = models.CharField(max_length=4000)
    pub_date = models.DateTimeField("date published")
    answer = models.CharField(max_length=400, default="Default Answer")
    image = models.CharField(max_length=1000)


class session(models.Model):
    question = models.ForeignKey(question, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    startTime = models.DateTimeField()
    endTime = models.DateField(null=True)


class submissions(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(question, on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=0)
    timeStart = models.DateTimeField()
    timeEnd = models.DateTimeField()
    score = models.FloatField(default=0)
