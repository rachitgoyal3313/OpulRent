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

    # Ensure media/images/ directory exists
    media_images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media', 'images')
    os.makedirs(media_images_dir, exist_ok=True)

    # Updated property images from Unsplash (verified URLs)
    property_images = [
        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
        "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde",
        "https://images.unsplash.com/photo-1600566753379-8c1a44c40800",
        "https://images.unsplash.com/photo-1600585153490-416c7edd80a0",
        "https://images.unsplash.com/photo-1600566753086-8f18c6a0d295",
        "https://images.unsplash.com/photo-1600585154526-990dced4db0d",
        "https://images.unsplash.com/photo-1600566753190-17f0e6df590d",
        "https://images.unsplash.com/photo-1600585152915-d208bec867a0",
        "https://images.unsplash.com/photo-1600585153780-4b4b9b7b9e0c",
        "https://images.unsplash.com/photo-1600566752222-6f18c6a0d2a0",
        "https://images.unsplash.com/photo-1600585153960-7b7b9e0c9e0c",
        "https://images.unsplash.com/photo-1600566752455-35792a6b9e0c",
        "https://images.unsplash.com/photo-1600585154120-4b4b9b7b9f0c",
        "https://images.unsplash.com/photo-1600566752686-8f18c6a0d3a0",
        "https://images.unsplash.com/photo-1600585154280-4b4b9b7b9a0c",
        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
        "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde",
        "https://images.unsplash.com/photo-1600566753379-8c1a44c40800",
        "https://images.unsplash.com/photo-1600585153490-416c7edd80a0",
        "https://images.unsplash.com/photo-1600566753086-8f18c6a0d295",
        "https://images.unsplash.com/photo-1600585154526-990dced4db0d",
        "https://images.unsplash.com/photo-1600566753190-17f0e6df590d",
        "https://images.unsplash.com/photo-1600585152915-d208bec867a0",
        "https://images.unsplash.com/photo-1600585153780-4b4b9b7b9e0c",
        "https://images.unsplash.com/photo-1600566752222-6f18c6a0d2a0",
        "https://images.unsplash.com/photo-1600585153960-7b7b9e0c9e0c",
        "https://images.unsplash.com/photo-1600566752455-35792a6b9e0c",
        "https://images.unsplash.com/photo-1600585154120-4b4b9b7b9f0c",
        "https://images.unsplash.com/photo-1600566752686-8f18c6a0d3a0",
        "https://images.unsplash.com/photo-1600585154280-4b4b9b7b9a0c",
    ]

    # Valid image MIME types
    valid_image_types = ['image/jpeg', 'image/png']

    # Properties for Sale
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
            "images": property_images[0]
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
            "images": property_images[1]
        },
        {
            "house_type": "4 BHK Villa",
            "locality": "Greater Kailash",
            "city": "New Delhi",
            "area": 3000.0,
            "beds": 4,
            "bathrooms": 4.0,
            "balconies": 3,
            "furnishing": "Furnished",
            "area_rate": 150.0,
            "sale_price": 450000.0,
            "owner": users[2],
            "images": property_images[2]
        },
        {
            "house_type": "2 BHK Flat",
            "locality": "Kharadi",
            "city": "Pune",
            "area": 1000.0,
            "beds": 2,
            "bathrooms": 2.0,
            "balconies": 2,
            "furnishing": "Unfurnished",
            "area_rate": 40.0,
            "sale_price": 40000.0,
            "owner": users[3],
            "images": property_images[3]
        },
        {
            "house_type": "3 BHK Flat",
            "locality": "Civil Lines",
            "city": "Nagpur",
            "area": 1400.0,
            "beds": 3,
            "bathrooms": 3.0,
            "balconies": 2,
            "furnishing": "Semi-Furnished",
            "area_rate": 25.0,
            "sale_price": 35000.0,
            "owner": users[4],
            "images": property_images[4]
        },
        {
            "house_type": "2 BHK Flat",
            "locality": "Andheri West",
            "city": "Mumbai",
            "area": 900.0,
            "beds": 2,
            "bathrooms": 2.0,
            "balconies": 1,
            "furnishing": "Furnished",
            "area_rate": 120.0,
            "sale_price": 108000.0,
            "owner": users[0],
            "images": property_images[5]
        },
        {
            "house_type": "3 BHK Flat",
            "locality": "Whitefield",
            "city": "Bangalore",
            "area": 1600.0,
            "beds": 3,
            "bathrooms": 3.0,
            "balconies": 2,
            "furnishing": "Semi-Furnished",
            "area_rate": 60.0,
            "sale_price": 96000.0,
            "owner": users[1],
            "images": property_images[6]
        },
        {
            "house_type": "4 BHK Flat",
            "locality": "Vasant Vihar",
            "city": "New Delhi",
            "area": 2500.0,
            "beds": 4,
            "bathrooms": 4.0,
            "balconies": 3,
            "furnishing": "Furnished",
            "area_rate": 140.0,
            "sale_price": 350000.0,
            "owner": users[2],
            "images": property_images[7]
        },
        {
            "house_type": "2 BHK Flat",
            "locality": "Hinjewadi",
            "city": "Pune",
            "area": 1100.0,
            "beds": 2,
            "bathrooms": 2.0,
            "balconies": 2,
            "furnishing": "Unfurnished",
            "area_rate": 35.0,
            "sale_price": 38500.0,
            "owner": users[3],
            "images": property_images[8]
        },
        {
            "house_type": "3 BHK Flat",
            "locality": "Manish Nagar",
            "city": "Nagpur",
            "area": 1300.0,
            "beds": 3,
            "bathrooms": 3.0,
            "balconies": 2,
            "furnishing": "Semi-Furnished",
            "area_rate": 20.0,
            "sale_price": 26000.0,
            "owner": users[4],
            "images": property_images[9]
        },
        {
            "house_type": "2 BHK Flat",
            "locality": "Powai",
            "city": "Mumbai",
            "area": 1000.0,
            "beds": 2,
            "bathrooms": 2.0,
            "balconies": 1,
            "furnishing": "Furnished",
            "area_rate": 100.0,
            "sale_price": 100000.0,
            "owner": users[0],
            "images": property_images[10]
        },
        {
            "house_type": "3 BHK Flat",
            "locality": "Hebbal",
            "city": "Bangalore",
            "area": 1700.0,
            "beds": 3,
            "bathrooms": 3.0,
            "balconies": 2,
            "furnishing": "Semi-Furnished",
            "area_rate": 70.0,
            "sale_price": 119000.0,
            "owner": users[1],
            "images": property_images[11]
        },
        {
            "house_type": "4 BHK Flat",
            "locality": "Safdarjung Enclave",
            "city": "New Delhi",
            "area": 2200.0,
            "beds": 4,
            "bathrooms": 4.0,
            "balconies": 3,
            "furnishing": "Furnished",
            "area_rate": 130.0,
            "sale_price": 286000.0,
            "owner": users[2],
            "images": property_images[12]
        },
        {
            "house_type": "2 BHK Flat",
            "locality": "Wagholi",
            "city": "Pune",
            "area": 950.0,
            "beds": 2,
            "bathrooms": 2.0,
            "balconies": 1,
            "furnishing": "Unfurnished",
            "area_rate": 30.0,
            "sale_price": 28500.0,
            "owner": users[3],
            "images": property_images[13]
        },
        {
            "house_type": "3 BHK Flat",
            "locality": "Somalwada",
            "city": "Nagpur",
            "area": 1500.0,
            "beds": 3,
            "bathrooms": 3.0,
            "balconies": 2,
            "furnishing": "Semi-Furnished",
            "area_rate": 22.0,
            "sale_price": 33000.0,
            "owner": users[4],
            "images": property_images[14]
        },
    ]

    # Properties for Rent
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
            "images": property_images[15]
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
            "images": property_images[16]
        },
        {
            "house_type": "1 BHK House",
            "locality": "Mundhwa",
            "city": "Pune",
            "area": 550.0,
            "beds": 1,
            "bathrooms": 1.0,
            "balconies": 0,
            "furnishing": "Unfurnished",
            "area_rate": 22.0,
            "rent": 12000.0,
            "owner": users[2],
            "images": property_images[17]
        },
        {
            "house_type": "2 BHK Flat",
            "locality": "Hingna",
            "city": "Nagpur",
            "area": 1000.0,
            "beds": 2,
            "bathrooms": 2.0,
            "balconies": 0,
            "furnishing": "Unfurnished",
            "area_rate": 8.0,
            "rent": 8000.0,
            "owner": users[3],
            "images": property_images[18]
        },
        {
            "house_type": "1 BHK Flat",
            "locality": "Mira Road",
            "city": "Mumbai",
            "area": 595.0,
            "beds": 1,
            "bathrooms": 1.0,
            "balconies": 0,
            "furnishing": "Unfurnished",
            "area_rate": 25.0,
            "rent": 15000.0,
            "owner": users[4],
            "images": property_images[19]
        },
        {
            "house_type": "1 BHK House",
            "locality": "Jakkur",
            "city": "Bangalore",
            "area": 600.0,
            "beds": 1,
            "bathrooms": 1.0,
            "balconies": 0,
            "furnishing": "Unfurnished",
            "area_rate": 27.0,
            "rent": 16000.0,
            "owner": users[0],
            "images": property_images[20]
        },
        {
            "house_type": "3 BHK Flat",
            "locality": "Chittaranjan Park",
            "city": "New Delhi",
            "area": 1260.0,
            "beds": 3,
            "bathrooms": 3.0,
            "balconies": 2,
            "furnishing": "Unfurnished",
            "area_rate": 47.67,
            "rent": 60000.0,
            "owner": users[1],
            "images": property_images[21]
        },
        {
            "house_type": "3 BHK Flat",
            "locality": "Soami Nagar South",
            "city": "New Delhi",
            "area": 2700.0,
            "beds": 3,
            "bathrooms": 3.0,
            "balconies": 2,
            "furnishing": "Semi-Furnished",
            "area_rate": 74.11,
            "rent": 200000.0,
            "owner": users[2],
            "images": property_images[22]
        },
        {
            "house_type": "1 BHK House",
            "locality": "Hadapsar",
            "city": "Pune",
            "area": 650.0,
            "beds": 1,
            "bathrooms": 1.0,
            "balconies": 0,
            "furnishing": "Unfurnished",
            "area_rate": 17.0,
            "rent": 11000.0,
            "owner": users[3],
            "images": property_images[23]
        },
        {
            "house_type": "1 BHK Flat",
            "locality": "Kharadi",
            "city": "Pune",
            "area": 495.0,
            "beds": 1,
            "bathrooms": 1.0,
            "balconies": 0,
            "furnishing": "Unfurnished",
            "area_rate": 48.0,
            "rent": 24000.0,
            "owner": users[4],
            "images": property_images[24]
        },
        {
            "house_type": "4 BHK House",
            "locality": "Indira Nagar",
            "city": "Bangalore",
            "area": 2000.0,
            "beds": 4,
            "bathrooms": 3.0,
            "balconies": 0,
            "furnishing": "Semi-Furnished",
            "area_rate": 40.0,
            "rent": 80000.0,
            "owner": users[0],
            "images": property_images[25]
        },
        {
            "house_type": "3 BHK Flat",
            "locality": "Whitefield",
            "city": "Bangalore",
            "area": 1543.0,
            "beds": 3,
            "bathrooms": 3.0,
            "balconies": 0,
            "furnishing": "Unfurnished",
            "area_rate": 39.0,
            "rent": 60000.0,
            "owner": users[1],
            "images": property_images[26]
        },
        {
            "house_type": "1 BHK Flat",
            "locality": "Powai",
            "city": "Mumbai",
            "area": 380.0,
            "beds": 1,
            "bathrooms": 2.0,
            "balconies": 0,
            "furnishing": "Furnished",
            "area_rate": 184.0,
            "rent": 70000.0,
            "owner": users[2],
            "images": property_images[27]
        },
        {
            "house_type": "3 BHK Flat",
            "locality": "Bandra East",
            "city": "Mumbai",
            "area": 1281.0,
            "beds": 3,
            "bathrooms": 3.0,
            "balconies": 0,
            "furnishing": "Semi-Furnished",
            "area_rate": 222.0,
            "rent": 290000.0,
            "owner": users[3],
            "images": property_images[28]
        },
        {
            "house_type": "4 BHK Flat",
            "locality": "Bandra East",
            "city": "Mumbai",
            "area": 2200.0,
            "beds": 4,
            "bathrooms": 4.0,
            "balconies": 3,
            "furnishing": "Unfurnished",
            "area_rate": 159.0,
            "rent": 350000.0,
            "owner": users[4],
            "images": property_images[29]
        },
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
        # Download and save image to media/images/
        image_url = prop_data["images"]
        image_name_base = image_url.split("/")[-1].split("?")[0]
        image_name = f"{image_name_base}.jpg"  # Enforce .jpg extension
        image_path = os.path.join(media_images_dir, image_name)
        try:
            # Open URL and check content type
            with urllib.request.urlopen(image_url) as response:
                if isinstance(response, HTTPResponse):
                    content_type = response.getheader('Content-Type')
                    if content_type not in valid_image_types:
                        raise ValueError(f"Invalid image type {content_type} for {image_url}")
                    # Download image
                    with open(image_path, 'wb') as f:
                        f.write(response.read())
                    # Save to ImageField
                    with open(image_path, 'rb') as f:
                        property_sale.images.save(image_name, File(f))
                    print(f"Successfully downloaded and saved image for sale property: {prop_data['house_type']} in {prop_data['locality']}")
        except urllib.error.HTTPError as e:
            print(f"Failed to download image {image_url} for sale property {prop_data['house_type']} in {prop_data['locality']}: {e}. Skipping image.")
        except ValueError as e:
            print(f"Invalid image for sale property {prop_data['house_type']} in {prop_data['locality']}: {e}. Skipping image.")
        except Exception as e:
            print(f"Unexpected error for image {image_url} for sale property {prop_data['house_type']} in {prop_data['locality']}: {e}. Skipping image.")
        property_sale.save()
        if os.path.exists(image_path):
            os.remove(image_path)

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
        # Download and save image to media/images/
        image_url = prop_data["images"]
        image_name_base = image_url.split("/")[-1].split("?")[0]
        image_name = f"{image_name_base}.jpg"  # Enforce .jpg extension
        image_path = os.path.join(media_images_dir, image_name)
        try:
            # Open URL and check content type
            with urllib.request.urlopen(image_url) as response:
                if isinstance(response, HTTPResponse):
                    content_type = response.getheader('Content-Type')
                    if content_type not in valid_image_types:
                        raise ValueError(f"Invalid image type {content_type} for {image_url}")
                    # Download image
                    with open(image_path, 'wb') as f:
                        f.write(response.read())
                    # Save to ImageField
                    with open(image_path, 'rb') as f:
                        property_rent.images.save(image_name, File(f))
                    print(f"Successfully downloaded and saved image for rent property: {prop_data['house_type']} in {prop_data['locality']}")
        except urllib.error.HTTPError as e:
            print(f"Failed to download image {image_url} for rent property {prop_data['house_type']} in {prop_data['locality']}: {e}. Skipping image.")
        except ValueError as e:
            print(f"Invalid image for rent property {prop_data['house_type']} in {prop_data['locality']}: {e}. Skipping image.")
        except Exception as e:
            print(f"Unexpected error for image {image_url} for rent property {prop_data['house_type']} in {prop_data['locality']}: {e}. Skipping image.")
        property_rent.save()
        if os.path.exists(image_path):
            os.remove(image_path)

    print("Database seeded successfully!")

if __name__ == "__main__":
    run()