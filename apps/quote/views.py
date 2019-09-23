from django.shortcuts import render, HttpResponse, redirect
from apps.quote.models import *
import bcrypt


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
    if psw != psw2:
        return HttpResponse("Passwords do Not match")
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
    return HttpResponse("Loggin and/or Password do not match any user")


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
    Quote.objects.create(user=User.objects.get(id=request.session['userid']),
                        author=request.POST['author'],
                        quote=request.POST['add_quote']
                            )
    return redirect('/wall')
