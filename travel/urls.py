from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.home,            name='home'),
    path('signup/',             views.signup_view,     name='signup'),
    path('login/',              views.login_view,      name='login'),
    path('logout/',             views.logout_view,     name='logout'),
    path('dashboard/',          views.dashboard,       name='dashboard'),
    path('package/<int:pk>/',   views.package_detail,  name='package_detail'),
    path('book/<int:pk>/',      views.book_ticket,     name='book_ticket'),
    path('my-bookings/',        views.my_bookings,     name='my_bookings'),
    path('admin-dashboard/',    views.admin_dashboard, name='admin_dashboard'),
    path('booking/<int:pk>/status/<str:status>/', views.update_booking_status, name='update_booking_status'),
]
