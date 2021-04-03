import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def home_page(request, name=None):
    if request.method == 'GET':
        if name == 'islogin':
            if request.user.is_active & request.user.is_authenticated:

                return JsonResponse({'status': 1})
            else:
                return JsonResponse({'status': 0})
        elif name == 'logout':
            logout(request)
            return JsonResponse({'status': 1})
        return render(request, 'dipoa/main.html')
    elif (request.method == 'POST') & (name == 'login'):

        user_info = json.loads(request.body)

        user_name = user_info['email']

        password = user_info['password']

        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 1})
        return JsonResponse({'status': 0})


@csrf_exempt
@login_required
def dashboard(request):
    if request.method == 'GET':
        return render(request, 'dipoa/dashboard/dashboard.html')
    else:
        problem_data = json.loads(request.body)

        print(problem_data)
        return JsonResponse({'status': 1})
