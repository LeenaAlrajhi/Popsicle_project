from django import forms
from .models import Popsicle

class PopsicleForm (forms.Form) :

    class Meta :
        module = Popsicle
        fields = ["name", "UPC", "flavor", "popsicle_type", "price",
                  "quantity", "description", "available", "production_date", "expiration_date"]
                  
