import logging
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

logger = logging.getLogger(__name__)



class HomeView(View):
    def __init__(self):
        self.context = {}
        self.context['title'] = 'Dashboard'

    def get(self, request, *args, **kwargs):
        return render(request, "home/dashboard.html", self.context)
        