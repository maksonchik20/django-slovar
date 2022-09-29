from django.shortcuts import render

def main_slovar(request):
    return render(request, 'slovar/main_slovar.html')