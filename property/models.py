from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    house_type = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    area = models.FloatField()
    beds = models.IntegerField()
    bathrooms = models.FloatField()
    balconies = models.IntegerField()
    furnishing = models.CharField(max_length=50)
    area_rate = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Multiple image fields instead of a single field
    image1 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    image5 = models.ImageField(upload_to='property_images/', blank=True, null=True)

    class Meta:
        abstract = True

class PropertyForSale(Property):
    sale_price = models.FloatField()  # Price in ETH for buying
    total_units = models.IntegerField(default=100)
    units_sold = models.IntegerField(default=0)

    @property
    def units_available(self):
        return self.total_units - self.units_sold

    @property
    def unit_price(self):
        return self.sale_price / self.total_units if self.total_units else 0

    def __str__(self):
        return f"{self.house_type} in {self.locality}, {self.city} (For Sale)"



class PropertyForRent(Property):
    rent = models.FloatField()  # Monthly rent in ETH

    def __str__(self):
        return f"{self.house_type} in {self.locality}, {self.city} (For Rent)"