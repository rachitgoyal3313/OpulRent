import os
import django
from django.core.files import File
import urllib.request
import urllib.error
from http.client import HTTPResponse

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OpulRent.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile
from property.models import PropertyForSale, PropertyForRent

def run():
    # Clear existing data
    User.objects.all().delete()
    UserProfile.objects.all().delete()
    PropertyForSale.objects.all().delete()
    PropertyForRent.objects.all().delete()

    # Create dummy users
    users_data = [
        {"username": "john_doe", "email": "john@example.com", "password": "password123", "wallet_address": "0x1234567890abcdef1234567890abcdef12345678"},
        {"username": "jane_smith", "email": "jane@example.com", "password": "password123", "wallet_address": "0xabcdef1234567890abcdef1234567890abcdef12"},
        {"username": "bob_jones", "email": "bob@example.com", "password": "password123", "wallet_address": "0x7890abcdef1234567890abcdef1234567890abcd"},
        {"username": "alice_brown", "email": "alice@example.com", "password": "password123", "wallet_address": "0x4567890abcdef1234567890abcdef1234567890ab"},
        {"username": "charlie_wilson", "email": "charlie@example.com", "password": "password123", "wallet_address": "0x0abcdef1234567890abcdef1234567890abcdef123"},
    ]

    users = []
    for user_data in users_data:
        user = User.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"]
        )
        UserProfile.objects.create(
            user=user,
            wallet_address=user_data["wallet_address"]
        )
        users.append(user)

    # Ensure media/property_images directory exists
    media_images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media', 'property_images')
    os.makedirs(media_images_dir, exist_ok=True)

    # Properties for Sale with local images
    properties_for_sale = [
        {
            "house_type": "3 BHK Flat",
            "locality": "Bandra West",
            "city": "Mumbai",
            "area": 1500.0,
            "beds": 3,
            "bathrooms": 3.0,
            "balconies": 2,
            "furnishing": "Furnished",
            "area_rate": 250.0,
            "sale_price": 375000.0,
            "owner": users[0],
            "image_prefix": "1image"  # Will be used to generate image1, image2, etc.
        },
        {
            "house_type": "2 BHK Flat",
            "locality": "Koramangala",
            "city": "Bangalore",
            "area": 1200.0,
            "beds": 2,
            "bathrooms": 2.0,
            "balconies": 1,
            "furnishing": "Semi-Furnished",
            "area_rate": 80.0,
            "sale_price": 96000.0,
            "owner": users[1],
            "image_prefix": "2image"
        },
        # Add more properties here...
        # Truncated for brevity
    ]

    # Properties for Rent with local images
    properties_for_rent = [
        {
            "house_type": "2 BHK Flat",
            "locality": "Goregaon East",
            "city": "Mumbai",
            "area": 897.0,
            "beds": 2,
            "bathrooms": 2.0,
            "balconies": 0,
            "furnishing": "Semi-Furnished",
            "area_rate": 134.0,
            "rent": 120000.0,
            "owner": users[0],
            "image_prefix": "6image"
        },
        {
            "house_type": "1 BHK Flat",
            "locality": "Powai",
            "city": "Mumbai",
            "area": 490.0,
            "beds": 1,
            "bathrooms": 1.0,
            "balconies": 0,
            "furnishing": "Semi-Furnished",
            "area_rate": 82.0,
            "rent": 40000.0,
            "owner": users[1],
            "image_prefix": "7image"
        },
        # Add more properties here...
        # Truncated for brevity
    ]

    # Save properties for sale
    for prop_data in properties_for_sale:
        property_sale = PropertyForSale(
            house_type=prop_data["house_type"],
            locality=prop_data["locality"],
            city=prop_data["city"],
            area=prop_data["area"],
            beds=prop_data["beds"],
            bathrooms=prop_data["bathrooms"],
            balconies=prop_data["balconies"],
            furnishing=prop_data["furnishing"],
            area_rate=prop_data["area_rate"],
            sale_price=prop_data["sale_price"],
            owner=prop_data["owner"]
        )
        
        # Set the 5 images using the image prefix
        image_prefix = prop_data["image_prefix"]
        for i in range(1, 6):
            image_name = f"{image_prefix}{i}.jpg"
            image_path = os.path.join(media_images_dir, image_name)
            
            # Check if the image already exists in the media directory
            if os.path.exists(image_path):
                # Set the corresponding image field
                with open(image_path, 'rb') as f:
                    image_field = getattr(property_sale, f"image{i}")
                    image_field.save(image_name, File(f))
                print(f"Set image{i} for sale property: {prop_data['house_type']} in {prop_data['locality']} using {image_name}")
            else:
                # Create a placeholder image if it doesn't exist
                print(f"Warning: Image {image_name} not found for sale property {prop_data['house_type']} in {prop_data['locality']}")
                
        
        property_sale.save()

    # Save properties for rent
    for prop_data in properties_for_rent:
        property_rent = PropertyForRent(
            house_type=prop_data["house_type"],
            locality=prop_data["locality"],
            city=prop_data["city"],
            area=prop_data["area"],
            beds=prop_data["beds"],
            bathrooms=prop_data["bathrooms"],
            balconies=prop_data["balconies"],
            furnishing=prop_data["furnishing"],
            area_rate=prop_data["area_rate"],
            rent=prop_data["rent"],
            owner=prop_data["owner"]
        )
        
        # Set the 5 images using the image prefix
        image_prefix = prop_data["image_prefix"]
        for i in range(1, 6):
            image_name = f"{image_prefix}{i}.jpg"
            image_path = os.path.join(media_images_dir, image_name)
            
            # Check if the image already exists in the media directory
            if os.path.exists(image_path):
                # Set the corresponding image field
                with open(image_path, 'rb') as f:
                    image_field = getattr(property_rent, f"image{i}")
                    image_field.save(image_name, File(f))
                print(f"Set image{i} for rent property: {prop_data['house_type']} in {prop_data['locality']} using {image_name}")
            else:
                # Create a placeholder image if it doesn't exist
                print(f"Warning: Image {image_name} not found for rent property {prop_data['house_type']} in {prop_data['locality']}")
        
        property_rent.save()

    print("Database seeded successfully!")

if __name__ == "__main__":
    run()