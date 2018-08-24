from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from apps.unit_conv_app.models import *
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

#User arrives to dashboard after registration/logged in
def dashboard(request):
    if 'id' not in request.session:
        messages.error(request,"Need to login/signup to access dashboard", "dash")
        return redirect('/loginReg')
    else:
    # try:
    #     # user to Super dasbhboard if user_level == 9, otherwise normal dashboard
    #     if User.objects.get(id=request.session['id'], user_level=9):
    #         return render(request, 'dashboard_app/dashboard_super.html')
    # except:
        return render(request, 'dashboard_app/dashboard.html')

def conversion_upload(request):
    return render(request, 'dashboard_app/conversion_upload.html')

def account_info(request):
    user = User.objects.get(id=request.session['id'])
    return render(request, 'dashboard_app/account_info.html', {'user':user})

def change_password(request):
    if 'id' in request.session:
        user_info={
            "first_name":User.objects.get(id=request.session['id']).first_name,
            "last_name":User.objects.get(id=request.session['id']).last_name
        }
        return render(request,'dashboard_app/change_password.html', user_info)
    else:
        messages.error(request,"Need to login/signup for changing password", "dash")
        return redirect('/loginReg')

def change_password_proc(request):
    if not request.method == POST:
        return redirect('change_password')
    errors = User.objects.change_password_validator(request.POST)
    user = User.objects.get(id=request.session['id'])
    # validating password form
    if len(errors):
        for key, value in errors.items():
            messages.error(request, key, "password")
            return redirect('change_password')
    # check current password matches
    elif not bcrypt.checkpw(request.POST['current_password'].encode(), user[0].password.encode()):
        messages.error(request, "wrong password", "password")
        return redirect('change_password')
    # edit password in the database
    user.password = request.POST['new_password']
    user.save()
    messages.success(request, "password changed", "password")
    return redirect('change_password')

def delete_upload(request, upload_id):
    #delete upload_file with id == upload_id
    #d = Upload.objects.get(id=upload_id)
    #d.delete()
    return redirect('conversion_upload')

def feedback(request):
    if 'id' not in request.session:
        messages.error(request,"Need to login/signup", "dash")
        return redirect('/loginReg')
    feedbacks = Feedback.objects.all().order_by('-id')
    return render(request,'dashboard_app/feedbacks.html', {"feedbacks":feedbacks})

@csrf_exempt
def feedbacks_ajax(request):

    print("*_"*20,"POST data: ", request.POST)
    if request.POST['Layout'] == "Layout":
        feedback_list={
            'flayout' : Feedback.objects.filter(layout='layout')
        }
    elif request.POST['Features'] == "Features":
        feedback_list={
            'ffeature' : Feedback.objects.filter(feature='feature')
        }
    elif requeste.POST['Speed'] == "Speed":
        feedback_list={
            'fspeed' : Feedback.objects.filter(speed='speed')
        }
    elif request.POST['Conversion'] == 'Conversion':
        feedback_list={
                'fconversion' : Feedback.objects.filter(conversion='conversion')
        }
    elif request.POST['Other'] == 'Other':
        feedback_list={
            'fother' : Feedback.objects.filter(other='other')
        }
    print('request.POST', request.POST)
    return render(request, 'dashboard_app/feedbacks_ajax.html', feedback_list)

def delete_feedback(request, feedbackid):
    dfeed = Feedback.objects.get(id=feedbackid)
    dfeed.delete()
    return redirect('/dashboard/feedback')

def wall(request):
    if "id" not in request.session:
        return redirect('wall')
    else: 
        post_info = {
            'posts':Post.objects.all().order_by('-id'),
            'comments': Comment.objects.all().order_by('-id')
        }
        return render(request,'dashboard_app/wall.html', post_info)

#processing the user leaving post on the wall
def post_proc(request):
    content= request.POST["content"]
    errors = Post.objects.post_validator(request.POST)
    if len(errors):
        messages.error(request, "Post can not be empty")
        return redirect("/dashboard/wall")
    else:
        this_poster= User.objects.get(id=request.session['id'])
        Post.objects.create(post_text=content, poster=this_poster)
        return redirect("/dashboard/wall")

def delete_post(request, post_id):
    #make sure no one can randomly delete post
    if 'id' in request.session:
        p = Post.objects.get(id=post_id)
        p.delete()
        return redirect("/dashboard/wall")
    else:
        return redirect("/loginReg")

def subscription(request):
    subscriber_list ={
        'subscriptions':Subscriber.objects.all().order_by('-id')
        }
    return render(request, 'dashboard_app/subscriptions.html', subscriber_list)

# def unsubscribe(request, subscription_id):
#     sub = Subscriber.objects.get(id=subscription_id)
#     sub.delete()
#     return redirect('/dashboard/subscription')

def subscribers_search(request):
    subscriber_list ={
        'subscriptions':Subscriber.objects.filter(sub_email__startswith=request.POST['startswith']).order_by('-id')
        }
    return render(request, 'dashboard_app/ajax_subscriptions.html', subscriber_list)

def unsubscribe(request, sub_id):
    sub = Subscriber.objects.get(id=sub_id)
    sub.delete()
    subscriber_list ={
        'subscriptions': list(Subscriber.objects.all().values().order_by('-id'))
        }
    return JsonResponse(subscriber_list)

def unsubscribe_ajax(request, sub_id):
    print('REACHED Unsubscribe_ajax views')
    sub = Subscriber.objects.get(id=sub_id)
    sub.delete()
    subscriber_list ={
        'subscriptions': Subscriber.objects.all().values().order_by('-id')
        }
    return render(request, 'dashboard_app/ajax_subscriptions.html', subscriber_list)

def add_user(request):
    return HttpResponse('add user functionality page here')

def account_edit(request):
    if request.method == 'POST':
        dedit = User.objects.get(id=request.session['id'])
        dedit.desc = request.POST['desc']
        dedit.save()
    return redirect('/dashboard/account_info')

def demo(request):
    return render(request, 'dashboard_app/ajax_demo.html')

def all_json(request):
    feedbacks = Feedback.objects.all()
    feedbacks_json = serializers.serialize("json", feedbacks)
    return HttpResponse(feedbacks_json, content_type='application/json')

def all_html(request):
    subscribers = Subscriber.objects.all()
    return render(request, "dashboard_app/all.html", {"subscribers":subscribers})

def find(request):
    subscribers = Subscriber.objects.filter(sub_email__startswith=request.POST['email_starts_with'])
    print(subscribers)
    return render(request, "dashboard_app/all.html", {"subscribers":subscribers})