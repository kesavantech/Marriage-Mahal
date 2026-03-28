from .common_views import (
    home_view, register_view, login_view, dashboard_view,
    about_view, contact_view, special_view, whatsapp_greet,
    logout_view, header_view, footer_view, profile_view,
    booking_form_view, booking_details_view,
)

from .admin_views import (
    PartialsView, home_slider_view, home_banner_view, users_view,
    update_user_profile_view, admin_base_view, change_action, add_manager_view
)

from .client_views import my_bookings_view, cancel_booking_view

from .manager_views import manage_bookings_view, confirm_booking_view, reject_booking_view, mark_advance_paid_view