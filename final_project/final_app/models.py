from django.db import models
from datetime import datetime

class Popsicle (models.Model) :

    name = models.CharField(max_length = 100)
    UPC = models.CharField(max_length = 12)  # Universal Product Code (UPC)
    flavor = models.CharField(max_length = 30) # remove ?
    price = models.CharField(max_length = 10)
    available = models.BooleanField(default = True)

    types = (
        ('I', 'IceCream'),
        ('F', 'Freezie')
    )

    popsicle_type = models.CharField(max_length = 1 , choices = types)
    production_date = models.DateField(auto_now=True) # what is the different between default and initial
    expiration_date = models.DateField(auto_now=True)
    quantity = models.CharField(max_length = 10) #  all, how I make buyers determine how much they want
    description = models.TextField()


    def __str__(self) :
        return self.name
