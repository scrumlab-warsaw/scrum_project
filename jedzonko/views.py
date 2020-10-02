from datetime import datetime
from random import shuffle
from math import ceil

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from jedzonko.models import Recipe, Plan, RecipePlan


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class Dashobard(View):

    def get(self, request):
        latest_plan = Plan.objects.all().order_by('-created')[0]
        plan_recipes = latest_plan.recipeplan_set.all().order_by('-day_name__order')
        days = []
        for i in range(1, 8):
            recipes_for_day = plan_recipes.filter(day_name__order=i).order_by('order')
            if len(recipes_for_day) > 0:
                days.append((recipes_for_day[0].day_name, recipes_for_day))

        context = {
            'recipe_amount': Recipe.recipe_amount(),
            'plan_amount': Plan.plan_amount(),
            'days': days,
            'latest_plan': latest_plan,
        }
        return render(request, 'dashboard.html', context)


def main_page(request):
    recipes = [recipe for recipe in Recipe.objects.all()]
    shuffle(recipes)
    return render(request, "index.html", {'recipes': recipes[:3], 'active_carousel_recipe_name': recipes[0].name})


def recipe_details(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    context = {'recipe': recipe, }
    return render(request, 'app-recipe-details.html', context)


def recipe_list(request):
    return render(request, 'app-recipes.html')


def plan_list(request):
    PLANS_PER_PAGE = 50
    plans = [plan for plan in Plan.objects.all().order_by('name')]
    plans = [(i, plan) for i, plan in enumerate(plans, 1)]
    paginator = Paginator(plans, PLANS_PER_PAGE)
    page_number = int(request.GET.get('page', 1))
    page_obj = paginator.get_page(page_number)
    page_numbers = [i for i in range(page_number - 2, page_number + 3) if 0 < i <= ceil(len(plans) / PLANS_PER_PAGE)]
    return render(request, 'app-schedules.html', {'page_obj': page_obj, 'page_numbers': page_numbers})


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


def recipe_modify(request, recipe_id):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia


def plan_details(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    recipes_plans = plan.recipeplan_set.all().order_by('order')
    meals_for_day = []
    for i in range(1, 8):
        recipes_for_day = recipes_plans.filter(day_name__order=i)
        if len(recipes_for_day) > 0:
            meals_for_day.append((recipes_for_day[0].day_name, recipes_for_day))
    context = {
        'plan': plan,
        'meals_for_day': meals_for_day
    }
    return render(request, 'app-details-schedules.html', context)



def plan_add(request):
    if request.method == 'GET':
        return render(request, 'app-add-schedules.html')
    else:
        name = request.POST.get('plan_name')
        description = request.POST.get('plan_description')
        if name == "" or description == "":
            context = {
                'wrong_input': 'Wypełnij poprawnie wszystkie pola.',
                'plan_name': name,
                'plan_description': description,
            }
            return render(request, 'app-add-schedules.html', context)

        plan = Plan.objects.create(name=name, description=description)
        return redirect(f'/plan/{plan.id}')


def add_recipe_to_plan(request):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia
