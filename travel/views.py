from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from .models import Package, Booking


# ─── HOME ─────────────────────────────────────────────────────
def home(request):
    featured = Package.objects.filter(is_featured=True)
    pakistan = Package.objects.filter(region='pakistan')
    return render(request, 'travel/home.html', {
        'featured': featured,
        'pakistan': pakistan,
    })


# ─── SIGNUP ───────────────────────────────────────────────────
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username   = request.POST.get('username', '').strip()
        email      = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        password1  = request.POST.get('password1', '')
        password2  = request.POST.get('password2', '')

        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('signup')

        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters!')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken! Try another one.')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered! Try logging in.')
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
        )
        login(request, user)
        messages.success(request, f'Welcome to Voyara, {first_name or username}! 🎉')
        return redirect('dashboard')

    return render(request, 'travel/signup.html')


# ─── LOGIN ────────────────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user     = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}! ✈')
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'travel/login.html')


# ─── LOGOUT ───────────────────────────────────────────────────
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out. Safe travels! ✈')
    return redirect('home')


# ─── PASSENGER DASHBOARD ──────────────────────────────────────
@login_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    packages = Package.objects.filter(is_featured=True)[:6]
    return render(request, 'travel/dashboard.html', {
        'bookings': bookings,
        'packages': packages,
    })


# ─── PACKAGE DETAIL ───────────────────────────────────────────
def package_detail(request, pk):
    package = get_object_or_404(Package, pk=pk)
    return render(request, 'travel/package_detail.html', {
        'package': package,
    })


# ─── BOOK TICKET ──────────────────────────────────────────────
@login_required
def book_ticket(request, pk):
    package = get_object_or_404(Package, pk=pk)

    if request.method == 'POST':
        num_passengers  = int(request.POST.get('num_passengers', 1))
        total_pkr       = package.price_pkr * num_passengers
        total_usd       = package.price_usd * num_passengers

        Booking.objects.create(
            user            = request.user,
            package         = package,
            full_name       = request.POST.get('full_name', ''),
            email           = request.POST.get('email', ''),
            phone           = request.POST.get('phone', ''),
            num_passengers  = num_passengers,
            travel_date     = request.POST.get('travel_date'),
            total_price_pkr = total_pkr,
            total_price_usd = total_usd,
            special_notes   = request.POST.get('special_notes', ''),
        )
        messages.success(request, f'Booking confirmed for {package.name}! 🎉 Check My Bookings for details.')
        return redirect('my_bookings')

    return render(request, 'travel/book_ticket.html', {
        'package': package,
        'today'  : date.today(),
    })


# ─── MY BOOKINGS ──────────────────────────────────────────────
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'travel/my_bookings.html', {
        'bookings': bookings,
    })


# ─── ADMIN DASHBOARD ──────────────────────────────────────────
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'Admin access only!')
        return redirect('dashboard')

    bookings  = Booking.objects.all().select_related('package', 'user')
    packages  = Package.objects.all()
    total_rev = sum(b.total_price_pkr for b in bookings)

    return render(request, 'travel/admin_dashboard.html', {
        'bookings'   : bookings,
        'packages'   : packages,
        'total_rev'  : total_rev,
        'total_book' : bookings.count(),
        'total_pkg'  : packages.count(),
        'total_users': User.objects.filter(is_staff=False).count(),
    })

# ─── UPDATE BOOKING STATUS 
@login_required
def update_booking_status(request, pk, status):
    if not request.user.is_staff:
        return redirect('dashboard')

    booking = get_object_or_404(Booking, pk=pk)
    booking.status = status
    booking.save()
    messages.success(request, f'Booking for {booking.full_name} marked as {status}!')
    return redirect('admin_dashboard')