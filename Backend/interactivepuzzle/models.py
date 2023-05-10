from django.db import models

# Create your models here.


class user(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)


class question(models.Model):
    question_text = models.CharField(max_length=400)
    pub_date = models.DateTimeField("date published")
