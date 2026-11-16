from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.

from django.http import HttpResponse
from .models import Booking




def home(request):
    data = {
        'title': 'NextGen 🚀',
        'name': 'Jayanth',
        'role': 'Python Developer',
        'message': 'Welcome to my Django Project'
    }

    return render(request, 'index.html', data)




def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

 # 🔴 CHECK IF USER EXISTS
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists ❌")
          
# ✅ Create user
        user = User.objects.create_user(username=username, password=password)

        # 🚀 Redirect to login page
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse("Invalid credentials ❌")

    return render(request, 'login.html')

@login_required
def dashboard(request):
    bookings = Booking.objects.all()   # ✅ fetch data

    return render(request, 'dashboard.html', {
        'bookings': bookings
    })




from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')

def booking_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        date = request.POST.get('date')
        time = request.POST.get('time')

 #  SAVE TO DATABASE
        Booking.objects.create(
            name=name,
            date=date,
            time=time
        )

 #S send success to same page
        return render(request, 'booking.html', {
            'success': True,
            'name': name,
            'date': date,
            'time': time
        })

    return render(request, 'booking.html')        

       
from django.shortcuts import get_object_or_404

def delete_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.delete()
    return redirect('dashboard')



def edit_booking(request, id):
    booking = get_object_or_404(Booking, id=id)

    if request.method == "POST":
        booking.name = request.POST.get('name')
        booking.date = request.POST.get('date')
        booking.time = request.POST.get('time')
        booking.save()

        return redirect('dashboard')

    return render(request, 'booking.html', {'booking': booking})




from django.contrib import messages
from .models import Payment

def payment_view(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        method = request.POST.get('method')

        # ✅ SAVE PAYMENT (no booking link)
        Payment.objects.create(
            amount=amount,
            method=method
        )

        messages.success(request, f"Payment of ₹{amount} successful 🎉")

        return redirect('dashboard')

    return render(request, 'payment.html')


@login_required
def dashboard(request):
    bookings = Booking.objects.all()
    payments = Payment.objects.all()

    paid_booking_ids = payments.values_list('booking_id', flat=True)

    return render(request, 'dashboard.html', {
        'bookings': bookings,
        'payments': payments,
        'paid_booking_ids': paid_booking_ids
    })


from collections import defaultdict
from .models import MenuItem, Order

def menu_view(request):
    items = MenuItem.objects.all()

    # ✅ Group items by category
    grouped_items = defaultdict(list)
    for item in items:
        grouped_items[item.category].append(item)

    if request.method == "POST":
        item_id = request.POST.get('item_id')
        quantity = request.POST.get('quantity')

        item = MenuItem.objects.get(id=item_id)

        Order.objects.create(
            item=item,
            quantity=quantity
        )

        return redirect('dashboard')

    return render(request, 'menu.html', {'grouped_items': dict(grouped_items)})



from collections import defaultdict
from .models import MenuItem, Order

def menu_view(request):
    items = MenuItem.objects.all()

    # ✅ Group items by category
    grouped_items = defaultdict(list)
    for item in items:
        grouped_items[item.category].append(item)

    if request.method == "POST":
        item_id = request.POST.get('item_id')
        quantity = request.POST.get('quantity')

        item = MenuItem.objects.get(id=item_id)

        Order.objects.create(
            item=item,
            quantity=quantity
        )

        return redirect('dashboard')

    return render(request, 'menu.html', {'grouped_items': dict(grouped_items)})


from .models import Order

@login_required
def dashboard(request):
    bookings = Booking.objects.all()
    payments = Payment.objects.all()
    orders = Order.objects.all()   # ✅ ADD THIS
    total_bill = sum(order.total_price() for order in orders)

    return render(request, 'dashboard.html', {
        'bookings': bookings,
        'payments': payments,
        'orders': orders,
        'total_bill': total_bill

    })

def delete_order(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    return redirect('dashboard')


def edit_order(request, id):
    order = Order.objects.get(id=id)

    if request.method == "POST":
        quantity = request.POST.get('quantity')
        order.quantity = quantity
        order.save()
        return redirect('dashboard')

    return render(request, 'edit_order.html', {'order': order})   


from .models import Order
from django.contrib.auth.decorators import login_required

@login_required
def orders_view(request):
    orders = Order.objects.all()

    total_bill = sum(order.total_price() for order in orders)

    return render(request, 'orders.html', {
        'orders': orders,
        'total_bill': total_bill
    })