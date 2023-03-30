from django.shortcuts import render,redirect
from . models import *
import bcrypt
from django.contrib import messages

def index(request):
    return render(request ,"index.html")

def registration(request):
    errors = User.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        hashed=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=fname,last_name=lname,email=email,password=hashed)
        new_user=User.objects.last()
        request.session['user_id']=new_user.id
    return redirect('/paintings')

def login(request):
    email=request.POST['email']
    password=request.POST['password']
    user=User.objects.filter(email=email).first()
    if user:
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            request.session['user_id']=user.id
            return redirect('/paintings')
    messages.error(request, 'Invalid Credentials')
    return redirect('/')

def paintings(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user=User.objects.get(id=request.session['user_id'])
    context={
        'user':user,
        'all_paintings': Painting.objects.all()
    }
    return render(request,"paintings.html",context)

def new_painting(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request,"new_painting.html")

def painting_details(request,id):
    if 'user_id' not in request.session:
        return redirect('/')
    painting=Painting.objects.get(id=id)
    context={
        'painting':painting
    }
    return render(request,"painting_details.html",context)

def create_painting(request):
    if 'user_id' not in request.session:
        return redirect('/')
    errors = Painting.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/paintings/new')
    user=User.objects.get(id=request.session['user_id'])
    Painting.objects.create(title=request.POST['title'],description=request.POST['description'],price=request.POST['price'],quantity=request.POST['quantity'],painted_by=user)
    return redirect('/paintings')

def edit_painting(request,id):
    if 'user_id' not in request.session:
        return redirect('/')
    painting=Painting.objects.get(id=id)
    context={
        'painting':painting
    }
    return render(request,"edit_painting.html",context)

def edit(request,id):
    if 'user_id' not in request.session:
        return redirect('/')
    errors = Painting.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect(f'/paintings/{id}/edit')
    painting=Painting.objects.get(id=id)
    painting.title=request.POST['title']
    painting.description=request.POST['description']
    painting.price=request.POST['price']
    painting.save()
    return redirect('/paintings')

def delete_painting(request,id):
    if 'user_id' not in request.session:
        return redirect('/')
    painting=Painting.objects.get(id=id)
    painting.delete()
    return redirect('/paintings')

def logout(request):
    del request.session['user_id']
    return redirect('/')

def buy(request,id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    painting = Painting.objects.get(id=id)
    painting.users_who_purchased.add(user)
    painting.quantity -= 1
    painting.save()
    return redirect('/paintings')

# Create your views here.
