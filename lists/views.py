from django.shortcuts import render, redirect
from django.http.response import HttpResponse

from lists.models import Item


def home_page(request):

    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    return render(request, 'lists/home.html')
