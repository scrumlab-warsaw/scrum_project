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

