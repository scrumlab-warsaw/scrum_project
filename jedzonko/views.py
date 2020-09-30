from datetime import datetime
from random import shuffle

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from jedzonko.models import Recipe, Plan


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class Dashobard(View):

    def get(self, request):
        latest_plan = Plan.objects.all().order_by('-created')[0]
        recipe_plans = latest_plan.recipeplan_set.all().order_by('-day_name__order')
        day_plans = []
        for i in range(7):
            plans_for_day = recipe_plans.filter(day_name__order=i).order_by('order')
            if len(plans_for_day) > 0:
                day_plans.append((plans_for_day[0].day_name.day_name, plans_for_day))

        print(day_plans)
        context = {
            'recipe_amount': Recipe.recipe_amount(), 'plan_amount': Plan.plan_amount(), 'day_plans': day_plans, 'latest_plan': latest_plan
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
        if (name == '' or description == '' or preparation_time == '' or
                preparation_description == '' or ingredients == ''):
            context = {'wrong_input': 'Wypełnij poprawnie wszystkie pola.',
                       'recipe_name': name,
                       'description': description,
                       'preparation_time': preparation_time,
                       'preparation_description': preparation_description,
                       'ingredients': ingredients
                       }
            return render(request, 'app-add-recipe.html', context)

        Recipe.objects.create(name=name, ingredients=ingredients, description=description,
                              preparation_description=preparation_description,
                              preparation_time=preparation_time)
        return redirect('recipe_list')


def recipe_modify(request, recipe_id):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia


def plan_details(request, plan_id):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia


def plan_add(request):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia


def add_recipe_to_plan(request):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia

