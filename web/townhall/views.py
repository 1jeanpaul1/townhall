# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpRequest
from django.template.context_processors import csrf
# from django.core.context_processors
from django.views.generic import View
from django.http import Http404
from django.shortcuts import render
from models import UserPost, Comment

from django.shortcuts import render

from models import AppUser, UserPost

# Create your views here.


# def index(request):
#     return HttpResponse("TOWN HALL START")
#
# def detail(request, question_id):
#     return HttpResponse("You're looking at FREAKING TOWN HALL %s." % question_id)
#
# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)
#
# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)

def login(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'townhall/login.html', c)

# def auth_view(request):
#     username = request.POST.get('username', '')
#     password = request.POST.get('password', '')
#     user = auth.authenticate(username=username, password=password)
#
#     if user is not None:



class HomeView(View):

    def get(self, request):
        template = 'townhall/home.html'
        context = {'user': request.user}
        return render(request, template, context)

class ProfileView(View):

    def get(self, request):
        cururl = request.path
        currentprofile = AppUser.objects.get(email=HttpRequest.path[17:])
        if (currentprofile.is_entrepreneur):
            template = 'entrepreneurprofile.html'
            context = {}
            context['username']= currentprofile.get_full_name()
            context['numideas']= UserPost.objects.filter(currentprofile).filter(is_idea=True).count()
            context['numventures'] = UserPost.objects.filter(currentprofile).filter(is_idea=False).count()
            context['location'] = currentprofile.city + ", " + currentprofile.country
            context['bio'] = currentprofile.bio
            context['email'] = currentprofile.email
            context['phonenumber'] = currentprofile.phone_number
            context['website'] = currentprofile.website
            context['interests'] = currentprofile.interests
            context['photo'] = currentprofile.profile_image
            return render(request, template, context)
        elif():
            template = 'citizenprofile'
            context = {}
            context['username'] = currentprofile.get_full_name()
            context['numideas'] = UserPost.objects.filter(currentprofile).filter(is_idea=True).count()
            context['location'] = currentprofile.city + ", " + currentprofile.country
            context['bio'] = currentprofile.bio
            context['email'] = currentprofile.email
            context['phonenumber'] = currentprofile.phone_number
            context['photo'] = currentprofile.profile_image
            return render(request, template, context)

class FeedView(View):

    def get(self, request):
        #gets all the posts
        user_posts = UserPost.objects.all()

        for post in user_posts:
            post = {'user': post.user.get_full_name(), 'title': post.title, 'reactions': post.aggregate_reactions,
                    'idea_or_venture': post.idea_or_venture, 'comment_count': '', 'venture_count': ''}
            post['comment_count'] = Comment.objects.filter(post=post).count()







