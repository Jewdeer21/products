from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt, re
from .models import *


def index(request):
    return render(request, 'myapp/index.html')

def register(request):
    errors = User.objects.reg_validator(request)

    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hashed)
        request.session['user_id'] = user.id
        print(user)
        return redirect('/dashboard')

def login(request):
    errors = User.objects.login_validator(request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please Login/Register")
        return redirect('/')
    else: 
        user = User.objects.get(id=request.session['user_id'])
        items = Item.objects.all()
        myItems = user.adds.all()
        notJoined = items.difference(myItems)
                
        context = {
            'user' : user,
            'items' : items,
            'myItems' : myItems,
            'notJoined' : notJoined,
        }

        return render(request, 'myapp/dashboard.html', context)

def show(request, item_id):
    item = Item.objects.get(id=item_id)
    joined = item.adds.all()
    context = {
        'item': item,
        'joined': joined
    }
    return render(request, 'myapp/dashboard.html', context)

def add(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user
        }
        return render(request, 'myapp/create.html', context)

def create(request):
    errors = Item.objects.item_validator(request)

    if len(errors) < 1:
        return redirect('/dashboard')
    else:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/items/add')

def join(request, item_id):
    user = User.objects.get(id=request.session['user_id'])
    item = Item.objects.get(id=item_id)
    user.adds.add(item)
    return redirect('/dashboard')

def leave(request, item_id):
    user = User.objects.get(id=request.session['user_id'])
    item = Item.objects.get(id=item_id)
    user.adds.remove(item)
    return redirect('/dashboard')


