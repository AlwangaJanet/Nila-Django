from django.http import HttpResponse
from django.shortcuts import render,redirect
import pyrebase

from django.shortcuts import render, redirect
from django.contrib import messages
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

from .forms import ProductForm

from django.shortcuts import render, redirect
from .forms import ProductForm
from firebase_admin import storage
import firebase_admin
from firebase_admin import credentials
from django.contrib import auth

bucket = storage.bucket()
config = {
  "apiKey": "AIzaSyDE7yGe59hvtnlrnagcu9e0pZrzv5mjuy4",
  "authDomain": "nilaap-42c61.firebaseapp.com",
  "databaseURL": "https://nilaap-42c61-default-rtdb.firebaseio.com",
  "projectId": "nilaap-42c61",
  "storageBucket": "nilaap-42c61.appspot.com",
  "messagingSenderId": "215693699799",
  "appId": "1:215693699799:web:367d91a0caa0e959b39e92",
}

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
from firebase_admin import db

def view_users(request):
    # Reference to the 'Users' node in your Firebase Realtime Database
    users_ref = db.reference('Users')

    # Get all users
    users = users_ref.get()

    # Check if users is not None before iterating over it
    if users is not None:
        # Extract user data and iterate over users
        user_data = []
        for user_id, user_info in users.items():
            # Assuming user information is stored with keys like 'name', 'email', etc.
            name = user_info.get('name')
            email = user_info.get('email')
            address = user_info.get('address')
            gender = user_info.get('gender')
            user_type = user_info.get('userType')
            photo_url = user_info.get('photoUrl')

            user_data.append({
                'name': name,
                'email': email,
                'address': address,
                'gender': gender,
                'user_type': user_type,
                'photo_url': photo_url
            })

        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = authe.sign_in_with_email_and_password(email,password)
        except:
            message ="invalid credentials"
            return render(request, 'shop/login.html', {'messages': message})

        return render(request, 'shop/main.html', {'users': user_data,"user":email})
    else:
        # Handle case when users is None (e.g., display a message or redirect to an error page)
        return HttpResponse("No users found or error fetching user data")



def login(request):
    

    return render(request, 'shop/login.html') 


def logout(request):
    auth.logout(request)
    return render(request,'shop/login.html')
    

# views.py

from django.shortcuts import render
from firebase_admin import db

def view_orders(request):
    # Access Firebase Realtime Database
    ref = db.reference('/')

    # Get reference to the 'orders' node
    orders_ref = ref.child('Order')

    # Get all orders data
    all_orders = orders_ref.get()

    # Pass orders data to template
    return render(request, 'shop/orders.html', {'orders': all_orders})

from django.shortcuts import render
import firebase_admin
from firebase_admin import credentials, db

def product_list(request):
    # Initialize Firebase app (replace firebase-credentials.json with your own credentials file)
   
    # Access Firebase Realtime Database
    ref = db.reference('/Products')

    # Get all products data
    products = ref.get()

    # Pass products data to template
    return render(request, 'shop/product_list.html', {'products': products})


def Pre_product_list(request):
    # Initialize Firebase app (replace firebase-credentials.json with your own credentials file)
   
    # Access Firebase Realtime Database
    ref = db.reference('/Pre-Order Products')

    # Get all products data
    products = ref.get()

    # Pass products data to template
    return render(request, 'shop/product_list_pre.html', {'products': products})

# Import necessary modules
import os
import urllib
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import firebase_admin
from firebase_admin import credentials, db, storage
from .models import Product

# Initialize Firebase Admin SDK
db_ref = db.reference('Products')
storage_client = storage.bucket()

# Function to handle product addition or update
@csrf_exempt
def add_or_update_product(request):
    if request.method == 'POST':
        # Extract product details from POST request
        product_id = request.POST.get('product_id', None)
        name = request.POST.get('name', None)
        category = request.POST.get('category', None)
        price = float(request.POST.get('price', 0))
        stock = int(request.POST.get('stock', 0))
        description = request.POST.get('description', None)
        sizes = request.POST.getlist('sizes', [])
        
        # Upload product image to Firebase Storage
        product_img = request.FILES.get('product_img', None)
        if product_img and product_id:
            image_blob = storage_client.blob('product_images/' + str(product_id) + '.jpg')
            image_blob.upload_from_string(product_img.read(), content_type='image/jpeg')
            image_url = image_blob.public_url
        else:
            image_url = ''  # Default image URL
        
        # Add or update product in Firebase Realtime Database
        if product_id:
            db_ref.child(product_id).update({
                'name': name,
                'category': category,
                'price': price,
                'stock': stock,
                'description': description,
                'sizes': sizes,
                'photoUrl': image_url
            })
            message = "Product updated successfully."
        else:
            new_product_ref = db_ref.push()
            new_product_ref.set({
                'name': name,
                'category': category,
                'price': price,
                'stock': stock,
                'description': description,
                'sizes': sizes,
                'photoUrl': image_url
            })
            message = "Product added successfully."
        
        return JsonResponse({'success': True, 'message': message})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

# Function to render the product upload form
def new_product(request):
    return render(request, 'shop/new_product.html')
