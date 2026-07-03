from rest_framework import serializers
from .models import Destination, Fare
from .models import Destination, Fare, Booking

class FareSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Fare
        fields = [
            'id',
            'origin',
            'transport_type',
            'price_usd',
            'duration_nights',
            'depart_date',
            'return_date',
            'airline',
            'is_featured',
        ]


class DestinationSerializer(serializers.ModelSerializer):
    fares = FareSerializer(many=True, read_only=True)

    class Meta:
        model  = Destination
        fields = [
            'id',
            'name',
            'country',
            'region',
            'description',
            'image_url',
            'altitude',
            'best_season',
            'is_featured',
            'fares',        # ← includes all fares for this destination
        ]

   # ← update this import


class BookingSerializer(serializers.ModelSerializer):
    fare_details = FareSerializer(source='fare', read_only=True)

    class Meta:
        model  = Booking
        fields = [
            'id',
            'fare',
            'fare_details',
            'full_name',
            'email',
            'phone',
            'num_passengers',
            'total_price',
            'status',
            'booked_at',
            'notes',
        ]
        read_only_fields = ['total_price', 'status', 'booked_at']        