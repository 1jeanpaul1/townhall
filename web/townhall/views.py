# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytz
from django.http import HttpResponse, HttpRequest
from django.contrib import auth
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
# from django.core.context_processors
from django.urls import reverse
from django.views.generic import View
from django.http import Http404
from django.shortcuts import render
from models import UserPost, Comment

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.views.generic import View
from .forms import UserRegistration, UserFormPost, UserLogin
from datetime import timedelta
# import datetime
from datetime import datetime
from django import template
from django.utils.timesince import timesince

# from django.contrib import auth

from models import AppUser, UserPost, Category

class ProfileView(View):
    def get(self, request):
        cururl = request.path
        currentprofile = AppUser.objects.get(email=str(HttpRequest.path[17:]))
        if (currentprofile.is_entrepreneur):
            template = 'entrepreneurprofile.html'
            context = {}
            context['username'] = currentprofile.get_full_name()
            context['numideas'] = UserPost.objects.filter(currentprofile).filter(is_idea=True).count()
            context['numventures'] = UserPost.objects.filter(currentprofile).filter(is_idea=False).count()
            context['location'] = currentprofile.city + ", " + currentprofile.country
            context['bio'] = currentprofile.bio
            context['email'] = currentprofile.email
            context['phonenumber'] = currentprofile.phone_number
            context['website'] = currentprofile.website
            context['interests'] = currentprofile.interests
            context['photo'] = currentprofile.profile_image
            return render(request, template, context)
        elif ():
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


class AllPostsView(View):
    def get(self, request):
        # gets all the posts
        template = 'townhall/home.html'
        current_user = request.user
        # user_interests = current_user.interests.all()
        # user_categories = {}  # dictionary of user interest related categories
        # for interest in user_interests:
        #     current_categories = interest.category_set.all()
        #     for category in current_categories:
        #         user_categories[category.id] = True

        user_posts = UserPost.objects.all().order_by('added_on').reverse()
        feed_posts = []
        for current_post in user_posts:
            post = {'user': current_post.user.get_full_name(), 'title': current_post.title,
                    'reactions': current_post.aggregate_reactions, 'idea_or_venture': current_post.idea_or_venture,
                    'comment_count': Comment.objects.filter(post=current_post).count(), 'venture_count': '',
                    'description': current_post.description}
            if current_post.liked - current_post.disliked < 0:
                post['attitude'] = 0
            else:
                post['attitude'] = 1
            time_passed = datetime.utcnow().replace(tzinfo=pytz.UTC) - current_post.added_on
            days = time_passed.days
            hours = time_passed.seconds // 3600
            minutest_passed = (time_passed.seconds // 60) % 60
            print("****days test***")
            print(days)
            print(time_passed)
            if days > 0:
                if days == 1:
                    statement = 'day'
                else:
                    statement = 'days'
                time_since = '%s %s ago' % (days, statement)
            elif hours > 0:
                if hours == 1:
                    statement = 'hour'
                else:
                    statement = 'hours'
                time_since = '%s %s ago' % (hours, statement)
            elif minutest_passed > 0:
                if minutest_passed == 1:
                    statement = 'minute'
                else:
                    statement = 'minutes'
                time_since = '%s %s ago' % (minutest_passed, statement)
            else:
                time_since = 'just now'
            post['time_since_upload'] = time_since
            feed_posts.append(post)

        context = {'posts': feed_posts, 'user': request.user.get_full_name, 'tab': 1}
        return render(request, template, context)

class FeedView(View):
    def get(self, request):
        # gets all the posts
        template = 'townhall/home.html'
        current_user = request.user
        user_interests = current_user.interests.all()
        user_categories = {}  # dictionary of user interest related categories
        for interest in user_interests:
            current_categories = interest.category_interests.all()
            for category in current_categories:
                user_categories[category.id] = True

        user_posts = UserPost.objects.all().order_by('added_on').reverse()
        feed_posts = []
        for current_post in user_posts:
            related_post = False
            for x in current_post.categories.all():
                if user_categories.get(x.id, False):
                    related_post = True
                    break
            if related_post:
                post = {'user': current_post.user.get_full_name(), 'title': current_post.title,
                        'reactions': current_post.aggregate_reactions, 'idea_or_venture': current_post.idea_or_venture,
                        'comment_count': Comment.objects.filter(post=current_post).count(), 'venture_count': '',
                        'description': current_post.description}
                if current_post.liked - current_post.disliked < 0:
                    post['attitude'] = 0
                else:
                    post['attitude'] = 1
                time_passed = datetime.utcnow().replace(tzinfo=pytz.UTC) - current_post.added_on
                days = time_passed.days
                hours = time_passed.seconds // 3600
                minutest_passed = (time_passed.seconds // 60) % 60
                if days > 0:
                    if days == 1:
                        statement = 'day'
                    else:
                        statement = 'days'
                    time_since = '%s %s ago' % (days, statement)
                elif hours > 0:
                    if hours == 1:
                        statement = 'hour'
                    else:
                        statement = 'hours'
                    time_since = '%s %s ago' % (hours, statement)
                elif minutest_passed > 0:
                    if minutest_passed == 1:
                        statement = 'minute'
                    else:
                        statement = 'minutes'
                    time_since = '%s %s ago' % (minutest_passed, statement)
                else:
                    time_since = 'just now'
                post['time_since_upload'] = time_since
                feed_posts.append(post)
        context = {'posts': feed_posts, 'user': request.user.get_full_name, 'tab': 0}
        return render(request, template, context)

class SavedPostsView(View):
    def get(self, request):
        # gets all the posts
        template = 'townhall/home.html'
        current_user = request.user
        # user_interests = current_user.interests.all()
        # user_categories = {}  # dictionary of user interest related categories
        # for interest in user_interests:
        #     current_categories = interest.category_set.all()
        #     for category in current_categories:
        #         user_categories[category.id] = True

        user_posts = UserPost.objects.all().order_by('added_on').reverse()
        feed_posts = []
        for current_post in user_posts:
            post = {'user': current_post.user.get_full_name(), 'title': current_post.title,
                    'reactions': current_post.aggregate_reactions, 'idea_or_venture': current_post.idea_or_venture,
                    'comment_count': Comment.objects.filter(post=current_post).count(), 'venture_count': '',
                    'description': current_post.description}
            if current_post.liked - current_post.disliked < 0:
                post['attitude'] = 0
            else:
                post['attitude'] = 1
            time_passed = datetime.utcnow().replace(tzinfo=pytz.UTC) - current_post.added_on
            days = time_passed.days
            hours = time_passed.seconds // 3600
            minutest_passed = (time_passed.seconds // 60) % 60
            print("****days test***")
            print(days)
            print(time_passed)
            if days > 0:
                if days == 1:
                    statement = 'day'
                else:
                    statement = 'days'
                time_since = '%s %s ago' % (days, statement)
            elif hours > 0:
                if hours == 1:
                    statement = 'hour'
                else:
                    statement = 'hours'
                time_since = '%s %s ago' % (hours, statement)
            elif minutest_passed > 0:
                if minutest_passed == 1:
                    statement = 'minute'
                else:
                    statement = 'minutes'
                time_since = '%s %s ago' % (minutest_passed, statement)
            else:
                time_since = 'just now'
            post['time_since_upload'] = time_since
            feed_posts.append(post)

        context = {'posts': feed_posts, 'user': request.user.get_full_name, 'tab': 2}
        return render(request, template, context)


class UserRegistrationView(View):
    form_class = UserRegistration
    template_name = 'townhall/home.html'

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
                return HttpResponseRedirect('../newpost')

        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    logout = '/'

    def get(self, request):
        # print(request)
        logout(request)
        return redirect(reverse('townhall_external:login'))


class LoginView(View):
    form_class = UserLogin
    success_template_name = 'townhall/home.html'
    failure_template_name = 'townhall/login.html'

    # displays a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.failure_template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        print(form.is_valid())
        print(form.data)
        print(request.POST)
        if form.is_valid():
            # form_user = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            print("*****user****")
            print(user.is_active)
            print(user)
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('../home')

        return render(request, self.failure_template_name, {'form': form})


class UserFormPostView(View):
    form_class = UserFormPost
    template_name = 'townhall/newpost.html'

    # blank form
    def get(self, request):
        form = self.form_class(None)
        context = {}
        context['categories'] = Category.objects.all()
        context['user'] = request.user
        return render(request, self.template_name, {'form': form})

        # process user registration

    def post(self, request):
        # print(request.POST)
        # form = self.form_class(request.POST)
        #print(form.is_valid())
        #print(form.data)
        # if form.is_valid():
        curuser = request.user
        curuser.is_active = True
        # print(curuser)
            # post = form.save(commit=False)
        data = request.POST
        title = data.get('title', '')
        summary = data.get('summary', '')
        description = data.get('description', '')
        is_idea = 'is_idea' in data
        # categories = data.get('categories', '')
        # print(data)
        # print(is_idea)
        print(request.user.id)
        curuser.save()
        curuser.fullclean
        post = UserPost.objects.create(user_id=request.user.id, title=title, summary=summary, description=description,
                                is_idea=is_idea)
        # post.save()
        # # post.categories.add(categories)
        #     # cleanred (normalized data)
        #     title = form.cleaned_data['title']
        #     summary = form.cleaned_data['summary']
        #     description = form.cleaned_data['description']
        #     is_idea = form.cleaned_data['is_idea']
        #     categories = form.cleaned_data['categories']
        #
        #     post.save()
        #
        #     if user.is_active:
        #         login(request, user)
        #         return HttpResponseRedirect('../home')
        #
        # return render(request, self.template_name, {'form': form})
            # user = curuser
            # title = form.cleaned_data['title']
            # summary = form.cleaned_data['summary']
            # description = form.cleaned_data['description']
            # # is_idea = form.cleaned_data['is_idea']
            # # categories = form.cleaned_data['categories']
            # # print(form.data)
            # post.save()

            # if user.is_active:
            #     login(request, user)
            #     return HttpResponseRedirect('../home')

        return render(request, self.template_name, )#{'form': form})


# >>>>>>> acae25d5ee2be304c394ae71c7acc790a143eaa3
