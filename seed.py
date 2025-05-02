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
    
    # Reset the ID sequences
    from django.db import connection
    with connection.cursor() as cursor:
        # Get the database engine being used
        db_engine = connection.vendor
        
        if db_engine == 'postgresql':
            # PostgreSQL sequence reset
            cursor.execute("SELECT setval(pg_get_serial_sequence('property_propertyforsale', 'id'), 1, false);")
            cursor.execute("SELECT setval(pg_get_serial_sequence('property_propertyforrent', 'id'), 1, false);")
        elif db_engine == 'sqlite':
            # SQLite sequence reset
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='property_propertyforsale';")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='property_propertyforrent';")
        elif db_engine == 'mysql':
            # MySQL sequence reset
            cursor.execute("ALTER TABLE property_propertyforsale AUTO_INCREMENT = 1;")
            cursor.execute("ALTER TABLE property_propertyforrent AUTO_INCREMENT = 1;")
    
    print("Existing data cleared and ID sequences reset.")

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

    # Ensure media/property_images directory exists
    # The path should be relative to the project root, not opulent subdirectory
    media_images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'property_images')
    os.makedirs(media_images_dir, exist_ok=True)
    print(f"Media directory ensured: {media_images_dir}")

    # Supported image extensions
    image_extensions = ['.jpg', '.jpeg', '.avif', '.png']

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
    sale_prices = [1.0, 2.0, 3.0]  # ETH values for sale prices
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
            "sale_price": sale_prices[i % len(sale_prices)],  # 1, 2, or 3 ETH
            "owner": users[i % len(users)],
            "image_prefix": f"{idx}image"  # Images: 1image1.jpg to 12image5.jpg
        })

    # Properties for Rent (12 properties with prefixes 13image to 24image)
    properties_for_rent = []
    rent_prices = [0.1, 0.2]  # ETH values for rent prices
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
            "rent": rent_prices[i % len(rent_prices)],  # 0.1 or 0.2 ETH
            "owner": users[i % len(users)],
            "image_prefix": f"{idx}image"  # Images: 13image1.jpg to 24image5.jpg
        })

    # Helper function to manually create image file paths in the database
    def set_image_path(property_obj, image_number, image_name):
        image_field = getattr(property_obj, f"image{image_number}")
        # Don't use File object, just set the path directly
        image_field.name = f"property_images/{image_name}"
        return True

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
        property_sale.save()  # Save first to get an ID
        
        # Set the 5 images using the image prefix
        image_prefix = prop_data["image_prefix"]
        for i in range(1, 6):
            image_assigned = False
            
            # Try each extension
            for ext in image_extensions:
                image_name = f"{image_prefix}{i}{ext}"
                image_path = os.path.join(media_images_dir, image_name)
                
                # Check if the image exists in the media directory
                if os.path.exists(image_path):
                    # Set the path directly instead of using File object
                    set_image_path(property_sale, i, image_name)
                    print(f"Set image{i} for sale property: {prop_data['house_type']} in {prop_data['locality']} using {image_name}")
                    image_assigned = True
                    break
            
            if not image_assigned:
                print(f"Warning: No image found for sale property {prop_data['house_type']} in {prop_data['locality']} for image{i} with prefix {image_prefix}")
        
        property_sale.save()  # Save again with the image paths
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
        property_rent.save()  # Save first to get an ID
        
        # Set the 5 images using the image prefix
        image_prefix = prop_data["image_prefix"]
        for i in range(1, 6):
            image_assigned = False
            
            # Try each extension
            for ext in image_extensions:
                image_name = f"{image_prefix}{i}{ext}"
                image_path = os.path.join(media_images_dir, image_name)
                
                # Check if the image exists in the media directory
                if os.path.exists(image_path):
                    # Set the path directly instead of using File object
                    set_image_path(property_rent, i, image_name)
                    print(f"Set image{i} for rent property: {prop_data['house_type']} in {prop_data['locality']} using {image_name}")
                    image_assigned = True
                    break
            
            if not image_assigned:
                print(f"Warning: No image found for rent property {prop_data['house_type']} in {prop_data['locality']} for image{i} with prefix {image_prefix}")
        
        property_rent.save()  # Save again with the image paths
    print(f"Saved {PropertyForRent.objects.count()} properties for rent.")

    print("Database seeded successfully!")

if __name__ == "__main__":
    run()