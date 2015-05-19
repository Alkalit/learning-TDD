from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from lists.models import Item, List
from lists.forms import ItemForm

def home_page(request):
    return render(request, 'lists/home.html', {'form': ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(pk=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty list item\n"

    return render(request, 'lists/list.html', {'list': list_, 'error': error})

def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['text'], list=list_)

    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        return render(request, 'lists/home.html', {'error': "You can't have an empty list item\n"})

    return redirect(list_)
