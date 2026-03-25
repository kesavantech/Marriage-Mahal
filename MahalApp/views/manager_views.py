from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from MahalApp.models import Booking


@login_required
def manage_bookings_view(request):
    if request.user.role not in ['manager', 'admin']:
        messages.error(request, 'Access Denied!')
        return redirect('dashboard')
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'manager/manage_bookings.html', {'bookings': bookings})


@login_required
def confirm_booking_view(request, booking_id):
    if request.user.role not in  ['manager','admin']:
        messages.error(request, 'Access Denied!')
        return redirect('dashboard')
    try:
        booking = Booking.objects.get(id=booking_id)
        if not booking.advance_paid:
            messages.error(request, 'Cannot confirm! Advance payment not verified yet.')
            return redirect('manage_bookings')
        booking.status = 'Confirmed'
        booking.save()
        messages.success(request, f'Booking #{booking.user.username} confirmed!')
    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found!')
    return redirect('manage_bookings')


@login_required
def mark_advance_paid_view(request, booking_id):
    if request.user.role not in  ['manager','admin']:
        messages.error(request, 'Access Denied!')
        return redirect('dashboard')
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.advance_paid = True
        booking.save()
        messages.success(request, f'Advance payment verified for Booking #{booking_id}!')
    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found!')
    return redirect('manage_bookings')


@login_required
def reject_booking_view(request, booking_id):
    if request.user.role not in  ['manager','admin']:
        messages.error(request, 'Access Denied!')
        return redirect('dashboard')
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.status = 'Rejected'
        booking.save()
        messages.success(request, f'Booking #{booking_id} rejected!')
    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found!')
    return redirect('manage_bookings')
