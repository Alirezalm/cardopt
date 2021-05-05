import json
import os

import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from dipoa.models import ProblemInstance, ProblemInfo, GamsSolverInfo


@csrf_exempt
def home_page(request, name = None):
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

        user = authenticate(request, username = user_name, password = password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 1})
        return JsonResponse({'status': 0})


@csrf_exempt
@login_required
def dashboard(request, name = None):
    if request.method == 'GET':
        if name == 'dash':
            return render(request, 'dipoa/dashboard/dashboard.html')
        elif name == 'history':

            results = {
                'history': [],
                'gams_history': []
            }
            for problem in ProblemInstance.objects.all().order_by('-id')[0:10]:
                results['history'].append(model_to_dict(problem))

            for solution in GamsSolverInfo.objects.all().order_by('-id')[0:10]:
                results['gams_history'].append(model_to_dict(solution))

            return JsonResponse(results)

        elif name == 'clear':
            ProblemInstance.objects.all().delete()
            GamsSolverInfo.objects.all().delete()
            return JsonResponse({'status': 1})
    else:
        if name == 'opt':
            problem_data = json.loads(request.body)
            with open('config.json', 'w') as jsonfile:
                json.dump(problem_data, jsonfile)

            # solution = requests.post('http://150.162.14.7:5000', data = request.body)
            solution = requests.post('http://127.0.0.1:5000', data = request.body)

            solution_dict = json.loads(solution.text)
            user = User.objects.get(username = request.user)
            p = ProblemInstance()
            p.name = problem_data['name']
            p.number_of_features = problem_data['nVars']
            if problem_data['name'] == 'dslr':
                p.number_of_samples = problem_data['nSamples']
            else:
                p.number_of_samples = 0
            p.number_of_constraints = problem_data['nVars']
            p.number_of_nonzeros = problem_data['nZeros']
            p.number_of_cores = problem_data['nNodes']
            p.optimal_obj = solution_dict['obj']
            p.relative_gap = solution_dict['gap']
            p.max_iter = solution_dict['iter']
            p.elapsed_time = solution_dict['elapsed_time']
            p.soc = problem_data['soc']
            p.sfp = problem_data['sfp']
            p.save()
            info = ProblemInfo()
            info.creator = user
            info.problem_info = p
            info.save()

            user_request = json.loads(request.body)
            solvers = user_request['solvers']

            for solver in solvers:
                user_request['selected_solver'] = solver

                gams_solution = requests.post('http://127.0.0.1:5050', data = json.dumps(user_request))

                gams_sol = json.loads(gams_solution.text)

                gams_info = GamsSolverInfo()

                gams_info.instance = p
                gams_info.gap = gams_sol['gap']
                gams_info.solver_name = gams_sol['solver']
                gams_info.time = gams_sol['time']
                gams_info.status = gams_sol['status']
                gams_info.save()

            return JsonResponse(solution_dict)
