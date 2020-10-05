from datetime import datetime
from random import shuffle
from math import ceil, sqrt

from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import View
from django.db import IntegrityError

from jedzonko.models import Recipe, Plan, DayName, RecipePlan, Page


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


class RecipeDetails(View):
    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        return render(request, 'app-recipe-details.html', {'recipe': recipe})

    def post(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        like = request.POST.get('like')
        dislike = request.POST.get('dislike')
        if like:
            recipe.votes += 1
        elif dislike:
            recipe.votes -= 1

        recipe.save()
        return render(request, 'app-recipe-details.html', {'recipe': recipe})


def recipe_list(request):
    RECIPES_PER_PAGE = 50

    searched = request.GET.get('recipe_name')
    if searched:
        recipes = Recipe.objects.filter(name__icontains=searched).order_by('-votes', 'created')
        if recipes.count() == 0:
            context = {'error_message': 'Nie znaleziono żadnego przepisu.'}
            return render(request, 'app-recipes.html', context)
        elif recipes.count() == 1:
            return redirect(f'/recipe/{recipes[0].id}')
    else:
        recipes = Recipe.objects.all().order_by('-votes', 'created')
    paginator = Paginator(recipes, RECIPES_PER_PAGE)
    page_number = int(request.GET.get('page', 1))
    page_obj = paginator.get_page(page_number)
    page_numbers = [i for i in range(page_number - 2, page_number + 3) if
                    0 < i <= ceil(len(recipes) / RECIPES_PER_PAGE)]
    recipes_to_show = enumerate(page_obj.object_list, page_obj.start_index())
    return render(request, 'app-recipes.html', {'page_obj': page_obj,
                                                'page_numbers': page_numbers,
                                                'recipes_to_show': recipes_to_show})


def plan_list(request):
    PLANS_PER_PAGE = 50
    plans = Plan.objects.all().order_by('name')
    paginator = Paginator(plans, PLANS_PER_PAGE)
    page_number = int(request.GET.get('page', 1))
    page_obj = paginator.get_page(page_number)
    page_numbers = [i for i in range(page_number - 2, page_number + 3) if 0 < i <= ceil(len(plans) / PLANS_PER_PAGE)]
    plans_to_show = enumerate(page_obj.object_list, page_obj.start_index())
    return render(request, 'app-schedules.html', {'page_obj': page_obj,
                                                  'page_numbers': page_numbers,
                                                  'plans_to_show': plans_to_show})


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
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        raise Http404('Recipe does not exist!')

    if request.method == 'GET':
        context = {'recipe': recipe}
        return render(request, 'app-edit-recipe.html', context)

    else:
        loaded_name = request.POST.get('name')
        loaded_description = request.POST.get('description')
        loaded_prep_time = request.POST.get('preparation_time')
        loaded_prep_desc = request.POST.get('preparation_description')
        loaded_ingredients = request.POST.get('ingredients')

        error_recipe = {
            'name': loaded_name,
            'description': loaded_description,
            'preparation_time': loaded_prep_time,
            'preparation_description': loaded_prep_desc,
            'ingredients': loaded_ingredients
        }

        if (loaded_name == "" or loaded_description == "" or loaded_prep_time == "" or
                loaded_prep_desc == "" or loaded_ingredients == ""):
            context = {'recipe': error_recipe,
                       'error_message': "Wypełnij poprawnie wszystkie pola."}
            return render(request, 'app-edit-recipe.html', context)

        if (Recipe.is_in_database(loaded_name, loaded_ingredients, loaded_description,
                                  loaded_prep_desc, loaded_prep_time)):
            context = {'recipe': error_recipe,
                       'error_message': "Ten przepis już istnieje!"}
            return render(request, 'app-edit-recipe.html', context)

        Recipe.objects.create(name=loaded_name, ingredients=loaded_ingredients, description=loaded_description,
                              preparation_description=loaded_prep_desc, preparation_time=loaded_prep_time)
        return redirect('recipe_list')


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

        if AddMealToPlan.check_if_recipeplan(loaded_plan, meal_name, loaded_day, order):
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
    def check_if_recipeplan(plan, meal, day, order):
        """
        Check if RecipePlan object already exists in database.
        :param plan: object from class Plan
        :param meal: attribute from RecipePlan object
        :param day: object from class DayName
        :param order: attribute from RecipePlan object
        :return: boolean: True - exists, False - doesn't exist.
        """
        validate_1 = RecipePlan.objects.filter(plan=plan, meal_name=meal, day_name=day).count()
        validate_2 = RecipePlan.objects.filter(plan=plan, order=order, day_name=day).count()
        return (validate_1 + validate_2) != 0


def page(request, slug):
    if Page.objects.filter(slug=slug).count() > 0:
        page = Page.objects.get(slug=slug)
        return render(request, 'page.html', {'page': page})
    else:
        return redirect(f'/#{slug}')


class ModifyPlanRecipes(View):
    def get(self, request, plan_id):
        plan = Plan.objects.get(pk=plan_id)
        recipes = Recipe.objects.all()
        days = ModifyPlanRecipes.separate_recipe_plans(plan.recipeplan_set.all().order_by('-day_name__order'))
        context = {
            'days': days,
            'plan': plan,
            'recipes': recipes,
        }
        return render(request, 'modify_plan_recipes.html', context)

    def post(self, request, plan_id):
        plan = Plan.objects.get(pk=plan_id)
        meal_names = request.POST.getlist('meal_name')
        orders = request.POST.getlist('order')
        recipe_ids = request.POST.getlist('recipe_id')
        day_orders = request.POST.getlist('day_order')
        plan_recipes = plan.recipeplan_set.all().order_by('day_name__order', 'order')
        recipes = Recipe.objects.all()

        if not ModifyPlanRecipes.data_is_unique(meal_names, orders, day_orders):
            plan_recipes = ModifyPlanRecipes.convert_to_dummy_recipe_plans(plan_recipes, meal_names, orders, recipe_ids)
            error = 'Sprawdź nazwy posiłków i ich kolejność<br>Nie mogą się powtarzać w danym dniu'
            days = []
            for i in range(1, 8):
                recipes_for_day = [recipe_plan for recipe_plan in plan_recipes if recipe_plan.day_name.order == i]
                if recipes_for_day:
                    days.append((recipes_for_day[0].day_name, recipes_for_day))
            context = {
                'days': days,
                'plan': plan,
                'recipes': recipes,
                'error': error,
            }

            return render(request, 'modify_plan_recipes.html', context)

        ModifyPlanRecipes.save_recipe_plans_data(plan_recipes, meal_names, orders, recipe_ids)
        return redirect('plan_details', plan_id)

    @staticmethod
    def separate_recipe_plans(plan_recipes):
        days = []
        for i in range(1, 8):
            recipes_for_day = plan_recipes.filter(day_name__order=i).order_by('order')
            if len(recipes_for_day) > 0:
                days.append((recipes_for_day[0].day_name, recipes_for_day))
        return days

    @staticmethod
    def data_is_unique(meal_names, orders, day_orders):
        form_length = len(meal_names)
        unique_meal_names_for_day = len(set(zip(meal_names, day_orders)))
        unique_orders_for_day = len(set(zip(orders, day_orders)))
        return form_length == unique_meal_names_for_day and form_length == unique_orders_for_day

    @staticmethod
    def convert_to_dummy_recipe_plans(plan_recipes, meal_names, orders, recipe_ids):
        dummy_plan_recipes = []
        for recipe_plan, meal_name, order, recipe_id in zip(plan_recipes, meal_names, orders, recipe_ids):
            dummy_plan_recipes.append(ModifyPlanRecipes.DummyRecipePlan(meal_name, order, recipe_id, recipe_plan))
        return dummy_plan_recipes

    @staticmethod
    def save_recipe_plans_data(plan_recipes, meal_names, orders, recipe_ids):
        orders = [int(i) for i in orders]

        for i in range(len(plan_recipes)):
            plan_recipes[i].meal_name = sqrt(i)
            plan_recipes[i].order = max(orders) + i + 1
            plan_recipes[i].save()

        for recipe_plan, meal_name, order, recipe_id in zip(plan_recipes, meal_names, orders, recipe_ids):
            recipe_plan.meal_name = meal_name
            recipe_plan.order = order
            recipe_plan.recipe = Recipe.objects.get(pk=recipe_id)
            recipe_plan.save()

    class DummyRecipePlan:
        def __init__(self, meal_name, order, recipe_id, recipe_plan):
            self.meal_name = meal_name
            self.order = order
            self.day_name = recipe_plan.day_name
            self.recipe = Recipe.objects.get(pk=recipe_id)


def delete_recipeplan(request, recipeplan_id):
    meal = RecipePlan.objects.get(id=recipeplan_id)
    plan = Plan.objects.get(id=meal.plan_id)
    meal.delete()
    return redirect(f'/plan/{plan.id}')
