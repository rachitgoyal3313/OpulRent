from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import PropertyForSale, PropertyForRent
from dashboard.models import Transaction, RentalAgreement
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone

def marketplace(request):
    search_query = request.GET.get('search', '')
    properties_for_sale = PropertyForSale.objects.filter(units_sold__lt=models.F('total_units'))
    properties_for_rent = PropertyForRent.objects.all()
    
    if search_query:
        properties_for_sale = properties_for_sale.filter(
            Q(house_type__icontains=search_query) |
            Q(locality__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(beds__icontains=search_query)
        )
        properties_for_rent = properties_for_rent.filter(
            Q(house_type__icontains=search_query) |
            Q(locality__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(beds__icontains=search_query)
        )
    
    properties = list(properties_for_sale) + list(properties_for_rent)
    return render(request, 'marketplace.html', {'properties': properties})

def buy_properties(request):
    search_query = request.GET.get('search', '')
    if search_query:
        properties = PropertyForSale.objects.filter(
            Q(house_type__icontains=search_query) |
            Q(locality__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(beds__icontains=search_query),
            units_sold__lt=models.F('total_units')
        )
    else:
        properties = PropertyForSale.objects.filter(units_sold__lt=models.F('total_units'))
    return render(request, 'buy.html', {'properties': properties})

def rent_properties(request):
    search_query = request.GET.get('search', '')
    if search_query:
        properties = PropertyForRent.objects.filter(
            Q(house_type__icontains=search_query) |
            Q(locality__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(beds__icontains=search_query)
        )
    else:
        properties = PropertyForRent.objects.all()
    return render(request, 'rent.html', {'properties': properties})

def property_detail(request, property_id, property_type):
    if property_type == 'sale':
        property_obj = get_object_or_404(PropertyForSale, id=property_id)
        context = {
            'property': property_obj,
            'property_type': property_type,
            'unit_price': property_obj.unit_price,
            'units_available': property_obj.units_available,
        }
    else:
        property_obj = get_object_or_404(PropertyForRent, id=property_id)
        context = {
            'property': property_obj,
            'property_type': property_type,
        }
    return render(request, 'property.html', context)

@login_required(login_url='user/login/')
def property_action(request, property_id, property_type):
    if property_type == 'sale':
        property_obj = get_object_or_404(PropertyForSale, id=property_id)
        units_to_buy = int(request.POST.get('units', 1))
        if units_to_buy > property_obj.units_available:
            messages.error(request, 'Not enough units available for purchase.')
            return redirect('property_detail', property_id=property_id, property_type=property_type)
        
        # Calculate transaction amount
        amount = property_obj.unit_price * units_to_buy
        
        # Record transaction
        Transaction.objects.create(
            property_sale=property_obj,
            buyer=request.user,
            seller=property_obj.owner,
            transaction_type='sale',
            amount=amount,
            units=units_to_buy
        )
        
        # Update units sold
        property_obj.units_sold += units_to_buy
        property_obj.save()
        
        messages.success(request, 'Property purchase successful!')
        return redirect('purchase_confirmation', property_id=property_id)
    else:
        property_obj = get_object_or_404(PropertyForRent, id=property_id)
        start_date = timezone.now().date()
        end_date = start_date + timezone.timedelta(days=365)
        RentalAgreement.objects.create(
            property=property_obj,
            tenant=request.user,
            landlord=property_obj.owner,
            monthly_rent=property_obj.rent,
            start_date=start_date,
            end_date=end_date,
            active=True
        )
        
        messages.success(request, 'Property rental successful!')
        return redirect('rental_confirmation', property_id=property_id)

@login_required(login_url='user/login/')
def purchase_confirmation(request, property_id):
    property_obj = get_object_or_404(PropertyForSale, id=property_id)
    return render(request, 'purchase_confirmation.html', {'property': property_obj})

@login_required(login_url='/user/login/')
def rental_confirmation(request, property_id):
    property_obj = get_object_or_404(PropertyForRent, id=property_id)
    return render(request, 'rental_confirmation.html', {'property': property_obj})

@login_required(login_url='/user/login/')
def mint(request):
    if request.method == 'POST':
        house_type = request.POST.get('house_type')
        locality = request.POST.get('locality')
        city = request.POST.get('city')
        area = float(request.POST.get('area', 0))
        beds = int(request.POST.get('beds', 0))
        bathrooms = float(request.POST.get('bathrooms', 0))
        balconies = int(request.POST.get('balconies', 0))
        furnishing = request.POST.get('furnishing')
        area_rate = float(request.POST.get('area_rate', 0))
        listing_type = request.POST.get('listing_type')
        
        if listing_type == 'sale':
            sale_price = float(request.POST.get('sale_price', 0))
            total_units = int(request.POST.get('total_units', 100))
            
            property_obj = PropertyForSale(
                house_type=house_type,
                locality=locality,
                city=city,
                area=area,
                beds=beds,
                bathrooms=bathrooms,
                balconies=balconies,
                furnishing=furnishing,
                area_rate=area_rate,
                owner=request.user,
                sale_price=sale_price,
                total_units=total_units
            )
        else:
            rent = float(request.POST.get('rent', 0))
            
            property_obj = PropertyForRent(
                house_type=house_type,
                locality=locality,
                city=city,
                area=area,
                beds=beds,
                bathrooms=bathrooms,
                balconies=balconies,
                furnishing=furnishing,
                area_rate=area_rate,
                owner=request.user,
                rent=rent
            )
        
        property_obj.save()
        
        for i in range(1, 6):
            image_key = f'image{i}'
            if image_key in request.FILES:
                image_file = request.FILES[image_key]
                setattr(property_obj, image_key, image_file)
        
        property_obj.save()
        
        messages.success(request, 'Property NFT created successfully!')
        return redirect('marketplace')
    
    return render(request, 'mint_property.html')