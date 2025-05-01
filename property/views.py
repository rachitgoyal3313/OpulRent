from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import PropertyForSale, PropertyForRent
from django.db.models import Q
from django.contrib import messages

def marketplace(request):
    search_query = request.GET.get('search', '')
    properties_for_sale = PropertyForSale.objects.all()
    properties_for_rent = PropertyForRent.objects.all()
    
    if search_query:
        # Combine sale and rent properties after filtering
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
            Q(beds__icontains=search_query)
        )
    else:
        properties = PropertyForSale.objects.all()
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

@login_required(login_url='/login/')
def property_action(request, property_id, property_type):
    if property_type == 'sale':
        property_obj = get_object_or_404(PropertyForSale, id=property_id)
        units_to_buy = int(request.POST.get('units', 1))
        if units_to_buy > property_obj.units_available:
            # Handle error, not enough units available
            messages.error(request, 'Not enough units available for purchase.')
            return redirect('property_detail', property_id=property_id, property_type=property_type)
        # Update units sold
        property_obj.units_sold += units_to_buy
        property_obj.save()
        # Additional logic for blockchain transaction here
        return redirect('purchase_confirmation', property_id=property_id)
    else:  # rent
        property_obj = get_object_or_404(PropertyForRent, id=property_id)
        # Logic for renting property
        # Here we would typically process rental terms, deposit, etc.
        # For now, we'll just redirect to the confirmation page
        return redirect('rental_confirmation', property_id=property_id)

@login_required(login_url='/login/')
def purchase_confirmation(request, property_id):
    property_obj = get_object_or_404(PropertyForSale, id=property_id)
    return render(request, 'purchase_confirmation.html', {'property': property_obj})

@login_required(login_url='/login/')
def rental_confirmation(request, property_id):
    property_obj = get_object_or_404(PropertyForRent, id=property_id)
    return render(request, 'rental_confirmation.html', {'property': property_obj})

@login_required(login_url='/users/login/')
def mint(request):
    """Handle property creation with image uploads"""
    if request.method == 'POST':
        # Get form data
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
        
        # Create property object based on listing type
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
        else:  # rent
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
        
        # Save the property to get an ID
        property_obj.save()
        
        # Handle image uploads
        for i in range(1, 6):
            image_key = f'image{i}'
            if image_key in request.FILES:
                image_file = request.FILES[image_key]
                # Set the image on the property
                setattr(property_obj, image_key, image_file)
        
        # Save the property again with images
        property_obj.save()
        
        # Show success message
        messages.success(request, 'Property NFT created successfully!')
        
        # Redirect to the marketplace
        return redirect('marketplace')
    
    return render(request, 'mint_property.html')