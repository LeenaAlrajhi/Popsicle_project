from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django_countries.fields import CountryField


CATEGORY_CHOICES = (
    ('O' , 'Organic'),
    ('N' , 'Natural'),
    ('F' , 'Fresh'),
    ('V' , 'Vegetable'),
    ('GF' , 'Gluten Free'),
    ('EB' , 'Events Box'),

)

class Profile (models.Model) :

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    mobile = models.CharField(max_length = 20)
    mobileReserve = models.CharField(max_length = 20)

    def __str__(self):
        return self.user.username


class Popsicle (models.Model) :
    name = models.CharField(max_length = 100)
    UPC = models.CharField(max_length = 12)  # Universal Product Code (UPC)
    flavor = models.CharField(max_length = 30) 
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    discount_price = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True, null = True)
    available = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    production_date = models.DateField(blank = True, null = True) # what is the different between default and initial
    expiration_date = models.DateField(blank = True, null = True)
    totalـquantity = models.IntegerField(default = 1) #  all, how I make buyers determine how much they want
    description = models.TextField()
    picture = models.ImageField(upload_to='popsicle-image')
    category = models.CharField(choices = CATEGORY_CHOICES, max_length = 2)

    def __str__(self) :
        return self.name

    def get_absolute_url(self) :
        return reverse ("detail", args=[str(self.id)])

    def get_add_to_cart_url(self) :
        return reverse ("add-to-cart", args=[str(self.id)])

    def get_remove_from_cart_url(self) :
        return reverse ("remove-from-cart", args=[str(self.id)])



class OrderProduct (models.Model) :
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    popsicle = models.ForeignKey(Popsicle, on_delete= models.CASCADE)
    popsicleId = models.IntegerField()
    quantity = models.IntegerField(default = 1)
    ordered = models.BooleanField(default = False)

    def __str__(self) :

        return f"{self.quantity} of {self.popsicle.name}"

    def get_total_product_price (self) :

        return self.quantity * self.popsicle.price 

    def get_total_product_discount_price (self) :

        return self.quantity * self.popsicle.discount_price

    def get_final_price(self) :

        if self.popsicle.discount_price :
            return self.get_total_product_discount_price()

        return self.get_total_product_price()


class Order (models.Model) :
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    orderNumber = models.IntegerField(default = 1) 
    ordered = models.BooleanField(default = False)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    location = models.CharField(max_length = 100)
    time = (
        
        ('1', '10AM-to-1PM'),
        ('2', '1PM-to-4PM'),
        ('3', '4PM-to-7PM'),
        ('4', '7PM-to-10PM'),
    )

    delivery_Time = models.CharField(max_length = 1 , choices = time) 

    choice = [('1' , 'Card') , ('2' , 'Cash on Delivery')]

    payment_options = models.CharField(max_length = 1, choices = choice, default = '1' )


    def __str__(self) :
        return self.user.username


    def get_subtotal(self) :
        total = 0

        for order_product in self.products.all() :
            total += order_product.get_final_price()
        return total 

    def get_shipping(self) :

        if self.get_subtotal() > 100 :
            return "Free"

        return 30

    def get_total(self) :

        subtotal = self.get_subtotal()
        shipping = 0

        if self.get_shipping() != "Free" :
            shipping = self.get_shipping()

        return subtotal + shipping

 
class Address (models.Model) :
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    address = models.CharField(max_length = 100)
    # countries = CountryField(multiple=True)
    country = CountryField(blank_label='(select country)')
    # location = models.CharField(max_length = 100)




