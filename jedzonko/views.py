from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class Dashobard(View):

    def get(self, request):
        return render(request, 'dashboard.html')


def main_page(request):
    return render(request, "index.html")


def recipe_details(request, recipe_id):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia


def recipe_list(request):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia


def plan_list(request):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia


def recipe_add(request):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia


def recipe_modify(request, recipe_id):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia


def plan_details(request, plan_id):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia


def plan_add(request):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia


def add_recipe_to_plan(request):
    return HttpResponse("")  # tymczasowo, do późniejszego uzupełnienia
