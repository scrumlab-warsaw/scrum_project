from datetime import datetime
from random import shuffle

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from jedzonko.models import Recipe, Plan


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class Dashobard(View):

    def get(self, request):
        context = {
            'recipe_amount': Recipe.recipe_amount(), 'plan_amount': Plan.plan_amount()
            }
        return render(request, 'dashboard.html', context)


    


def main_page(request):
    recipes = [recipe for recipe in Recipe.objects.all()]
    shuffle(recipes)
    return render(request, "index.html", {'recipes': recipes[:3], 'active_carousel_recipe_name': recipes[0].name})


def recipe_details(request, recipe_id):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia


def recipe_list(request):
    return render(request, 'app-recipes.html')


def plan_list(request):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia


def recipe_add(request):
    if request.method == 'GET':
        return render(request, 'app-add-recipe.html')
    if request.method == 'POST':
        name = request.POST.get('recipe_name')
        description = request.POST.get('description')
        preparation_time = request.POST.get('preparation_time')
        preparation_description = request.POST.get('preparation_description')
        ingredients = request.POST.get('ingredients')
        print(name)
        print(description)
        print(preparation_time)
        print(preparation_description)
        print(ingredients)
        return render(request, 'app-add-recipe.html')



def recipe_modify(request, recipe_id):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia


def plan_details(request, plan_id):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia


def plan_add(request):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia


def add_recipe_to_plan(request):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia
