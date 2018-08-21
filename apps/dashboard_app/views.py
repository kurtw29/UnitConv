from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from apps.unit_conv_app.models import *

#User arrives to dashboard after registration/logged in
def dashboard(request):
    if 'id' not in request.session:
        messages.error(request,"Need to login/signup for access to dashboard", "dash")
        return redirect('/loginReg')
    try:
        # user to Super dasbhboard if user_level == 9, otherwise normal dashboard
        print(request.session['id'], "IDIDIDIDIDIDIDIDIDID")
        if User.objects.get(id=request.session['id'], user_level=9):
            return render(request, 'dashboard_app/dashboard_super.html')
    except:
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
    # user = User.objects.get(id=request.session['id'])
    # if request.method == POST:
    #     #validate password form
    #     errors = 
    #     if len(errors):
    return redirect('dashboard')



def delete_upload(request, upload_id):
    #delete upload_file with id == upload_id
    #d = Upload.objects.get(id=upload_id)
    #d.delete()
    return redirect('conversion_upload')

def feedback(request):
    return render(request,'dashboard_app/feedbacks.html')

def delete_feedback(request, feedback_id):
    #delete feedback with id == feedback__id
    #d = Feedback.objects.get(id=feedback_id)
    #d.delete()
    return redirect('feedbacks')

def wall(request):
    post_info = {
        'posts':Post.objects.all(),
        'comments': Comment.objects.all()
    }
    return render(request,'dashboard_app/wall.html', post_info)

#processing the user leaving post on the wall
def post_proc(request):
    if "id" not in request.session:
        return redirect('wall')
    else: 
        if request.method == "POST":
            content= request.POST["content"]
        if len(content) == 0:
            messages.error(request, "Post can not be empty", "post")
            return redirect("wall")
        else:
            this_poster= User.objects.get(id=request.session['id'])
            Post.objects.create(post_text=content, poster=this_poster)
            return redirect("wall")

def delete_post(request, post_id):
    #make sure no one can randomly delete post
    if 'id' in request.session:
        p = Post.objects.get(id=post_id)
        p.delete()
        return redirect("wall")
    else:
        return redirect("/loginReg")

def subscription(request):
    return render(request, 'dashboard_app/subscriptions.html')

def unsubscribe(request, subscription_id):
    return redirect(request, 'subscription')

def add_user(request):
    return HttpResponse('add user functionality page here')

def account_edit(request):
    return HttpResponse('user acct edit page')
