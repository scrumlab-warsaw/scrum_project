from django.contrib import admin

# Register your models here.
from jedzonko.models import Recipe, Plan, RecipePlan, Page

admin.site.register(Recipe)
admin.site.register(Plan)
admin.site.register(RecipePlan)
admin.site.register(Page)
