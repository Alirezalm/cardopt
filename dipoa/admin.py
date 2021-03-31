from django.contrib import admin

# Register your models here.
from dipoa.models import ProblemInstance, ProblemInfo

admin.site.register(ProblemInstance)
admin.site.register(ProblemInfo)
