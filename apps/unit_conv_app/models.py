from __future__ import unicode_literals
from django.db import models
import re
name_regex = re.compile(r'^[a-zA-Z\D.-]+$')
email_regex = re.compile(r'^[a-zA-Z\d.+_-]+@[a-zA-Z\d_-]+\.[a-zA-Z]+$')
pw_regex = re.compile(r'^.*(?=.*\d)(?=.*[a-zA-Z]).*$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name cannot be fewer than 2 charcters"
        elif not name_regex.match(postData['first_name']):
            errors['first_name'] = "First name should be letters only"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name cannot be fewer than 2 charcters"
        elif not name_regex.match(postData['last_name']):
            errors['last_name'] = "Last name should be letters only"
        if len(postData['email']) < 6:
            errors['email'] = "Invalid Email"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Invalid email - address format"
        elif User.objects.filter(email = postData['email']):
            errors['email'] = "Email already exists"
        if len(postData['password']) < 8:
            errors['password'] = "Password cannot be fewer than 8 characters"
        elif not postData['password'] == postData['confirm_password']:
            errors['password'] = "Need to match Password Confirmation"
        elif not pw_regex.match(postData['password']):
            errors['password'] = "Password needs at least one digit and one capital letter"
        return errors
    
    def subscribe_validator(self, postData):
        errors = {}
        if len(postData['subscriber_email']) < 1:
            errors['subscribe_error'] = "Email cannot be blank"
        elif not email_regex.match(postData['subscriber_email']):
            errors['susbscribe_error'] = "Invalid email format"
        return errors

    def feedback_validator(self, postData):
        errors={}
        if 'rating' not in postData:
            errors['rating'] = "Please rate our site"
        return errors

    def edit_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name cannot be fewer than 2 charcters"
        elif not name_regex.match(postData['first_name']):
            errors['first_name'] = "Letters only"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name cannot be fewer than 2 charcters"
        elif not name_regex.match(postData['last_name']):
            errors['last_name'] = "Last name should be letters only"
        if len(postData['email']) < 6:
            errors['email'] = "Invalid Email"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Invalid email - address format"
        return errors

    def change_password_validator(self, postData):
        #password inputs cannot be blank
        new_pw = postData['new_password']
        confirm_new_pw = postData['confirm_new_password']
        errors = {}
        if len(new_pw) < 8:
            errors['new_password'] = "Password needs to be at least 8 characters"
        #validating password requirements
        elif not pw_regex.match(new_pw):
            errors['new_password'] = "New Password needs to have digit, capital letter, & lowercase letter"
        if len(confirm_new_pw) < 1:
            errors['confirm_new_password'] = "Need to confirm new password"
        #confirm & new passwords need to match
        elif not confirm_new_pw == new_pw:
            errors['confirm_new_password'] = "Confirm password needs to match new password"
        return errors
        
    def post_validator(self, postData):
        errors = {}
        if len(postData['content']) < 1:
            errors['post']= "Cannot post an empty message"
        return errors

    def add_image_validator(self, postData):
        errors = {}
        if len(postData['title'])< 1:
            errors['title'] = "Title cannot be blank"
        if len(postData['image_url'])<1:
            errors['image_url'] = "URL cannot be blank"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length=255)
    desc = models.TextField(default="")
    user_level = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Post(models.Model):
    post_text = models.TextField()
    poster = models.ForeignKey(User, related_name="posts")
    post_liker = models.ManyToManyField(User, related_name="liked_posts")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


class Comment(models.Model):
    comment_text = models.TextField()
    commentor = models.ForeignKey(User, related_name="user_comments")
    commented_post = models.ForeignKey(Post, related_name="posted_comments")
    comment_liker = models.ManyToManyField(User, related_name="liked_comments")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Image(models.Model):
    image_name = models.CharField(max_length=255)
    image_url = models.URLField(max_length=255)
    uploader = models.ForeignKey(User, related_name="uploaded_images")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Subscriber(models.Model):
    sub_email = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Feedback(models.Model):
    rating = models.PositiveSmallIntegerField()
    feedback_email = models.CharField(max_length=255, default='')
    status = models.CharField(max_length =45, default='')
    status_comment = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # layout=models.CharField(max_length=45, default='')
    # layout_response = models.TextField(blank = True, default='')
    # feature=models.CharField(max_length=45, default='')
    # feature_response = models.TextField(blank = True, default='')
    # speed=models.CharField(max_length=45, default='')
    # speed_response = models.TextField(blank = True, default='')
    # conversion=models.CharField(max_length=45, default='')
    # conversion_response = models.TextField(blank = True, default='')
    # other=models.CharField(max_length=45, default='')
    # other_response = models.TextField(blank = True, default='')
    objects = UserManager()

class Response(models.Model):
    response_text = models.TextField()
    response_category = models.CharField(max_length=255)
    respond_feedback = models.ForeignKey(Feedback, related_name="feedback_responses")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Image(models.Model):
    title = models.CharField(max_length=255)
    image_url = models.URLField(null=True, blank=True)
    adder = models.ForeignKey(User, related_name='added_image_urls')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()