from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .models import Popsicle, Profile, Order, OrderProduct, Address
from django.contrib.auth.models import User
from .forms import PopsicleForm, ContactForm, ProfileForm, UserForm, LoginForm, OrderForm, AddressForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView, View
from django.views.generic import ListView, DetailView


class PopsicleHomeView (ListView) :
    model = Popsicle
    paginate_by = 8
    template_name = "home.html"

class PopsicleDetailView (DetailView) :
    model = Popsicle
    template_name = "detail.html"


class OrderSummaryView (LoginRequiredMixin, View) :

    def get (self, *args, **kwargs):
        try: 
            order = Order.objects.get(user = self.request.user, ordered = False)

            data = {
                "order" : order,
            }
            return render(self.request, "cart.html", data)
            
        except ObjectDoesNotExist :
            messages.error(self.request, "You dont have an active order")
            return HttpResponseRedirect(reverse("/"))


def add_to_cart (request, pk) :

    popsicle = get_object_or_404(Popsicle, pk = pk)
    orderـcurrent = Order.objects.filter(user = request.user, ordered = False) # get only orders that have not yet been ordered

    if orderـcurrent.exists() :
        order = orderـcurrent[0]
        order_product, created = OrderProduct.objects.get_or_create(popsicle = popsicle, user = request.user, popsicleId = '1', ordered = False) # get or create this Popsicle in OrderProduct and store it in order_product, created variable is a boolean specifying whether a new object was created, to check that the product has not already been purchased

        # check if the OrderProduct is in the Order
        if order.products.filter(popsicle__pk = popsicle.pk).exists() : # check if this product is already in the cart
            order_product.quantity += 1
            order_product.save()
            messages.success(request, "The quantity of popsicle was updated")
            return HttpResponseRedirect(reverse("cart"))


        else :
            messages.success(request, "This popsicle was added to your cart")
            print("create the order product")
            order.products.add(order_product)

    else :
        ordered_date = timezone.now()
        orderNumber = len(Order.objects.filter()) + 1 # << (( check )) initialize value of the order number for every order from the store with specific serial number, OR use id ?
        order = Order.objects.create(user = request.user, ordered_date = ordered_date, orderNumber = orderNumber) # << Take the location from the user 
        order_product = OrderProduct.objects.create(popsicle = popsicle, user = request.user, popsicleId = '1', ordered = False) # create this Popsicle in OrderProduct and store it in order_product, to check that the product has not already been purchased
        order.products.add(order_product) # link this OrderProduct in Order 
    
    return HttpResponseRedirect(reverse("home"))
        
    # return redirect ("detail", kwargs = {"pk": pk}) # I use redirect  
    


def remove_from_cart (request, pk) :

    popsicle = get_object_or_404(Popsicle, pk = pk)
    orderـcurrent = Order.objects.filter(user = request.user, ordered = False) # get only orders that have not yet been ordered

    if orderـcurrent.exists() :
        order = orderـcurrent[0]

        # check if the OrderProduct is in the Order
        if order.products.filter(popsicle__pk = popsicle.pk).exists() : # check if this product is already in the cart
            order_product = OrderProduct.objects.filter(popsicle = popsicle, user = request.user, popsicleId = '1', ordered = False)[0]
            order.products.remove(order_product)
            messages.success(request, "This popsicle was removed from your cart")

        else :
            messages.info(request, "This popsicle was not in your cart")
    
    else :
        messages.info(request, "You don't have an active order")
    
    return HttpResponseRedirect(reverse("cart") )


def remove_single_product_from_cart (request, pk) :

    popsicle = get_object_or_404(Popsicle, pk = pk)
    orderـcurrent = Order.objects.filter(user = request.user, ordered = False) # get only orders that have not yet been ordered

    if orderـcurrent.exists() :
        order = orderـcurrent[0]

        # check if the OrderProduct is in the Order
        if order.products.filter(popsicle__pk = popsicle.pk).exists() : # check if this product is already in the cart
            order_product = OrderProduct.objects.filter(popsicle = popsicle, user = request.user, popsicleId = '1', ordered = False)[0]
            order_product.quantity -= 1
            if order_product.quantity == 0 :
                order.products.remove(order_product)
                messages.success(request, "This popsicle quantity was updated")
                return HttpResponseRedirect(reverse("cart") )

            order_product.save()
            messages.success(request, "This popsicle quantity was updated")

        else :
            messages.info(request, "This popsicle was not in your cart")
    
    else :
        messages.info(request, "You don't have an active order")
    
    return HttpResponseRedirect(reverse("cart") )
 

class CheckoutView (View):
    def get(self, *args, **kwargs) :
            
        orderForm = OrderForm()
        addressForm = AddressForm()

        data = {
            "orderForm" : orderForm,
            "addressForm" : addressForm
        }
        return render(self.request, "checkout.html", data)

    def post(self, *args, **kwargs) :
        orderForm = OrderForm(request.POST or None) 
        addressForm = AddressForm(request.POST or None)

        if orderForm.is_valid() and addressForm.is_valid() :
            print("The form is valid")

            return HttpResponseRedirect(reverse("checkout"))


def checkout (request) :
    
    orderForm = OrderForm()
    addressForm = AddressForm()

    orders = Order.objects.filter(user = request.user, ordered = False)
    addresses = Address.objects.filter(user = request.user)

    if request.method == "POST" :
        orderForm = OrderForm(request.POST)
        addressForm = AddressForm(request.POST)
        current_order = orders[0]
        current_address = addresses[0]

        if orderForm.is_valid() and addressForm.is_valid() :
            orderF = orderForm.save(commit=False)
            current_order.deliveryTime = orderF.deliveryTime
            current_order.payment_options = orderF.payment_options
            current_order.save()

            addressF = addressForm.save(commit=False)
            current_address.address = addressF.address
            current_address.country = addressF.country
            addressF.user = request.user
            addressF.save()

            return HttpResponseRedirect(reverse("checkout"))

    data = {
        "orderForm" : orderForm,
        "addressForm" : addressForm
    }
    return render(request, "checkout.html", data)


def thank (request) :

    return render(request, "thank.html")


def add_popsicle (request) :

    if request.user.is_superuser :

        form = PopsicleForm()

        if request.method == "POST" :
            form = PopsicleForm(request.POST)

            if form.is_valid() :
                popsicle = form.save(commit = False)  
                if "picture" in request.FILES :
                    popsicle.picture = request.FILES["picture"]
                popsicle.save()

                messages.success(request, "Your popsicle have been added succesfully")
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
            form = ContactForm() 
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


class PopsicleUpdateData (UpdateView) :
    model = Popsicle
    fields = "__all__"
    template_name = "popsicle_update_form.html"


class PopsicleDelete (DeleteView) :
    model = Popsicle
    success_url = reverse_lazy("home")
    template_name = "home.html"


