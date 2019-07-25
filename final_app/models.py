from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


CATEGORY_CHOICES = (
    ('O' , 'Organic'),
    ('N' , 'Natural'),
    ('F' , 'Fresh'),
    ('V' , 'Vegetable'),
    ('GF' , 'Gluten Free'),
    ('EB' , 'Events Box'),

)

# LABEL_CHOICES = (
#     ('P' , 'primary'),
#     ('S' , 'secondary'),
#     ('D' , 'danger'),

# )


class Profile (models.Model) :

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    mobile = models.CharField(max_length = 20)
    mobileReserve = models.CharField(max_length = 20)
    # location = models.CharField()


    def __str__(self):
        return self.user.username


class Popsicle (models.Model) :
    # order = models.ForeignKey(Order, on_delete= models.CASCADE)   <<<CHECK>>>
    name = models.CharField(max_length = 100)
    UPC = models.CharField(max_length = 12)  # Universal Product Code (UPC)
    flavor = models.CharField(max_length = 30) # remove ?
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    available = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    types = (
        ('I', 'IceCream'),
        ('F', 'Freezie')
    )

    popsicle_type = models.CharField(max_length = 1 , choices = types)
    production_date = models.DateField() # what is the different between default and initial
    expiration_date = models.DateField()
    quantity = models.CharField(max_length = 10) #  all, how I make buyers determine how much they want
    description = models.TextField()
    picture = models.ImageField(upload_to='popsicle-image')
    category = models.CharField(choices = CATEGORY_CHOICES, max_length = 2)
    # label = models.CharField(choices = LABEL_CHOICES, max_length = 1) << change color of each category

    def __str__(self) :
        return self.name

    def get_absolute_url(self) :
        return reverse ("detail", args=[str(self.id)])



class OrderProduct (models.Model) :
    popsicle = models.ForeignKey(Popsicle, on_delete= models.CASCADE)
    

    def __str__(self) :

        pass


class Order (models.Model) :

    purchaser = models.ForeignKey(Profile, on_delete= models.CASCADE)
    orderNumber = models.CharField(max_length = 30)
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

    deliveryTime = models.CharField(max_length = 1 , choices = time) 

    choice = [('1' , 'Card') , ('2' , 'Cash on Delivery')]

    payment_options = models.CharField(max_length = 1, choices = choice, default = '1' )


    def __str__(self) :
        return self.purchaser.username


    # def is_upperclass(self):
    #     return self.year_in_school in (self.JUNIOR, self.SENIOR)


