from django.shortcuts import render, HttpResponse, redirect
from apps.quote.models import *
import bcrypt
import re


# Create your views here.
def index(request):
    return render(request, 'index.html')

def regester(request, method='POST'):
#regeister User
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    psw = request.POST["psw"]
    psw2 = request.POST["psw-repeat"]
    # Validations
    if len(first_name) < 2 or len(last_name) <2:
        context = {'message':"First or last name must be more than 2 charictors "}
        return render(request, 'index.html', context)

    if not re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        context = {'message':"Please enter a valid email adress!"}
        return render(request, 'index.html', context)

    if psw != psw2:
        context = {'message':"Please make sure passwords match"}
        return render(request, 'index.html', context)

    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(psw.encode('utf8'), salt)
    hashed_pwd = hashed_pwd.decode('utf8')
    new_user = User.objects.create(
                                    first_name = first_name,
                                    last_name = last_name,
                                    email = email,
                                    hashed_pwd = hashed_pwd,
                                    )
    print("User {}{} has been created".format(first_name, last_name))
    return redirect('/')


def login(request, method='POST'):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        print(logged_user.first_name)
        if bcrypt.checkpw(request.POST['l_psw'].encode(), logged_user.hashed_pwd.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/wall')

    context = {'message':"Loggin and/or Password do not match any user"}
    return render(request, 'index.html', context)

def logout(request, method='POST'):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return redirect('/')

def wall(request):
    if 'userid' in request.session.keys():
        context = {
                    'user':User.objects.get(id=request.session['userid']),
                    'post_data': Quote.objects.all()
                    }
        return render(request, 'wall.html', context)
        # return render(request, 'wall.html')
    return HttpResponse("Error: you must be signed in to access this content")


def add_quote(request, method='POST'):

    author=request.POST['author']
    if len(author) < 2:
        context = {'message': "Author's name must be at least 3 charictors"}
        return render(request, 'wall.html', context)

    quote=request.POST['add_quote']
    if len(quote) < 5:
        context = {'message': "Quote must be at least 5 charictors"}
        return render(request, 'wall.html', context)

    Quote.objects.create(user=User.objects.get(id=request.session['userid']),
                        author=author,
                        quote=quote
                            )
    return redirect('/wall')

def user_posts(request, id):
    if 'userid' in request.session.keys():

        user= User.objects.get(id=id)
        quotes = Quote.objects.filter(user=id)
        print("*"*50)
        for quote in quotes:
            print(quote.quote)
        context = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'quotes':quotes
                    }
        return render(request, 'u_quotes.html', context)
    return HttpResponse("Error: you must be signed in to access this content")


# Edit account
def edit_to_account(request, id):
    if 'userid' in request.session.keys():

        user= User.objects.get(id=id)
        context = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email':user.email
                    }
        return render(request, 'update.html', context)
    return HttpResponse("Error: you must be signed in to access this content")


def edit_account(request, id, method='POST'):
    update_user = User.objects.get(id=id)

    if len(request.POST['first_name']) < 2 or len(request.POST['last_name']) <2:
        context = {'message':"First or last name must be more than 2 charictors "}
        return render(request, 'update.html', context)

    if not re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", request.POST['email']):
        context = {'message':"Please enter a valid email adress!"}
        return render(request, 'update.html', context)

    if request.POST['first_name'] != update_user.first_name:
        update_user.first_name = request.POST['first_name']
        print("Updated first Name")
    if request.POST['last_name'] != update_user.last_name:
        update_user.last_name = request.POST['last_name']
        print("updated last_name")
    if request.POST['email'] != update_user.email:
        update_user.email = request.POST['email']
        print("updated email")
    update_user.save()
    return redirect('/wall')


def delete(request, id):
    deleter = Quote.objects.get(id=id)
    deleter.delete()
    return redirect('/wall')
