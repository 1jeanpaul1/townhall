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

from models import AppUser, UserPost, Category, UserSavedPosts

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
                    'description': current_post.description, 'post_id': current_post.id}
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
                        'description': current_post.description, 'post_id': current_post.id}
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

        user_saved_posts = UserSavedPosts.objects.all().filter(user=request.user).order_by('added_on').reverse()
        feed_posts = []
        for saved_post in user_saved_posts:
            post = {'user': saved_post.user.get_full_name(), 'title': saved_post.post.title,
                    'reactions': saved_post.post.aggregate_reactions, 'idea_or_venture': saved_post.post.idea_or_venture,
                    'comment_count': Comment.objects.filter(post=saved_post.post).count(), 'venture_count': '',
                    'description': saved_post.post.description, 'post_id': current_post.id}
            if saved_post.post.liked - saved_post.post.disliked < 0:
                post['attitude'] = 0
            else:
                post['attitude'] = 1
            time_passed = datetime.utcnow().replace(tzinfo=pytz.UTC) - saved_post.post.added_on
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
                return redirect(reverse('townhall_external:all_posts'))

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
        # context = {}
        # context['categories'] = Category.objects.all()
        # context['user'] = request.user
        return render(request, self.template_name, {'form': form})

        # process user registration

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            summary = form.cleaned_data['summary']
            description = form.cleaned_data['description']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            UserPost.objects.create(user=request.user, title=title, city=city, state=state, zipcode=zipcode,
                                    description=description, summary=summary)
            return redirect(reverse('townhall_external:all_posts'))

        return render(request, self.template_name, {'form': form})

# class PostView(View):
#     template_name = 'townhall/post.html'
#     def get(self, request):
#         return render(request, self.template_name)


def getPost(request, post_id):
    template_name = 'townhall/post.html'
    current_post = UserPost.objects.get(id=post_id)
    post_data = {'post_user': current_post.user.get_full_name(), 'description': current_post.description,
                 'reactions': current_post.aggregate_reactions, 'title': current_post.title}
    current_post_comments = []
    for comment in current_post.post_comment.all():
        commend_data = {'comment_user': comment.user.get_full_name(), 'content': comment.content}
        current_post_comments.append(commend_data)
    post_data['comments'] = current_post_comments
    context = post_data
    return render(request, template_name, context)