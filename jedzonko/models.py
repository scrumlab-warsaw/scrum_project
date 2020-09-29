from django.db import models


# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_description = models.TextField(default='')
    preparation_time = models.IntegerField()
    votes = models.IntegerField(default=0)

    @staticmethod
    def recipe_amount():
        return Recipe.objects.all().count()


class Schedule(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def schedule_amount():
        return Schedule.objects.all().count()
