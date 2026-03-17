from django.shortcuts import render, redirect
from .models import UserDetails

def hello_world(request):
    return render(request, 'Loginify/signup.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if email already exists
        if UserDetails.objects.filter(email=email).exists():
            return render(request, 'Loginify/signup.html', 
                         {'error': 'Email already exists!'})
        
        # Check if username already exists
        if UserDetails.objects.filter(username=username).exists():
            return render(request, 'Loginify/signup.html', 
                         {'error': 'Username already exists!'})

        # Create new user
        user = UserDetails(username=username, email=email, password=password)
        user.save()

        # Redirect to login page after successful signup
        return redirect('/login/')
    
    return render(request, 'Loginify/signup.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = UserDetails.objects.get(email=email, password=password)
            # Show success message
            return render(request, 'Loginify/success.html', 
                         {'username': user.username})
        except UserDetails.DoesNotExist:
            return render(request, 'Loginify/login.html', 
                         {'error': 'Invalid email or password!'})
    
    return render(request, 'Loginify/login.html')