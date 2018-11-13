from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from apps.unit_conv_app.models import *
from django.core import serializers
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
from apps.dashboard_app.models import *
from django.db.models import Avg
import datetime
import bcrypt
from django.db.models import Q

#User arrives to dashboard after registration/logged in
def dashboard(request):
    if 'id' not in request.session:
        messages.error(request,"Need to login/signup to access dashboard", "dash")
        return redirect('/loginReg')
    else:
        post_info = {
            'posts':Post.objects.all().order_by('-id'),
            'comments': Comment.objects.all(),
            'users':User.objects.get(id=request.session['id'])
        }
        return render(request, 'dashboard_app/dashboard.html', post_info )

def add_image(request):
    if 'id' not in request.session:
        messages.error(request,"Need to login/signup to access dashboard", "dash")
        return redirect('/loginReg')
    images = Image.objects.all().order_by('-id')
    return render(request, 'dashboard_app/add_image.html', {'images':images})

def add_image_proc(request):
    # Check if we received request POST
    if request.method == "POST":
        # validation messages for the add_image form (cannot enter blank)
        errors = Image.objects.add_image_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/dashboard/add_image')
        # after validation, adding title & URL to database
        else:
            # associate the user in session with adding the image
            logged_user = User.objects.get(id=request.session['id'])
            # adding the image info to database
            adding_image = Image.objects.create(title=request.POST['title'], image_url=request.POST['image_url'], adder=logged_user)
            print("*-"*20, "ADDED IMAGE URL: ", adding_image)
            # provide success message after completion
            messages.success(request, "Successfully added")
            return redirect("/dashboard/add_image")
    return redirect('/dashboard/add_image')

def added_image_search(request):
    if request.method == "POST":
        print("*-"*12, "REQUEST.POST: ", request.POST)

        if request.POST['from_date'] and request.POST['to_date']:
            images = Image.objects.filter(title__contains=request.POST['image_name'], adder__first_name__contains=request.POST['added_by_name'], created_at__date__gt=datetime.datetime.strptime(request.POST['from_date'], "%Y-%m-%d"), created_at__date__lt=datetime.datetime.strptime(request.POST['to_date'], "%Y-%m-%d")).order_by("-id")
        elif request.POST['from_date']:
            images = Image.objects.filter(title__contains=request.POST['image_name'], adder__first_name__contains=request.POST['added_by_name'], created_at__date__gt=datetime.datetime.strptime(request.POST['from_date'], "%Y-%m-%d")).order_by("-id")
        elif request.POST['to_date']:
            images = Image.objects.filter(title__contains=request.POST['image_name'], adder__first_name__contains=request.POST['added_by_name'], created_at__date__lt=datetime.datetime.strptime(['to_date'], "%Y-%m-%d")).order_by("-id")
        else:
            images = Image.objects.filter(title__contains=request.POST['image_name'], adder__first_name__contains=request.POST['added_by_name']).order_by("-id")
            
        return render(request, 'dashboard_app/searched_images.html', {'images':images})
    else:
        return HttpResponse("Error, request.method != POSTS ")

def delete_image(request, num):
    img = Image.objects.get(id=num)
    img.delete()
    return redirect('/dashboard/add_image')

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
    if not request.method == "POST":
        messages.error(request, "invalid form submission")
        return redirect('/dashboard/change_password')
    errors = User.objects.change_password_validator(request.POST)
    user = User.objects.get(id=request.session['id'])
    # validating password form
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/dashboard/change_password')
    # check current password matches
    elif not bcrypt.checkpw(request.POST['current_password'].encode(), user.password.encode()):
        messages.error(request, "wrong password")
        return redirect('/dashboard/change_password')
    # edit password in the database
    hashIt = bcrypt.hashpw(request.POST['new_password'].encode(), bcrypt.gensalt())
    user.password = hashIt
    user.save()
    messages.success(request, "password changed")
    return redirect('/dashboard/change_password')

def feedback(request):
    if 'id' not in request.session:
        messages.error(request,"Need to login/signup", "dash")
        return redirect('/loginReg')
    # Create a data points for # of feedbacks every month
    feedbacks_months = []
    for i in range(0,12):
        feedbacks_months.append(Feedback.objects.filter(created_at__month=i+1).count())
    print("feedbacks_months: ", feedbacks_months)
    # Create a list of rating counts [5, 4, 3, 2, 1]
    feedbacks_rating_count = []
    for r in range(5,0,-1):
        feedbacks_rating_count.append(Feedback.objects.filter(rating=r).count())
    print("List feedbacks_ratings counts [rated_5, rated_4, rated_3, rated_2, rated_1]: ", feedbacks_rating_count )
    # Create dictionary for HTML templating
    feedbacks = {
        # List all feedbacks in descending order
        'feedbacks':Feedback.objects.all().order_by('-id'),
        # Find total number of feedbacks
        'feedbacks_tot': Feedback.objects.count(),
        # Num of feedbacks during August
        'feedbacks_months' : feedbacks_months,
        # Find the average rating
        'rating_avg': Feedback.objects.aggregate(Avg('rating'))['rating__avg'],
        # Count number of received ratings by rates
        'feedbacks_rating_count': feedbacks_rating_count,
        # Count layout_text responses
        'layout_text_tot' : Response.objects.filter(response_category='layout').count(),
        # Count of feature_text responses
        'feature_text_tot' : Response.objects.filter(response_category='feature').count(),
        # Count of speed_text responses
        'speed_text_tot' : Response.objects.filter(response_category='speed').count(),
        # Count of conversion_text responses
        'conversion_text_tot' : Response.objects.filter(response_category='conversion').count(),
        # Count of other_text responses
        'other_text_tot' : Response.objects.filter(response_category='other').count()
    }
    return render(request,'dashboard_app/feedbacks.html', feedbacks)

def feedbacks_ajax(request):
    if request.method != "POST":
        messages.error(request, "Invalid search, method != POST")
        return redirect('/dashboard/feedback')

    # Search feedbacks by id
    print("*-"*12, "RECEIVED POST, here's request.POST: ", request.POST)
    feedbacks = Feedback.objects.all()
    # if user input 'feedback_id' (default = '') then run this function, otherwise skip this if-statement filter.
    if request.POST['feedback_id'] != '':
        feedbacks = feedbacks.filter(id=request.POST['feedback_id'])


    if 'rating_checkbox' in request.POST:
        # print('DID WE PASS THE LEN(RATING) TSETING?')
        rating_checkbox = request.POST['rating_checkbox']
        # print("What is len(rating_checkbox): ", len(rating_checkbox))
        if len(rating_checkbox)==1:
            feedbacks = feedbacks.filter(rating=rating_checkbox)
        if len(rating_checkbox)>1:
            # start the initial case
            feedbacks = feedbacks.filter(rating=rating_checkbox[0])
            # start the loop
            for r_num in range(1, len(rating_checkbox)):
                print("Print the for-loop of post['rating_checkbox']", r_num)
                feedbacks =  feedbacks |feedbacks.filter(rating=r_num)
            # print("AFTER for-looping the rating checkboxes, this is the feedback queries", feedbacks)
    # Bring out only entries that includes "feedback_email"
    if request.POST['feedback_email'] == 'True':
        print("post.feedback_EMAIL = TRUE")
        feedbacks = feedbacks.exclude(feedback_email='')
    # Bring out the entries in associated with selected 'feedback_status':None, Work_in_Progress, Reviewed, Completed
    if request.POST['feedback_status']:
        feedbacks = feedbacks.filter(status = request.POST['feedback_status'])

    # Bring out the entries within selected date range
    if request.POST['from'] and request.POST['to']:
        feedbacks = feedbacks.filter(created_at__date__gt=datetime.datetime.strptime(request.POST['from'], "%m/%d/%Y"), created_at__date__lt=datetime.datetime.strptime(request.POST['to'], "%m/%d/%Y"))
    elif request.POST['from']:
        feedbacks = feedbacks.filter(created_at__date__gt=datetime.datetime.strptime(request.POST['from'], "%m/%d/%Y"))
    elif request.POST['to']:
        feedbacks = feedbacks.filter(created_at__date__lt=datetime.datetime.strptime(request.POST['to'], "%m/%d/%Y"))
        
    # Bring out only the selected/checked 'area of improvment checkboxes'
    if 'rating_layout_checkout' in request.POST:
        feedbacks = feedbacks.filter(feedback_responses__response_category=request.POST['rating_layout_checkout'])
    if 'rating_feature_checkout' in request.POST:
        feedbacks = feedbacks.filter(feedback_responses__response_category=request.POST['rating_feature_checkout'])
    if 'rating_speed_checkout' in request.POST:
        feedbacks = feedbacks.filter(feedback_responses__response_category=request.POST['rating_speed_checkout'])
    if 'rating_conversion_checkout' in request.POST:
        feedbacks = feedbacks.filter(feedback_responses__response_category='rating_conversion_checkout')
    if 'rating_other_checkout' in request.POST:
        feedbacks = feedbacks.filter(feedback_responses__response_category='rating_other_checkout')
    feedbacks = feedbacks.order_by('-id')
    return render(request, "dashboard_app/feedbacks_ajax.html", {'feedbacks':feedbacks})
    # return render(request, "dashboard_app/ajax_fresponses.html", {'feedbacks':feedbacks})
    # return HttpResponse("nope, no ID received")
    # feedbacks = Feedback.objects.filter(id=request.POST['feedback_id'], layout_response__contains=fc)
    # return render(request, "dashboard_app/feedbacks_ajax.html", {'feedbacks':feedbacks})

    # Search feedbacks "contains"
    # if request.POST['feedback_contains']:
    #     print('*-'*20,"WE HAVE ARRIVED")
    #     feedbacks = Feedback.objects.filter(layout_response__contains=fc)

    # return render(request, "dashboard_app/feedbacks_ajax.html", {'feedbacks':feedbacks})


    print("*_"*20,"POST data: ", request.POST)
    if request.POST['Layout'] == "Layout":
        feedback_list['flayout'] = Feedback.objects.filter(feedback_responses__response_category='layout')
    elif request.POST['Features'] == "Features":
        feedback_list['ffeature']= Feedback.objects.filter(feedback_responses__response_category='feature')
    elif requeste.POST['Speed'] == "Speed":
        feedback_list['fspeed']= Feedback.objects.filter(feedback_responses__response_category='speed')
    elif request.POST['Conversion'] == 'Conversion':
        feedback_list[    'fconversion' ]= Feedback.objects.filter(conversion='conversion')
    elif request.POST['Other'] == 'Other':
        feedback_list['fother']= Feedback.objects.filter(feedback_responses__response_category='other')
    print('request.POST', request.POST)
    return render(request, 'dashboard_app/feedbacks_ajax.html', feedback_list)

def delete_feedback(request, feedbackid):
    dfeed = Feedback.objects.get(id=feedbackid)
    dfeed.delete()
    return redirect('/dashboard/feedback')


def subscription(request):
    subscriber_list ={
        'subscriptions':Subscriber.objects.all().order_by('-id')
        }
    return render(request, 'dashboard_app/subscriptions.html', subscriber_list)

def subscribers_search(request):
    subscriber_list ={
        'subscriptions':Subscriber.objects.filter(sub_email__startswith=request.POST['startswith']).order_by('-id')
        }
    return render(request, 'dashboard_app/ajax_subscriptions.html', subscriber_list)

def find(request):
    subscribers = Subscriber.objects.filter(sub_email__startswith=request.POST['email_starts_with'])
    print(subscribers)
    return render(request, "dashboard_app/all.html", {"subscribers":subscribers})

def unsubscribe(request, sub_id):
    sub = Subscriber.objects.get(id=sub_id)
    sub.delete()
    subscriber_list ={
        'subscriptions': list(Subscriber.objects.all().values().order_by('-id'))
        }
    return JsonResponse(subscriber_list)

def unsubscribe_ajax(request, sub_id):
    print('REACHED Unsubscribe_ajax views with sub_id: ', sub_id)
    sub = Subscriber.objects.get(id=sub_id)
    sub.delete()
    subscriber_list ={
        'subscriptions': Subscriber.objects.all().order_by('-id')
        }
    return render(request, 'dashboard_app/ajax_subscriptions.html', subscriber_list)

def add_user(request):
    return HttpResponse('add user functionality page here')

def account_edit(request):
    if request.method == 'POST':
        print("*-"*12, "ARRIVE AT account_edit, request.POST:", request.POST)
        dedit = User.objects.get(id=request.session['id'])
        dedit.desc = request.POST['desc']
        dedit.save()
        print('saved USER desc, User.desc: ', User.objects.values('desc').get(id=request.session['id']))
        response = request.POST['desc']
    return HttpResponse(response)

def demo(request):
    return render(request, 'dashboard_app/ajax_demo.html')

def all_json(request):
    feedbacks = Feedback.objects.all()
    feedbacks_json = serializers.serialize("json", feedbacks)
    return HttpResponse(feedbacks_json, content_type='application/json')

def all_html(request):
    subscribers = Subscriber.objects.all()
    return render(request, "dashboard_app/all.html", {"subscribers":subscribers})

def wall(request):
    if "id" not in request.session:
        return redirect('wall')
    else: 
        post_info = {
            'posts':Post.objects.all().order_by('-id'),
            'comments': Comment.objects.all()
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
        post_info = {
            'posts':Post.objects.all().order_by('-id'),
            'comments': Comment.objects.all(),
        }
        # return redirect("/dashboard/wall")
        return render(request, "dashboard_app/ajax_comment.html", post_info)

def like_post(request, post_id):
    this_post = Post.objects.get(id=post_id)
    this_liker = User.objects.get(id=request.session['id'])
    this_liker.liked_posts.add(this_post)
    post_info = {
        'posts':Post.objects.all().order_by('-id'),
        'comments': Comment.objects.all(),
    }
    # return redirect("/dashboard/wall")
    return render(request, "dashboard_app/ajax_comment.html", post_info)

def delete_post(request, post_id):
    #make sure no one can randomly delete post
    if 'id' in request.session:
        p = Post.objects.get(id=post_id)
        p.delete()
        post_info = {
            'posts':Post.objects.all().order_by('-id'),
            'comments': Comment.objects.all(),
            # 'comments': Comment.objects.filter(commented_post__id=comment_id),
            'related_msg_id':post_id
        }
        # return redirect("/dashboard/wall")
        return render(request, "dashboard_app/ajax_comment.html", post_info)
        # return redirect("/dashboard/wall")
    else:
        return redirect("/loginReg")

def comment_proc(request, post_id):
    #add to database the comment associate with the given message's id
    if request.method == "POST":
        print("*-"*15,"\nReached comment_PROC, request.POST: ", request.POST)
        print("*-"*15,"\nReached comment_PROC, post_id: ", post_id)
        commented_msg = Post.objects.get(id=post_id)
        logged_commentor = User.objects.get(id=request.session['id'])
        add_comment = Comment.objects.create(comment_text=request.POST['comment_text'], commentor=logged_commentor, commented_post=commented_msg)
        print("*-"*20, "Added comment_post")
    post_info = {
        'posts':Post.objects.all().order_by('-id'),
        'comments': Comment.objects.all(),
        'related_msg_id':post_id
    }
    # return redirect("/dashboard/wall")
    return render(request, "dashboard_app/ajax_comment.html", post_info)

def like_comment(request, comment_id):
    this_comment = Comment.objects.get(id=comment_id)
    this_liker = User.objects.get(id=request.session['id'])
    this_liker.liked_comments.add(this_comment)
    post_info = {
        'posts':Post.objects.all().order_by('-id'),
        'comments': Comment.objects.all(),
    }
    # return redirect("/dashboard/wall")
    return render(request, "dashboard_app/ajax_comment.html", post_info)

def delete_comment(request, comment_id):
    #make sure no one can randomly delete post
    if 'id' in request.session:
        c = Comment.objects.get(id=comment_id)
        c.delete()
        post_info = {
        'posts':Post.objects.all().order_by('-id'),
        'comments': Comment.objects.all(),
        # 'comments': Comment.objects.filter(commented_post__id=comment_id),
        'related_msg_id':comment_id
        }
        # return redirect("/dashboard/wall")
        return render(request, "dashboard_app/ajax_comment.html", post_info)
    else:
        return redirect("/loginReg")
