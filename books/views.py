from urllib import request
from django.shortcuts import render, get_object_or_404,redirect
from .models import Book,Order,OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def index(request):
    books = Book.objects.all()  # Fetch all books from the database
    return render(request, 'index.html', {'books': books})
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('home')  # Redirect to home after successful login
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'login.html')
def signup(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pwd=request.POST.get('password')
        confpwd=request.POST.get('confirm_password')
        print(username)
        # password validation
        if pwd!=confpwd:
            messages.error(request,"Password do not match")
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
            return redirect('signup')
        user=User.objects.create_user(username=username,password=pwd)
        user.save()
        login(request,user)
        messages.success(request,"User created successfully")
        return redirect('home')  # Redirect to home after successful signup
    # If the request method is GET, render the signup page
    return render(request, 'signup.html')
def product_details(request, id):
    book = get_object_or_404(Book,id=id)
      # If the form was submitted (POST)
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart[str(book.id)] = cart.get(str(book.id), 0) + 1  # Increment quantity
        request.session['cart'] = cart  # Save back to session
        return redirect('home')  # ✅ Redirect to cart after adding
    return render(request, 'product_details.html', {'book': book})
def cart_view(request):
    # Handle removal
    remove_id = request.GET.get('remove')
    if remove_id:
        cart = request.session.get('cart', {})
        if remove_id in cart:
            cart[remove_id] -= 1
            if cart[remove_id] <= 0:
                del cart[remove_id]
        request.session['cart'] = cart
        return redirect('cart')

    # Normal view
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for book_id, quantity in cart.items():
        book = get_object_or_404(Book, id=book_id)
        cart_items.append({
            'book': book,
            'quantity': quantity,
            'subtotal': quantity * float(book.price)
        })
        total += quantity * float(book.price)

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})
# def orders_view(request):
#     cart = request.session.get('cart', {})
#     cart_items = []
#     total = 0

#     for book_id, quantity in cart.items():
#         book = get_object_or_404(Book, id=book_id)
#         cart_items.append({
#             'book': book,
#             'quantity': quantity,
#             'subtotal': quantity * float(book.price)
#         })
#         total += quantity * float(book.price)

    return render(request, 'orders.html', {'cart_items': cart_items, 'total': total})
@login_required
@csrf_exempt  # Use with caution, only if necessary

def shipping_details(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'shipping_details.html', {'book': book})

def order_success(request):
    return render(request, 'order_success.html')
@login_required
def shipping_details_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for book_id, quantity in cart.items():
        book = get_object_or_404(Book, id=book_id)
        cart_items.append({
            'book': book,
            'quantity': quantity,
            'subtotal': quantity * float(book.price)
        })
        total += quantity * float(book.price)
    if request.method == "POST" and "name" in request.POST:
        # Submit shipping
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        latest_order = Order.objects.filter(user=request.user).order_by('-order_number').first()
        next_order_number = 1 if not latest_order else latest_order.order_number + 1
        order = Order.objects.create(
            user=request.user,
            address=address,
            phone=phone,
            email=email,
            order_number=next_order_number
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item['book'],
                quantity=item['quantity'],
                price=item['book'].price
            )

        # Clear cart
        request.session['cart'] = {}
        return redirect('order_success')

    return render(request, "shipping_details.html", {
        "cart_items": cart_items,
        "total": total
    })
# def orders_view(request):
#     orders = Order.objects.filter(user=request.user).order_by('-created_at')
#     return render(request, 'orders.html', {'orders': orders})
@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    orders = Order.objects.filter(user=request.user).prefetch_related('items__book')
# Add total field for each order
    for order in orders:
        order.total = sum(item.quantity * item.price for item in order.items.all())

    return render(request, 'orders.html', {'orders': orders})
@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.delete()
        messages.success(request, "Order canceled.")
    return redirect('orders')
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')