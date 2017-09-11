from django.db import models

# Create your models here.


class TrainingLog(models.Model):
    time = models.DateTimeField()
    train_ratio = models.IntegerField(max_length=2)
    algorithm_name = models.CharField(max_length=20)
    hidden_layer_nodes = models.IntegerField(max_length=2)
    accuracy_tested = models.BooleanField(default=False)
    trained_inputs = models.IntegerField()
    tested_inputs = models.IntegerField()
    accuracy = models.IntegerField()
