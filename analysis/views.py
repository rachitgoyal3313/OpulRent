from django.shortcuts import render
from django.http import JsonResponse
from .ml_models import predict_property  # Direct import of the function
import logging

# Set up logging
logger = logging.getLogger(__name__)

def analyze(request):
    context = {}
    if request.method == "POST":
        data = request.POST
        try:
            logger.info("Processing analyze request with data: %s", data)
            
            # Calculate area_rate from price and size
            size = float(data.get("size", 0))
            price = float(data.get("price", 0))
            area_rate = price / size if size > 0 else 0
            
            logger.info("Calculated area_rate: %f", area_rate)
            
            prediction = predict_property(
                type_=data.get("propertyType") or "Flat",
                locality=data.get("location") or "Unknown",
                city=data.get("location") or "Unknown",  # Using location as city since we have only one field
                furnishing=data.get("furnishing") or "semi-furnished",
                bhk=int(data.get("bedrooms") or 1),
                area=float(data.get("size") or 1000),
                beds=int(data.get("bedrooms") or 1),
                bathrooms=int(data.get("bathrooms") or 1),
                balconies=0,  # Default value since we don't have this field in the form
                area_rate=area_rate
            )
            logger.info("Prediction result: %s", prediction)
            context["prediction"] = prediction
        except Exception as e:
            logger.error("Error processing prediction: %s", str(e), exc_info=True)
            context["error"] = f"Error processing prediction: {str(e)}"
    return render(request, 'analyze_page.html', context)

def predict_investment(request):
    if request.method == "POST":
        data = request.POST
        try:
            logger.info("Processing predict_investment request with data: %s", data)
            
            size = float(data.get("size", 0))
            price = float(data.get("price", 0))
            area_rate = price / size if size > 0 else 0
            
            logger.info("Calculated area_rate: %f", area_rate)
            
            prediction = predict_property(
                type_=data.get("propertyType") or "Flat",
                locality=data.get("location") or "Unknown",
                city=data.get("location") or "Unknown",  # Using location as city since we have only one field
                furnishing=data.get("furnishing") or "semi-furnished",
                bhk=int(data.get("bedrooms") or 1),
                area=float(data.get("size") or 1000),
                beds=int(data.get("bedrooms") or 1),
                bathrooms=int(data.get("bathrooms") or 1),
                balconies=0,  # Default value since we don't have this field in the form
                area_rate=area_rate
            )
            logger.info("Prediction result: %s", prediction)
            return JsonResponse(prediction)
        except Exception as e:
            logger.error("Error in predict_investment: %s", str(e), exc_info=True)
            return JsonResponse({"error": f"Prediction failed: {str(e)}"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=400)