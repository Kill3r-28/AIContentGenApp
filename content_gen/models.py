from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserRequestTrack(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    difficulty = models.CharField(choices=[("easy", "EASY"), ("medium", "MEDIUM"), ("hard", "HARD")], max_length=10)
    question_type = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    subtopic = models.CharField(max_length=100)
    question_count = models.PositiveIntegerField()
    input_token = models.PositiveIntegerField()
    output_token = models.PositiveIntegerField()
