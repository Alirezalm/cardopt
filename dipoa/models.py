from django.contrib.auth.models import User
from django.db import models

PROBLEM_CLASSES = (
    ('dslr', 'distributed logistic regression'),
    ('dspo', 'distributed sparse portfolio optimization')
)


class ProblemInstance(models.Model):
    name = models.CharField(max_length=100, choices=PROBLEM_CLASSES)
    number_of_features = models.IntegerField()
    number_of_samples = models.IntegerField()
    number_of_constraints = models.IntegerField()
    number_of_nonzeros = models.IntegerField()
    number_of_cores = models.IntegerField()
    optimal_obj = models.CharField(max_length = 100, null = True)
    relative_gap = models.CharField(max_length = 100, null = True)
    max_iter = models.CharField(max_length = 100, null = True)
    elapsed_time = models.CharField(max_length = 100, null = True)


class ProblemInfo(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    problem_info = models.ForeignKey(ProblemInstance, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
