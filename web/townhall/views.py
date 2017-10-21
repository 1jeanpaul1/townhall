# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.generic import View
from django.http import Http404
from django.shortcuts import render

from django.shortcuts import render

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
