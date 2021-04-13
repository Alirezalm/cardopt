from django.urls import path

from dipoa.views import home_page, dashboard

app_name = 'dipoa'
urlpatterns = [
    path('<str:name>', home_page, name='homepage'),
    path('', home_page, name='homepage'),
    path('app/dashboard', dashboard, name = 'dashboard')

]
