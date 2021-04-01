from django.urls import path

from dipoa.views import home_page

urlpatterns = [
    path('', home_page, name='homepage')
]
