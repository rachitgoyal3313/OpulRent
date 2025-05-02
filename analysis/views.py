from django.shortcuts import render
from django.http import JsonResponse
from .ml_models import predict_rent_roi_growth  # Updated import
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Allowed cities for dropdown
ALLOWED_CITIES = ['Mumbai', 'Pune', 'Nagpur', 'Bangalore', 'New Delhi']

def analyze(request):
    context = {}
    if request.method == "POST":
        data = request.POST
        try:
            logger.info("Processing analyze request with data: %s", data)
            
            city = data.get("location")
            if city not in ALLOWED_CITIES:
                context["error"] = "Invalid city selected. Please choose from the dropdown."
                return render(request, 'analyze_page.html', context)

            # Calculate area_rate from price and size
            size = float(data.get("size", 0))
            price = float(data.get("price", 0))
            area_rate = price / size if size > 0 else 0
            
            logger.info("Calculated area_rate: %f", area_rate)

            user_input = {
                'locality': city,
                'city': city,
                'area': size,
                'Estimated Price': price,
                'beds': int(data.get("bedrooms") or 1),
                'bathrooms': int(data.get("bathrooms") or 1),
                'type': data.get("propertyType") or "Flat",
                'furnishing': data.get("furnishing") or "semi-furnished",
            }

            prediction = predict_rent_roi_growth(user_input)
            logger.info("Prediction result: %s", prediction)

            context["prediction"] = {
                'predicted_rent': prediction['predicted_rent'],
                'predicted_roi': prediction['predicted_roi'],
                'predicted_growth': prediction['growth_score']
            }
        except Exception as e:
            logger.error("Error processing prediction: %s", str(e), exc_info=True)
            context["error"] = f"Error processing prediction: {str(e)}"
    return render(request, 'analyze_page.html', context)

# Optional API view (commented out)
# def predict_investment(request):
#     if request.method == "POST":
#         data = request.POST
#         try:
#             logger.info("Processing predict_investment request with data: %s", data)
#             size = float(data.get("size", 0))
#             price = float(data.get("price", 0))
#             area_rate = price / size if size > 0 else 0
#             
#             prediction = predict_rent_roi_growth({...})
#             return JsonResponse(prediction)
#         except Exception as e:
#             return JsonResponse({"error": f"Prediction failed: {str(e)}"}, status=400)
#     return JsonResponse({"error": "Invalid request method"}, status=400)
