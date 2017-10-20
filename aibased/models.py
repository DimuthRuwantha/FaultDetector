from django.db import models

# Create your models here.


class TrainingLog(models.Model):
    time = models.DateTimeField()
    train_ratio = models.IntegerField()
    algorithm_name = models.CharField(max_length=20)
    hidden_layer_nodes = models.IntegerField()
    accuracy_tested = models.BooleanField(default=False)
    trained_inputs = models.IntegerField()
    tested_inputs = models.IntegerField()
    accuracy = models.IntegerField()


class PreFaults(models.Model):
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    fault = models.CharField(max_length=100)
