from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from apps.unit_conv_app.models import *
import bcrypt

# Create your views here.
def index(request):
    if 'id' in request.session:
        loginOut={
            "logout_link":"logout",
            "logout_text":"Logout"
        }
    else:
        loginOut={
            "logout_link":"loginReg",
            "logout_text":"Login/Signin"
        }
    return render(request, 'unit_conv_app/index.html', loginOut)

def index_volume(request):
    return render(request, 'unit_conv_app/index_volume.html')

def feedback(request):
    return render(request, 'unit_conv_app/feedback.html')

def feedback_proc(request):
    # check if we have received request POST
    if request.method == 'POST':
        #validate email
        return redirect('/feedback')
    return redirect('/feedback')

def subscribe(request):
    return render(request, 'unit_conv_app/subscribe.html')

def subscribe_proc(request):
    # check if we have received request POST
    if request.method == 'POST':
        #validate email
        errors = Subscriber.objects.subscribe_validator(request.POST)
        # if there are errors, create flash error message
        if len(errors):
            print('ERROR VALIDATION', errors)
            for key, value in errors.items():
                messages.error(request, value)
                print("SUB ERROR FOR-LOOP - KEY", key, "SUB ERROR FOR-LOOP - VALUE", value)
                return redirect('/subscribe')
        # data are valid, enter data
        else:
            sEmail = Subscriber.objects.create(sub_email = request.POST['subscriber_email'])
            messages.success(request, "Successfully subscribed! Thank you!")
            return redirect('/subscribe')

    return redirect('/subscribe')

def loginReg(request):
    return render(request, 'unit_conv_app/loginReg.html')

# receives form POST for User registration
def reg_process(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, "registration")
        return redirect('/loginReg')
    else:
        hashIt = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'],password=hashIt)
        request.session['name'] = request.POST['first_name']
        request.session['id'] = User.objects.last().id
        print('*-'*15, 'REQUEST SESSION: ', request.session)
        messages.success(request, "Successfully registered!")
    return redirect('/dashboard')

def login_process(request):
    email_input = request.POST['email']
    user = User.objects.filter(email=email_input)
    try:
        if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
            messages.success(request, "Successfully logged in!")
            request.session['id'] = user[0].id
            return redirect('/dashboard')
        else:
            messages.error(request, "Invalid Login", "login")
            return redirect('/loginReg')
    except:
        messages.error(request, "Invalid Login", "login")
        return redirect('/loginReg')

def logout(request):
    request.session.clear()
    return redirect('/')