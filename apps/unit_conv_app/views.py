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

    return render(request, 'unit_conv_app/feedback.html', loginOut)

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
        # This is so we don't have to repeatedly type request.POST
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
        # This is so we don't have to repeatedly type request.POST 
        layout_text = feature_text = speed_text = conversion_text = other_text = ''

        layout_text = request.POST.get('layout_text', None)
        feature_text = request.POST.get('feature_text', None)
        speed_text = request.POST.get('speed_text', None)
        conversion_text = request.POST.get('conversion_text', None)
        other_text = request.POST.get('other_text', None)

        layout = request.POST.get('layout', None)
        feature = request.POST.get('feature', None)
        speed = request.POST.get('speed', None)
        conversion = request.POST.get('conversion', None)
        other = request.POST.get('other', None)


        # Enter the POST data to our database 
        submitted_feedback = Feedback.objects.create(rating=request.POST['rating'], feedback_email=request.POST['feedback_email'])

        if layout_text:
            Response.objects.create(response_text=layout_text, response_category="layout", respond_feedback=submitted_feedback )
        if feature_text:
            Response.objects.create(response_text=feature_text, response_category="feature", respond_feedback=submitted_feedback )
        if speed_text:
            Response.objects.create(response_text=speed_text, response_category="speed", respond_feedback=submitted_feedback )
        if conversion_text:
            Response.objects.create(response_text=conversion_text, response_category="conversion", respond_feedback=submitted_feedback )
        if other_text:
            Response.objects.create(response_text=other_text, response_category="other", respond_feedback=submitted_feedback )

        messages.success(request, "Thank you for your feedback!")
    return redirect('/feedback')

def subscribe(request):
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
    return render(request, 'unit_conv_app/subscribe.html', loginOut)

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

# Display images when user click keypad, we passed the "numkey" variable
def display_image(request, numkey):
    #notice we passed the "numky" via url, "numkey" is the clicked keypad's value
    print("*_"*12,'WE CAME TO  VIEWS.display_image, this is sum: ', sum,"-*"*12)
    # Display images base on the changes in the keypad
    # Create a dictionary to keep STORE all the picture's urls and ASSOCIATE each picture with a number range in [0-9, back, clear] (an unique "numkey" value)
    display_dict={
        "1": "static/unit_conv_app/images/imagefiles_kanji_ichi_one.png",
        "2": "static/unit_conv_app/images/imagefiles_kanji_ni_two.png",
        "3": "static/unit_conv_app/images/imagefiles_kanji_san_three.png",
        "4": "static/unit_conv_app/images/imagefiles_kanji_yon_four.png",
        "5": "static/unit_conv_app/images/imagefiles_kanji_go_five.png",
        "6": "static/unit_conv_app/images/imagefiles_kanji_roku_six.png",
        "7": "static/unit_conv_app/images/imagefiles_kanji_shichi_seven.png",
        "8": "static/unit_conv_app/images/imagefiles_kanji_hachi_eight.png",
        "9": "static/unit_conv_app/images/imagefiles_kanji_kyu_nine.png",
        "0": "static/unit_conv_app/images/imagefiles_kanji_rei_zero.png",
        "back": "https://i.pinimg.com/originals/36/19/23/361923e239621f89c2e7b3894be7e749.jpg",
        "clear": "https://i.pinimg.com/originals/36/19/23/361923e239621f89c2e7b3894be7e749.jpg",
        "clicked_numkey": numkey
    }
    # Select the display picture url based on the numkey
    print("Select the display picture base on the numkey. Numkey: ", numkey, "display_dict[numkey]: ", display_dict[numkey])
    # Ajax 
    return render(request, 'unit_conv_app/ajax_images.html', {"display_url":display_dict[numkey]})