from django.http import HttpResponseNotAllowed
from django.shortcuts import render


def home_page(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(['GET', ], status=405)

    return render(request, 'home/home_page.html')
