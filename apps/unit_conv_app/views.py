from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from apps.unit_conv_app.models import *
from django.core.mail import send_mail
from django.conf import settings

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
    feedback_categories={
        "layout":"layout",
        "feature":"feature",
        "speed":"speed",
        "conversion":"conversion",
        "other":"other"
    }

    return render(request, 'unit_conv_app/feedback.html', feedback_categories)

def feedback_proc(request):
    # check if we have received request POST
    if request.method == 'POST':
        print("*_*"*12, request.POST, "THIS IS REQUEST. POST", "*_*"*12)
        errors = Feedback.objects.feedback_validator(request.POST)
        if len(errors):
            messages.error(request, "Please rate our site.")
            request.session['layout_text']=request.POST['layout_text']
            request.session['feature_text']=request.POST['feature_text']
            request.session['speed_text']=request.POST['speed_text']
            request.session['conversion_text']=request.POST['conversion_text']
            request.session['other_text']=request.POST['other_text']
            return redirect('/feedback')
        else:
            request.session.clear()
            layout = feature = speed = conversion = other = ''
            if 'layout' in request.POST:
                layout = request.POST['layout']
            if 'feature' in request.POST:
                feature = request.POST['feature']
            if 'speed' in request.POST:
                speed = request.POST['speed']
            if 'conversion' in request.POST:
                conversion = request.POST['conversion']
            if 'other' in request.POST:
                other = request.POST['other']
                
            layout_text = feature_text = speed_text = conversion_text = other_text = ''
            if 'layout_text' in request.POST:
                layout_text = request.POST['layout_text']
            if 'feature_text' in request.POST:
                feature_text = request.POST['feature_text']
            if 'speed_text' in request.POST:
                speed_text = request.POST['speed_text']
            if 'conversion_text' in request.POST:
                conversion_text = request.POST['conversion_text']
            if 'other_text' in request.POST:
                other_text = request.POST['other_text']
            Feedback.objects.create(rating=request.POST['rating'],
             layout=layout,
             feature=feature,
             speed=speed,
             conversion=conversion,
             other=other,
             feedback_email=request.POST['feedback_email'], layout_response=layout_text,  feature_response=feature_text,  conversion_response=conversion_text, other_response=other_text)
            messages.success(request, "Thank you for your feedback!")
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
            Subscriber.objects.create(sub_email = request.POST['subscriber_email'])
            messages.success(request, "Successfully subscribed! Thank you!")
            subject = "Thank you for subscribing!"
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, "You've successfully subscribed! Thank you!", email_from, [request.POST['subscriber_email']], fail_silently=False)
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

def display_image(request):
    print("*_"*12,'WE CAME TO  VIEWS.display_image',"-*"*12)
    return render(request, '/unit_conv_app/display_image.html')