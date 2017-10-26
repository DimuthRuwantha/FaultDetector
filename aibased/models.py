from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class TrainingLog(models.Model):
    # trained_by = models.CharField(max_length=20)
    trained_by = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()
    train_ratio = models.IntegerField()
    algorithm_name = models.CharField(max_length=20)
    hidden_layer_nodes = models.IntegerField()
    accuracy_tested = models.BooleanField(default=False)
    trained_inputs = models.IntegerField()
    tested_inputs = models.IntegerField()
    accuracy = models.IntegerField()


class PreFault(models.Model):
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    fault = models.CharField(max_length=100)
    i_a = models.FloatField()
    i_b = models.FloatField()
    i_c = models.FloatField()
    v_a = models.FloatField()
    v_b = models.FloatField()
    v_c = models.FloatField()

