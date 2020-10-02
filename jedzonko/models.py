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

    @staticmethod
    def is_in_database(name, ingredients, description, preparation_description, preparation_time):
        counter = Recipe.objects.filter(name=name, ingredients=ingredients, description=description,
                                        preparation_description=preparation_description,
                                        preparation_time=preparation_time).count()
        return counter > 0

    def ingredients_as_list(self):
        if "," in self.ingredients:
            lst = self.ingredients.split(",")
        else:
            lst = self.ingredients.split()
        return lst

    def __str__(self):
        return f'{self.name[:50]}'


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through='RecipePlan')

    @staticmethod
    def plan_amount():
        return Plan.objects.all().count()

    def __str__(self):
        return f'{self.name[:30]}'


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=255)
    order = models.IntegerField()
    day_name = models.ForeignKey('DayName', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('meal_name', 'day_name', 'plan'), ('order', 'day_name', 'plan'))

    def __str__(self):
        return f'{self.plan} - {self.day_name}: {self.meal_name} - {self.recipe}'


class DayName(models.Model):
    day_name = models.CharField(max_length=16)
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.day_name


class Page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.title
