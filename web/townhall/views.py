# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import auth
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
# from django.core.context_processors
from django.views.generic import View
from django.http import Http404
from django.shortcuts import render
from models import UserPost, Comment

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.views.generic import View
from .forms import UserRegistration

# from django.contrib import auth

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

# def login(request):
#     c = {}
#     c.update(csrf(request))
#     return render(request, 'townhall/login.html', c)
#
#
# def auth_view(request):
#     username = request.POST.get('username', '')
#     password = request.POST.get('password', '')
#     user = auth.authenticate(username=username, password=password)
#
#     if user is not None:
#         auth.login(request, user)
#         return HttpResponseRedirect('../../townhall/home/')
#     else:
#         return HttpResponseRedirect('../../townhall/login/')



class HomeView(View):

    def get(self, request):
        template = 'townhall/home.html'
        context = {'user': request.user}
        return render(request, template, context)

class ProfileView(View):

    def get(self, request):
        currentuser = AppUser.objects.get(email=request.user)
        if (currentuser.is_entrepreneur):
            template = 'entrepreneurprofile.html'
            context = {}
            context['username']= currentuser.get_full_name()
            context['numideas']= UserPost.objects.filter(currentuser).filter(is_idea=True).count()
            context['numventures'] = UserPost.objects.filter(currentuser).filter(is_idea=False).count()
            context['location'] = currentuser.city + ", " + currentuser.country
            context['bio'] = currentuser.bio
            context['email'] = currentuser.email
            context['phonenumber'] = currentuser.phone_number
            context['website'] = currentuser.website
            context['interests'] = currentuser.interests
            context['photo'] = currentuser.profile_image
            return render(request, template, context)
        elif():
            template = 'citizenprofile'
            context = {}
            context['username'] = currentuser.get_full_name()
            context['numideas'] = UserPost.objects.filter(currentuser).filter(is_idea=True).count()
            context['location'] = currentuser.city + ", " + currentuser.country
            context['bio'] = currentuser.bio
            context['email'] = currentuser.email
            context['phonenumber'] = currentuser.phone_number
            context['photo'] = currentuser.profile_image
            return render(request, template, context)

class FeedView(View):

    def get(self, request):
        #gets all the posts
        user_posts = UserPost.objects.all()

        for post in user_posts:
            post = {'user': post.user.get_full_name(), 'title': post.title, 'reactions': post.aggregate_reactions,
                    'idea_or_venture': post.idea_or_venture, 'comment_count': '', 'venture_count': ''}
            post['comment_count'] = Comment.objects.filter(post=post).count()



class UserRegistrationView(View):
    form_class = UserRegistration
    template_name = 'townhall/register.html'

    # displays a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process user registration
    def post(self, request):
        print(request.POST)
        form = self.form_class(request.POST)
        # print(form.is_valid())
        # print(form.data)
        if form.is_valid():
            user = form.save(commit=False)

            # cleanred (normalized data)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=email, password=password)

            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('../home')

        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    logout = '/'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(self.logout)




