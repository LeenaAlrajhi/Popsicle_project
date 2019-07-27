from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Popsicle, Profile, Order, OrderProduct
from django.contrib.auth.models import User
from .forms import PopsicleForm, ContactForm, ProfileForm, UserForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import ListView, DetailView

class PopsicleHomeView (ListView) :
    model = Popsicle
    template_name = "home.html"

class PopsicleDetailView (DetailView) :
    model = Popsicle
    template_name = "detail.html"

def add_to_cart (request, pk) :

    popsicle = get_object_or_404(Popsicle, pk = pk)
    order_product, created = OrderProduct.objects.get_or_create(popsicle = popsicle, user = request.user, ordered = False) # get or create this Popsicle in OrderProduct and store it in order_product, created variable is a boolean specifying whether a new object was created, to check that the product has not already been purchased
    orderـcurrent = Order.objects.filter(user = request.user, ordered = False) # get only orders that have not yet been ordered

    if orderـcurrent.exists() :
        order = orderـcurrent[0]

        # check if the OrderProduct is in the Order
        if order.products.filter(popsicle__pk = popsicle.pk).exists() : # check if this product is already in the cart
            order_product.quantity += 1
            order_product.save()
            messages.success(request, "The quantity of popsicle was updated")
            return HttpResponseRedirect(reverse("detail"), kwargs = {"pk": pk})


        else :
            messages.success(request, "This popsicle was added to your cart")
            order.products.add(order_product)
            return HttpResponseRedirect(reverse("detail"), kwargs = {"pk": pk})

    else :
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date = ordered_date)
        order.products.add(order_product) # link this OrderProduct in Order 
        return HttpResponseRedirect(reverse("detail"), kwargs = {"pk": pk})
        
    # return redirect ("detail", kwargs = {"pk": pk}) # I use redirect  
    


def remove_from_cart (request, pk) :

    popsicle = get_object_or_404(Popsicle, pk = pk)
    orderـcurrent = Order.objects.filter(user = request.user, ordered = False) # get only orders that have not yet been ordered

    if orderـcurrent.exists() :
        order = orderـcurrent[0]

        # check if the OrderProduct is in the Order
        if order.products.filter(popsicle__pk = popsicle.pk).exists() : # check if this product is already in the cart
            order_product, created = OrderProduct.objects.filter(popsicle = popsicle, user = request.user, ordered = False)[0]
            order.products.remove(order_product)
            messages.success(request, "This popsicle was removed from your cart")
            return HttpResponseRedirect(reverse("detail"), kwargs = {"pk": pk})


        else :
            messages.info(request, "This popsicle was not in your cart")
            return HttpResponseRedirect(reverse("detail"), kwargs = {"pk": pk})
    
    else :
        messages.info(request, "You don't have an active order")
        return HttpResponseRedirect(reverse("detail"), kwargs = {"pk": pk}) 


def home (request) :

    popsicles = Popsicle.objects.all()

    data = {
        "popsicles" : popsicles

    }
    return render (request, "home.html", data)

def detail (request, pk) :

    popsicle = get_object_or_404(Popsicle, pk = pk)

    data = {
        "popsicle" : popsicle
    }
    return render (request, "detail.html", data)

# @permission_required
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


def contact (request) :

    form = ContactForm()

    if request.method == "POST" :
        form = ContactForm(request.POST)

        if form.is_valid() :
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            mobile = form.cleaned_data["mobile"]
            message = form.cleaned_data["message"]
            send_email(name, email, mobile, message) # check
            form = ContactForm() # why ???
            messages.success(request, "email is sent, we will contact you soon")
            return HttpResponseRedirect(reverse("home"))

    data = {
        "form" : form

    }
    return render (request, "contact.html", data)


def send_email(name, email, mobile, message):
    print('sending email done')


def sign_up (request) :

    userForm = UserForm()
    profileForm = ProfileForm()

    if request.method == "POST" :

        userForm = UserForm(request.POST)
        profileForm = ProfileForm(request.POST)

        if userForm.is_valid() and profileForm.is_valid() :
            user = userForm.save(commit=False)
            user.set_password(user.password)
            user.save()

            profile = profileForm.save(commit=False)
            profile.user = user
            profile.save()

            return HttpResponseRedirect(reverse("home"))

    data = {
        "userForm" : userForm,
        "profileForm" : profileForm
    }
    return render(request, "sign_up.html", data)


def user_login (request) :

    form = LoginForm()

    if request.method == "POST" :
        form = LoginForm(request.POST)

        if form.is_valid() :
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate (username = username, password = password)

            if user :

                if user.is_active :
                    login(request, user)

                    return HttpResponseRedirect(reverse("home"))
                
                else :
                    messages.error(request, "user is not active")

            else :
                messages.error(request, "invalid username or password")

    data = {
        "form" : form
    }
    return render(request, "user_login.html", data)


@login_required
def user_logout (request) :

    logout(request)
    return HttpResponseRedirect(reverse("home"))

                
# Cart Page

# def product_list (request) :

#     popsicles = Popsicle.objects.all()

#     data = {
#         "popsicles" : popsicles

#     }
#     return render (request, "product_list.html", data)


class PopsicleUpdateData (UpdateView) :
    model = Popsicle
    fields = "__all__"
    template_name = "popsicle_update_form.html"


class PopsicleDelete (DeleteView) :
    model = Popsicle
    success_url = reverse_lazy("home")
    template_name = "home.html"


