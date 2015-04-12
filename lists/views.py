from django.shortcuts import render
from django.http.response import HttpResponse

from lists.models import Item


def home_page(request):
    item = Item()
    item.text = request.POST.get('item_text', '')
    item.save()

    return render(request, 'lists/home.html', {
        'new_item_text': item.text
    })
