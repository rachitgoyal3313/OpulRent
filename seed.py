import os
import django
from django.core.files import File

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OpulRent.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile
from property.models import PropertyForSale, PropertyForRent

def run():
    # Clear existing data
    print("Clearing existing data...")
    User.objects.all().delete()
    UserProfile.objects.all().delete()
    PropertyForSale.objects.all().delete()
    PropertyForRent.objects.all().delete()
    print("Existing data cleared.")

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
    print(f"Created {len(users)} users.")

    # Ensure opulent/media/property_images directory exists
    media_images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'opulent', 'media', 'property_images')
    os.makedirs(media_images_dir, exist_ok=True)
    print(f"Media directory ensured: {media_images_dir}")

    # Supported image extensions
    image_extensions = ['.jpg', '.jpeg', '.avif']

    # Define locations for properties
    locations = [
        ("Bandra West", "Mumbai"),
        ("Koramangala", "Bangalore"),
        ("Goregaon East", "Mumbai"),
        ("Powai", "Mumbai"),
        ("Jayanagar", "Bangalore"),
        ("Andheri West", "Mumbai"),
        ("Indiranagar", "Bangalore"),
        ("Malad West", "Mumbai"),
        ("Whitefield", "Bangalore"),
        ("Versova", "Mumbai"),
        ("Marathahalli", "Bangalore"),
        ("Juhu", "Mumbai"),
    ]

    # Properties for Sale (12 properties with prefixes 1image to 12image)
    properties_for_sale = []
    for i in range(12):
        idx = i + 1
        loc_idx = i % len(locations)
        properties_for_sale.append({
            "house_type": f"{2 + (i % 3)} BHK Flat",
            "locality": locations[loc_idx][0],
            "city": locations[loc_idx][1],
            "area": 800.0 + (i * 100.0),
            "beds": 2 + (i % 3),
            "bathrooms": 2.0 + (i % 2),
            "balconies": i % 3,
            "furnishing": ["Furnished", "Semi-Furnished", "Unfurnished"][i % 3],
            "area_rate": 100.0 + (i * 10.0),
            "sale_price": 50000.0 + (i * 25000.0),
            "owner": users[i % len(users)],
            "image_prefix": f"{idx}image"  # Images: 1image1.jpg to 12image5.jpg
        })

    # Properties for Rent (12 properties with prefixes 13image to 24image)
    properties_for_rent = []
    for i in range(12):
        idx = i + 13
        loc_idx = i % len(locations)
        properties_for_rent.append({
            "house_type": f"{1 + (i % 3)} BHK Flat",
            "locality": locations[loc_idx][0],
            "city": locations[loc_idx][1],
            "area": 500.0 + (i * 50.0),
            "beds": 1 + (i % 3),
            "bathrooms": 1.0 + (i % 2),
            "balconies": i % 2,
            "furnishing": ["Furnished", "Semi-Furnished", "Unfurnished"][i % 3],
            "area_rate": 50.0 + (i * 5.0),
            "rent": 20000.0 + (i * 10000.0),
            "owner": users[i % len(users)],
            "image_prefix": f"{idx}image"  # Images: 13image1.jpg to 24image5.jpg
        })

    # Save properties for sale
    print(f"Saving {len(properties_for_sale)} properties for sale...")
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
            image_field = getattr(property_sale, f"image{i}")
            image_assigned = False
            
            # Try each extension
            for ext in image_extensions:
                image_name = f"{image_prefix}{i}{ext}"
                image_path = os.path.join(media_images_dir, image_name)
                
                # Check if the image exists in the media directory
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        image_field.save(image_name, File(f))
                    print(f"Set image{i} for sale property: {prop_data['house_type']} in {prop_data['locality']} using {image_name}")
                    image_assigned = True
                    break
            
            if not image_assigned:
                print(f"Warning: No image found for sale property {prop_data['house_type']} in {prop_data['locality']} for image{i} with prefix {image_prefix}")
        
        property_sale.save()
    print(f"Saved {PropertyForSale.objects.count()} properties for sale.")

    # Save properties for rent
    print(f"Saving {len(properties_for_rent)} properties for rent...")
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
            image_field = getattr(property_rent, f"image{i}")
            image_assigned = False
            
            # Try each extension
            for ext in image_extensions:
                image_name = f"{image_prefix}{i}{ext}"
                image_path = os.path.join(media_images_dir, image_name)
                
                # Check if the image exists in the media directory
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        image_field.save(image_name, File(f))
                    print(f"Set image{i} for rent property: {prop_data['house_type']} in {prop_data['locality']} using {image_name}")
                    image_assigned = True
                    break
            
            if not image_assigned:
                print(f"Warning: No image found for rent property {prop_data['house_type']} in {prop_data['locality']} for image{i} with prefix {image_prefix}")
        
        property_rent.save()
    print(f"Saved {PropertyForRent.objects.count()} properties for rent.")

    print("Database seeded successfully!")

if __name__ == "__main__":
    run()