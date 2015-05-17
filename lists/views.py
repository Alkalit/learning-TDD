from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.core.exceptions import ValidationError

from lists.models import Item, List


def home_page(request):
    return render(request, 'lists/home.html')

def view_list(request, list_id):
    list_ = List.objects.get(pk=list_id)
    return render(request, 'lists/list.html', {'list': list_})

def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)

    try:
        item.full_clean()
        return redirect('/lists/%d/' % list_.id)
    except ValidationError:
        return render(request, 'lists/home.html', {'error': "You can't have an empty list item\n"})

def add_item(request, list_id):
    list_ = List.objects.get(pk=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % list_.id)
