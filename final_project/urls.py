"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from final_app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("", views.PopsicleHomeView.as_view(), name = "home"),
    path("detail/<int:pk>", views.PopsicleDetailView.as_view(), name = "detail"),
    path("add/", views.add_popsicle, name = "add-popsicle"),
    path("contact/", views.contact, name = "contact"),
    path("sign_up/", views.sign_up, name = "sign_up"),
    path("login/", views.user_login, name = "login"),
    path("logout/", views.user_logout, name = "logout"),
    path("popsicle/<int:pk>/update/", views.PopsicleUpdateData.as_view(), name = "update-popsicle-data"),
    path("popsicle/<int:pk>/delete/", views.PopsicleDelete.as_view(), name = "delete-popsicle"),
    path("cart/", views.OrderSummaryView.as_view(), name = "cart"),
    path("add-to-cart/<int:pk>/", views.add_to_cart, name = "add-to-cart"),
    path("remove-from-cart/<int:pk>/", views.remove_from_cart, name = "remove-from-cart"),
    path("remove-product-from-cart/<int:pk>/", views.remove_single_product_from_cart, name = "remove-single-product-from-cart"),
    path("checkout/", views.checkout , name = "checkout"),
    # path("checkout/", views.CheckoutView.as_view() , name = "checkout"),
    path("thank-you/", views.thank , name = "thank"),



    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
