from datetime import datetime
from random import shuffle
from math import ceil

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from jedzonko.models import Recipe, Plan, DayName, RecipePlan


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

    if request.method == 'POST':
        like = request.POST.get('like')
        dislike = request.POST.get('dislike')

        if like:
            recipe.votes += 1
        elif dislike:
            recipe.votes -= 1

        recipe.save()

    context = {'recipe': recipe}
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
    return HttpResponse("udało się")  # tymczasowo, do późniejszego uzupełnienia


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


class AddMealToPlan(View):
    PLANS = Plan.objects.all()
    RECIPES = Recipe.objects.all()
    DAYS = DayName.objects.all()

    def get(self, request):
        context = {'plans': AddMealToPlan.PLANS,
                   'recipes': AddMealToPlan.RECIPES,
                   'days': AddMealToPlan.DAYS}
        return render(request, 'app-schedules-meal-recipe.html', context)

    def post(self, request):
        plan = request.POST.get('plan')
        meal_name = request.POST.get('meal_name')
        order = request.POST.get('order')
        recipe = request.POST.get('recipe')
        day = request.POST.get('day')

        loaded_plan = Plan.objects.get(name=plan)
        loaded_recipe = Recipe.objects.get(name=recipe)
        loaded_day = DayName.objects.get(day_name=day)

        if meal_name == "" or order == "":
            context = {'plans': AddMealToPlan.PLANS,
                       'loaded_plan': loaded_plan,
                       'recipes': AddMealToPlan.RECIPES,
                       'loaded_recipe': loaded_recipe,
                       'days': AddMealToPlan.DAYS,
                       'loaded_day': loaded_day,
                       'error_message': 'Wypełnij poprawnie wszystkie pola.',
                       'meal_name': meal_name,
                       'order': order
                       }
            return render(request, 'app-schedules-meal-recipe.html', context)

        if AddMealToPlan.saving_failure(loaded_plan, meal_name, loaded_day, order):
            context = {'plans': AddMealToPlan.PLANS,
                       'loaded_plan': loaded_plan,
                       'recipes': AddMealToPlan.RECIPES,
                       'loaded_recipe': loaded_recipe,
                       'days': AddMealToPlan.DAYS,
                       'loaded_day': loaded_day,
                       'error_message': 'Ten posiłek już istnieje.',
                       'meal_name': meal_name,
                       'order': order
                       }
            return render(request, 'app-schedules-meal-recipe.html', context)

        RecipePlan.objects.create(meal_name=meal_name, order=order, day_name=loaded_day,
                                  recipe=loaded_recipe, plan=loaded_plan)
        return redirect(f'/plan/{loaded_plan.id}')

    @staticmethod
    def saving_failure(plan, meal, day, order):
        validate_1 = RecipePlan.objects.filter(plan=plan, meal_name=meal, day_name=day).count()
        validate_2 = RecipePlan.objects.filter(plan=plan, order=order, day_name=day).count()
        return validate_1 + validate_2
