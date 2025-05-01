from django.shortcuts import render
from django.db import models
from .models import Transaction, RentalAgreement
from property.models import PropertyForSale, PropertyForRent
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'index.html')

def marketplace(request):
    properties_sale = PropertyForSale.objects.filter(units_sold__lt=models.F('total_units'))
    properties_rent = PropertyForRent.objects.all()
    context = {
        'properties_sale': properties_sale,
        'properties_rent': properties_rent
    }
    return render(request, 'marketplace.html', context)

@login_required
def dashboard(request):
    user = request.user
    
    # Owned properties (where user is owner)
    owned_sale = PropertyForSale.objects.filter(owner=user)
    owned_rent = PropertyForRent.objects.filter(owner=user)
    
    # Purchased properties (via transactions)
    purchased = Transaction.objects.filter(buyer=user, transaction_type='sale')
    
    # Rented properties (where user is tenant)
    rented = RentalAgreement.objects.filter(tenant=user, active=True)
    
    # Listed properties (owned and available)
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
        'purchased': purchased,
        'rented': rented,
        'listed_sale': listed_sale,
        'listed_rent': listed_rent,
        'rental_income': rental_income,
        'sales_income': sales_income,
        'kyc_status': 'Approved'  # Could be dynamic
    }
    return render(request, 'dashboard.html', context)