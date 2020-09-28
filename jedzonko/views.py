from datetime import datetime
from random import shuffle

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from jedzonko.models import Recipe


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class Dashobard(View):

    def get(self, request):
        return render(request, 'dashboard.html')

def main_page(request):
    recipes = [recipe for recipe in Recipe.objects.all()]
    shuffle(recipes)
    return render(request, "index.html", {'recipes': recipes[:3], 'active_carousel_recipe_name': recipes[0].name})

