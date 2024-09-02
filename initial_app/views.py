from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from .models import Customer, Order
from .forms import CustomerForm, OrderForm

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def customer_management(request):
    customers = Customer.objects.all()
    return render(request, 'customer_management.html', {'customers': customers})

@login_required
def order_management(request):
    orders = Order.objects.all()
    return render(request, 'order_management.html', {'orders': orders})

@login_required
def home(request):
    # Get total number of customers
    total_customers = Customer.objects.count()
    
    # Get total number of orders
    total_orders = Order.objects.count()
    
    # Get total revenue
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Get top 5 customers by order count
    top_customers = Customer.objects.annotate(order_count=Count('orders')).order_by('-order_count')[:5]
    
    # Get order status distribution
    order_status = Order.objects.values('status').annotate(count=Count('status'))
    
    context = {
        'total_customers': total_customers,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'top_customers': top_customers,
        'order_status': order_status,
    }
    return render(request, 'home.html', context)

@login_required
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_management')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'edit_customer.html', {'form': form, 'customer': customer})

@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_management')
    else:
        form = OrderForm(instance=order)
    return render(request, 'edit_order.html', {'form': form, 'order': order})
