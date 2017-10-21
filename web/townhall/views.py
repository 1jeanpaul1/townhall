# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.generic import View
from django.http import Http404
from django.shortcuts import render

from django.shortcuts import render

from models import AppUser, UserPost

# Create your views here.


def index(request):
    return HttpResponse("TOWN HALL START")

def detail(request, question_id):
    return HttpResponse("You're looking at FREAKING TOWN HALL %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


class HomeView(View):

    def get(self, request):
        template = 'home.html'
        context = {}
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