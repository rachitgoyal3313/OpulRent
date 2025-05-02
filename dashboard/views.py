from django.shortcuts import render
from django.db import models
from .models import Transaction, RentalAgreement
from property.models import PropertyForSale, PropertyForRent
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse  
from django.urls import reverse_lazy  

ALLOWED_CITIES = ['Mumbai', 'Pune', 'Nagpur', 'Bangalore', 'New Delhi']

def home(request):
    # Fetch a property for sale with available units first
    property = PropertyForSale.objects.filter(units_sold__lt=models.F('total_units')).first()
    property_type = 'sale'
    
    # If no properties for sale, fetch a rental property
    if not property:
        property = PropertyForRent.objects.first()
        property_type = 'rent'
    
    context = {
        'property': property,
        'property_type': property_type
    }
    return render(request, 'index.html', context)

def marketplace(request):
    properties_sale = PropertyForSale.objects.filter(units_sold__lt=models.F('total_units'))
    properties_rent = PropertyForRent.objects.all()
    context = {
        'properties_sale': properties_sale,
        'properties_rent': properties_rent
    }
    return render(request, 'marketplace.html', context)

@login_required(login_url=reverse_lazy('login'))
def dashboard(request):
    user = request.user
    
    # Owned properties
    owned_sale = PropertyForSale.objects.filter(owner=user)
    owned_rent = PropertyForRent.objects.filter(owner=user)
    
    # Purchased properties
    purchased_transactions = Transaction.objects.filter(buyer=user, transaction_type='sale').select_related('property_sale')
    
    # Count unique purchased properties
    purchased_properties = PropertyForSale.objects.filter(sale_transactions__buyer=user).distinct()
    
    # Total properties owned (owned + purchased)
    total_properties_owned = owned_sale.count() + owned_rent.count() + purchased_properties.count()
    
    # Rented properties
    rented = RentalAgreement.objects.filter(tenant=user, active=True).select_related('property')
    
    # Listed properties
    listed_sale = PropertyForSale.objects.filter(owner=user, units_sold__lt=models.F('total_units'))
    listed_rent = PropertyForRent.objects.filter(owner=user)
    
    # Financials
    rental_income = sum(
        agreement.monthly_rent 
        for agreement in RentalAgreement.objects.filter(landlord=user, active=True)
    )
    
    sales_income = sum(
        transaction.amount 
        for transaction in Transaction.objects.filter(seller=user, transaction_type='sale')
    )
    
    context = {
        'owned_sale': owned_sale,
        'owned_rent': owned_rent,
        'purchased_transactions': purchased_transactions,
        'rented': rented,
        'listed_sale': listed_sale,
        'listed_rent': listed_rent,
        'total_properties_owned': total_properties_owned,
        'rental_income': rental_income,
        'sales_income': sales_income,
        'kyc_status': 'Approved'
    }
    return render(request, 'dashboard.html', context)