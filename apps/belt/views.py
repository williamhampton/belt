from django.shortcuts import render,redirect
from models import users, quotes, favorites
import re
import inspect
from django.db.models import Count
email_re = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
import bcrypt
def containnumber(string):
    return bool(re.search(r'\d', string))

users_all = users.objects.all()
quotes_all = quotes.objects.all()
favorites_all = favorites.objects.all()

def index(request):
    return render(request, 'index.html')

def add(request):
    firstname = request.POST.get('first')
    lastname = request.POST.get('last')
    email = request.POST.get('email')
    password = request.POST.get('pass')
    passwordcon = request.POST.get('passcon')
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    error = False
    context = {
        'users': users.objects.all(),
        }
    if len(firstname)<2:
        error= True
        context['enterfirst'] = 'Enter a valid name'
    if containnumber(firstname)==True:
        error = True
        context['enterfirst'] = 'Enter a valid name'
    if len(lastname)<2:
        error = True
        context['enterlast'] = 'Enter a valid name'
    if containnumber(lastname):
        error = True
        context['enterlast'] = 'Enter a valid name'
    if not email_re.match(email):
        error = True
        context['emailcon'] = 'Must be a valid email'
    if len(password)<9:
        error = True
        context['password'] = 'Password must be longer than 8 digits'
    if len(passwordcon)<9:
        error = True
        context['password'] = 'Password must be longer than 8 digits'
    if password != passwordcon:
        context['password'] = 'Passwords must match'
        error = True
    if not error:
        print pw_hash
        context['sucess'] =  'You sucessfully registerd'
        users.objects.create(first_name = request.POST['first'], last_name = request.POST['last'], email = request.POST['email'], password= pw_hash)
        return render(request, 'index.html',context)
    else:
        return render(request, 'index.html',context)


def login(request):
    email_login = request.POST['email_login']
    print users.objects.filter(email = request.POST['email_login']).exists()

    if users.objects.filter(email = request.POST['email_login']).exists() == False:
        context = {
            'fail': 'Enter a valid email'
        }
        return render(request, 'index.html',context)
    else:
        password_login = request.POST['password_login']
        user = users.objects.filter(email = email_login)
        hashed = user[0].password
        if user is not None:
            if bcrypt.hashpw(password_login.encode(), hashed.encode()) == hashed:
                print user[0].first_name
                request.session['first_name'] = user[0].first_name
                request.session['last_name'] = user[0].last_name
                request.session['email'] = user[0].email
                request.session['id'] = user[0].id
                return redirect('/quotes')
            else:
                context = {
                'fail': 'Email and password did not match'
                }
                return render(request, 'index.html', context)

def userquotes(request):
    context = {
        'userid' : request.session['id'],
        'username': request.session['first_name'],
        'quotes': quotes.objects.all(),
        'favorites': favorites.objects.all()
    }
    return render(request, 'quotes.html', context)

def newquote(request):
    data = request.POST.get('quote')
    databy = request.POST.get('quoteby')
    error = False
    userinstance = users_all.filter(id = request.session['id'])
    context = {
        'userid' : request.session['id'],
        'username': request.session['first_name'],
        'quotes': quotes.objects.all(),
        'favorites': favorites.objects.all()
    }
    if len(data)<10:
        error = True
        context['failquote'] = 'Enter a valid Quote please'
    if len(databy)< 3:
        error = True
        context['failquoteby'] = 'Enter a valid Author of the Quote'
    if error:
        return render(request, 'quotes.html', context)
    else:
        quotes.objects.create(quote = data,quoteby =databy, user = userinstance[0])
        context['success'] = 'Successfully added your quote'
        return render(request, 'quotes.html', context)

def fav(request):
    userinstance = users_all.filter(id = request.session['id'])
    data = request.POST.get('quotefav')
    databy = request.POST.get('quotebyfav')
    context = {
        'userid' : request.session['id'],
        'username': request.session['first_name'],
        'quotes': quotes.objects.all(),
        'favorites': favorites.objects.all()
    }
    favorites.objects.create(quote = data,quoteby =databy, user = userinstance[0])
    quotes_all.filter(quote = data).delete()
    return render (request, 'quotes.html', context)

def removefav(request):
    userinstance = users_all.filter(id = request.session['id'])
    data = request.POST.get('quotefavrem')
    databy = request.POST.get('quotebyfavrem')
    context = {
        'userid' : request.session['id'],
        'username': request.session['first_name'],
        'quotes': quotes.objects.all(),
        'favorites': favorites.objects.all()
    }
    quotes.objects.create(quote = data,quoteby =databy, user = userinstance[0])
    favorites_all.filter(quote = data).delete()
    return render (request, 'quotes.html', context)

def showuser(request, id):
    users_user = users_all.filter(id = id)
    quotesby = quotes_all.filter(user = id)
    number = quotes_all.filter(user= id).annotate(count = Count("id"))
    context = {
        'users': users_user,
        'quotes': quotesby,
        'number': number.count

    }

    return render(request, 'showuser.html',context)
