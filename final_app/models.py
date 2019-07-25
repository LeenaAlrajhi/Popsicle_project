from django.db import models
from datetime import datetime
from django.shortcuts import reverse
from django.contrib.auth.models import User

class Popsicle (models.Model) :
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

    def __str__(self) :
        return self.name

    def get_absolute_url(self) :
        return reverse ("detail", args=[str(self.id)])


class Profile (models.Model) :

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    mobile = models.CharField(max_length = 20)
    mobileReserve = models.CharField(max_length = 20)
    # location = models.CharField()

    # time = (
        
    #     ('1', '10AM-to-1PM'),
    #     ('2', '1PM-to-4PM'),
    #     ('3', '4PM-to-7PM'),
    #     ('4', '7PM-to-10PM'),
    # )

    # deliveryTime = models.CharField(max_length = 1 , choices = time) <<< model order


    def __str__(self):
        return self.user.username


