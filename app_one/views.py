from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from . models import User, Quote
import bcrypt

def index(request):
    return render(request, 'reg_and_login.html')

def register(request):
    print(request.POST)
    #validate the form info from the form
    errorsFromValidator = User.objects.registrationValidator(request.POST)
    print('errorsFromValidator below')
    print(errorsFromValidator)
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect("/")
    else:
        # hash1 = bcrypt.hashpw('test'.encode(), bcrypt.gensalt()).decode()
        hashedPassword = bcrypt.hashpw(request.POST['PW'].encode(), bcrypt.gensalt()).decode()
        # use this to encrypt password
        newUser = User.objects.create(
            First_name= request.POST['Fname'],
            Last_name= request.POST['Lname'],
            Date= request.POST['Date'],
            Email= request.POST['Email'],
            Password= hashedPassword,
            # hashedpassword is the name of our encrypted password, now you have to make it to login with an encrypted password
        )
    #use session to store the ID of the logged in user
        request.session['loggedInId'] = newUser.id
    # use the info from the form to create new users into the database
    
    return redirect("/success")

def success(request):
    if 'loggedInId' not in request.session:
        messages.error(request, 'You must be logged in first')
        return redirect('/')
        # send back to home page with the error message
    context = {
        'loggedInUser': User.objects.get(id=request.session['loggedInId']),
        'quotes': Quote.objects.all()
    }
    return render(request, 'index.html', context)

def login(request):
    print(request.POST)
    errorsFromValidator = User.objects.loginValidator(request.POST)
    print('errorsFromValidator below')
    print(errorsFromValidator)
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect("/")
    else:
        usersWithMatchingEmail = User.objects.filter(Email = request.POST['Email'])
        
        request.session['loggedInId'] = usersWithMatchingEmail[0].id
        # obtainting the users id through email and obtaining their id
    return redirect('/mainpage')

def mainpage(request):
    context = {
        'loggedInUser': User.objects.get(id=request.session['loggedInId']),
    }
    return render(request,'success.html', context)

def logout(request):
    request.session.clear()
    #deleting the cookie in order to log the user out
    return redirect("/")

def add_quote(request):
    print(request.POST)
    errorsFromQuoteValidator = Quote.objects.quoteValidator(request.POST)
    print('errorsFromQuoteValidator below')
    print(errorsFromQuoteValidator)
    if len(errorsFromQuoteValidator)>0:
        for key, value in errorsFromQuoteValidator.items():
            messages.error(request, value)
        return redirect("/success")
    else:
        user = User.objects.get(id = request.session['loggedInId'])
        quote = Quote.objects.create(
            message = request.POST['message'],
            madeBy = request.POST['madeBy'],
            uploaded_by = User.objects.get(id=request.session['loggedInId'])
        )
        user.favorite_quote.add(quote)
    return redirect('/success')

def favorite(request, id):
    print('hello world')
    user = User.objects.get(id=request.session['loggedInId'])
    quote = Quote.objects.get(id = id)
    user.favorite_quote.add(quote)
    return redirect ('/success')

def remove(request, id):
    user = User.objects.get(id=request.session['loggedInId'])
    quote = Quote.objects.get(id = id)
    user.favorite_quote.remove(quote)
    return redirect ('/success')

def delete(request, id):
    print('this quote will be deleted')
    quote = Quote.objects.get(id=id)
    print(quote)
    quote.delete()
    return redirect ('/success')

def show_quote(request, id):
    quote = Quote.objects.get(id=id)
    context = {
        'quote': Quote.objects.filter(id=id)
    }
    return render(request, 'show_one.html', context)

def edit(request, id):
    quote_to_update = Quote.objects.get(id=id)
    errorsFromQuoteValidator = Quote.objects.quoteValidator(request.POST)
    if len(errorsFromQuoteValidator)>0:
        for key, value in errorsFromQuoteValidator.items():
            messages.error(request, value)
        return redirect(f'/quotes/{quote_to_update.id}')
    quote_to_update.madeBy = request.POST['madeBy']
    quote_to_update.message = request.POST['message']
    quote_to_update.save()
    return redirect('/success')
    
def showuser(request, id):
    count = User.objects.get(id=id).quote_uploaded.all().count
    context = {
        'quotes': User.objects.get(id=id).quote_uploaded.all(),
        'count' : count,
        'user' : User.objects.get(id=id)
    }
    return render(request, 'show_user.html', context)