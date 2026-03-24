from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from MahalApp.models import Booking


@login_required
def my_bookings_view(request):
    if request.user.role != 'client':
        return redirect('dashboard')
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'client/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking_view(request, booking_id):
    if request.user.role != 'client':
        return redirect('dashboard')
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
        if booking.status == 'Pending':
            booking.status = 'Cancelled'
            booking.save()
            messages.success(request, 'Booking cancelled successfully!')
        else:
            messages.error(request, 'Only pending bookings can be cancelled!')
    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found!')
    return redirect('my_bookings')
