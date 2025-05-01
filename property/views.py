from django.shortcuts import render
from .models import PropertyForSale, PropertyForRent

def marketplace(request):
    properties_for_sale = PropertyForSale.objects.all()
    properties_for_rent = PropertyForRent.objects.all()
    properties = list(properties_for_sale) + list(properties_for_rent)
    return render(request, 'marketplace.html', {'properties': properties})

def buy_properties(request):
    properties = PropertyForSale.objects.all()
    return render(request, 'buy.html', {'properties': properties})

def rent_properties(request):
    properties = PropertyForRent.objects.all()
    return render(request, 'rent.html', {'properties': properties})