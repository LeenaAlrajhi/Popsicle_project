from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .models import Popsicle
from .forms import PopsicleForm
from django.contrib import messages

def home (request) :

    popsicle = Popsicle.objects.all()

    data = {
        "popsicle" : popsicle

    }
    return render (request, "home.html", data)

def add_popsicle (request) :

    form = PopsicleForm()

    if request.method == "POST" :
        form = PopsicleForm(request.POST)

        if form.is_valid() :
            popsicle = form.save(commit = True)  

            messages.success(request, "your popsicle have been added succesfully")
            return HttpResponseRedirect(reverse("home"))

    data = {
        "form" : form

    }
    return render (request, "add-popsicle.html", data)


        
