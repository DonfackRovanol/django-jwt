from django.shortcuts import render
from datetime import datetime

def index(request):
    return render(request, 'site/index.html', context={"date": datetime.today()})