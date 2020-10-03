"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from jedzonko.views import (
    IndexView, main_page, Dashobard, recipe_list, plan_list, recipe_add, RecipeDetails,
    recipe_modify, plan_details, plan_add, AddMealToPlan, page, ModifyPlanRecipes, delete_recipeplan
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view()),
    path('main/', Dashobard.as_view()),
    path('', main_page),
    path('recipe/<int:recipe_id>/', RecipeDetails.as_view(), name="recipe_details"),
    path('recipe/list/', recipe_list, name="recipe_list"),
    path('recipe/add/', recipe_add),
    path('recipe/modify/<int:recipe_id>', recipe_modify),
    path('plan/<int:plan_id>/', plan_details , name='plan_details'),
    path('plan/list/', plan_list),
    path('plan/add/', plan_add),
    path('plan/add-recipe/', AddMealToPlan.as_view()),
    path('<slug:slug>/', page),
    path('plan/modify/<int:plan_id>/', ModifyPlanRecipes.as_view(), name='modify_plan_recipes'),
    path('recipeplan/<int:recipeplan_id>/delete/', delete_recipeplan)
]
