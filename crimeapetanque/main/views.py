from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    data = {'title' : 'Главная страница'}
    return render(request, 'main/index.html', data)


def about(request):
    data = {'title' : 'О Нас'}
    return render(request, 'main/about.html',data)


def show_category(request, cat_id):
    return index(request)


cats_db = [
    {'id': 1, 'name': 'ТЕТЫ'},
    {'id': 2, 'name': 'ДУПЛЕТЫ'},
    {'id': 3, 'name': 'ТРИПЛЕТЫ'},
]
