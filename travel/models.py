from django.db import models
from django.contrib.auth.models import User


class Package(models.Model):

    REGION_CHOICES = [
        ('pakistan',    'Pakistan'),
        ('asia',        'Asia'),
        ('europe',      'Europe'),
        ('middle_east', 'Middle East'),
        ('americas',    'Americas'),
        ('africa',      'Africa'),
    ]

    name          = models.CharField(max_length=200)
    country       = models.CharField(max_length=100)
    region        = models.CharField(max_length=50, choices=REGION_CHOICES)
    description   = models.TextField()
    detail        = models.TextField(blank=True)
    image_url     = models.URLField(max_length=500)
    altitude      = models.CharField(max_length=100, blank=True)
    best_season   = models.CharField(max_length=100, blank=True)
    duration_days = models.IntegerField(default=5)
    price_pkr     = models.DecimalField(max_digits=10, decimal_places=2)
    price_usd     = models.DecimalField(max_digits=8,  decimal_places=2)
    is_featured   = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.country}"

    class Meta:
        ordering = ['-is_featured', 'name']


class Booking(models.Model):

    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    package         = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='bookings')
    full_name       = models.CharField(max_length=200)
    email           = models.EmailField()
    phone           = models.CharField(max_length=20)
    num_passengers  = models.IntegerField(default=1)
    travel_date     = models.DateField()
    total_price_pkr = models.DecimalField(max_digits=10, decimal_places=2)
    total_price_usd = models.DecimalField(max_digits=8,  decimal_places=2)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_notes   = models.TextField(blank=True)
    booked_at       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} → {self.package.name} ({self.status})"

    class Meta:
        ordering = ['-booked_at']