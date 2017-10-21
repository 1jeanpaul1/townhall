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



# class HomeView(View):
#
#     def get(self, request):
#         template = 'townhall/home.html'
#         context = {'user': request.user}
#         return render(request, template, context)

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

class HomeView(View):

    def get(self, request):
        #gets all the posts
        template = 'townhall/home.html'
        current_user = request.user
        user_interests = current_user.interests
        user_categories = {} # dictionary of user interest related categories
        for interest in user_interests:
            current_categories = interest.category_set.all()
            for category in current_categories:
                user_categories[category.id] = True
        paginate_count = 5

        user_posts = UserPost.objects.all().order_by('added_on')
        # looks at first 5, then filters on that
        filter_five_posts = []
        count = 1
        last_flipped_index = 0
        feed_posts = []
        for current_post in user_posts:
            post = {'user': current_post.user.get_full_name(), 'title': current_post.title,
                    'reactions': current_post.aggregate_reactions, 'idea_or_venture': current_post.idea_or_venture,
                    'comment_count': Comment.objects.filter(post=current_post).count(), 'venture_count': ''}
            feed_posts.append(post)

        context = {'posts': feed_posts}


            # for post_category in current_post.categories:
            #     if user_categories.get(post_category.id, False):
            #         if (coun)
            #         print
            #         count += 1
            #         continue
        return render(request, template, context)


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
        print(request)
        logout(request)
        return redirect('login')




