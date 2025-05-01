from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')



def marketplace(request):
    context = {}  
    return render(request, 'marketplace.html', context)

def mint(request):
    return render(request, 'mint_property.html')

def analyze(request):
    return render(request, 'analyze_page.html')

def dashboard(request):
    return render(request, 'dashboard.html')
