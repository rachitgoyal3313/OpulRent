from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import PropertyForSale, PropertyForRent

def marketplace(request):
    properties_for_sale = PropertyForSale.objects.all()
    properties_for_rent = PropertyForRent.objects.all()
    properties = list(properties_for_sale) + list(properties_for_rent)
    return render(request, 'marketplace.html', {'properties': properties})

def buy_properties(request):
    search_query = request.GET.get('search', '')
    if search_query:
        properties = PropertyForSale.objects.filter(
            house_type__icontains=search_query) | PropertyForSale.objects.filter(
            locality__icontains=search_query) | PropertyForSale.objects.filter(
            city__icontains=search_query)
    else:
        properties = PropertyForSale.objects.all()
    return render(request, 'buy.html', {'properties': properties})

def rent_properties(request):
    search_query = request.GET.get('search', '')
    if search_query:
        properties = PropertyForRent.objects.filter(
            house_type__icontains=search_query) | PropertyForRent.objects.filter(
            locality__icontains=search_query) | PropertyForRent.objects.filter(
            city__icontains=search_query)
    else:
        properties = PropertyForRent.objects.all()
    return render(request, 'rent.html', {'properties': properties})

def property_detail(request, property_id, property_type):
    if property_type == 'sale':
        property_obj = get_object_or_404(PropertyForSale, id=property_id)
    else:  # property_type == 'rent'
        property_obj = get_object_or_404(PropertyForRent, id=property_id)
    
    context = {
        'property': property_obj,
        'property_type': property_type
    }
    
    return render(request, 'property.html', context)

@login_required(login_url='/login/')
def property_action(request, property_id, property_type):
    if property_type == 'sale':
        property_obj = get_object_or_404(PropertyForSale, id=property_id)
        # Logic for buying property would go here
        # This is where you'd handle the blockchain transaction
        return redirect('purchase_confirmation', property_id=property_id)
    else:  # property_type == 'rent'
        property_obj = get_object_or_404(PropertyForRent, id=property_id)
        # Logic for renting property would go here
        # This is where you'd handle the blockchain transaction
        return redirect('rental_confirmation', property_id=property_id)

@login_required(login_url='/login/')
def purchase_confirmation(request, property_id):
    property_obj = get_object_or_404(PropertyForSale, id=property_id)
    return render(request, 'purchase_confirmation.html', {'property': property_obj})

@login_required(login_url='/login/')
def rental_confirmation(request, property_id):
    property_obj = get_object_or_404(PropertyForRent, id=property_id)
    return render(request, 'rental_confirmation.html', {'property': property_obj})