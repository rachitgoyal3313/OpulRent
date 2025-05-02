from django.db import models
from django.contrib.auth.models import User
from property.models import PropertyForSale, PropertyForRent

class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('sale', 'Sale'),
        ('rent', 'Rent'),
    )
    
    property_sale = models.ForeignKey(PropertyForSale, on_delete=models.CASCADE, null=True, blank=True, related_name='sale_transactions')
    property_rent = models.ForeignKey(PropertyForRent, on_delete=models.CASCADE, null=True, blank=True, related_name='rent_transactions')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_properties')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sold_properties')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    units = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.transaction_type == 'sale':
            return f"Sale - {self.property_sale}"
        return f"Rent - {self.property_rent}"

class RentalAgreement(models.Model):
    property = models.ForeignKey(PropertyForRent, on_delete=models.CASCADE, related_name='rental_agreements')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rented_properties')
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leased_properties')
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Rental - {self.property}"