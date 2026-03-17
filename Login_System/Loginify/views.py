from django.shortcuts import render, redirect
from .models import UserDetails
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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

# Get all users
def get_all_users(request):
    users = UserDetails.objects.all()
    data = list(users.values())
    return JsonResponse(data, safe=False)

# Get single user by email
def get_user_by_email(request, email):
    try:
        user = UserDetails.objects.get(email=email)
        data = {'username': user.username, 'email': user.email}
        return JsonResponse(data)
    except UserDetails.DoesNotExist:
        return JsonResponse({'error': 'User not found!'}, status=404)

# Update user by email
@csrf_exempt
def update_user(request, email):
    if request.method == 'PUT':
        try:
            user = UserDetails.objects.get(email=email)
            data = json.loads(request.body)
            if 'username' in data:
                user.username = data['username']
            if 'password' in data:
                user.password = data['password']
            UserDetails.objects.filter(email=email).update(
                username=user.username,
                password=user.password
            )
            return JsonResponse({'message': 'User updated successfully!'})
        except UserDetails.DoesNotExist:
            return JsonResponse({'error': 'User not found!'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed!'}, status=405)

# Delete user by email
@csrf_exempt
def delete_user(request, email):
    if request.method == 'DELETE':
        try:
            user = UserDetails.objects.get(email=email)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully!'})
        except UserDetails.DoesNotExist:
            return JsonResponse({'error': 'User not found!'}, status=404)