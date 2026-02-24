# Import all common views to make them available at package level
from .common_views import (
    home_view,
    register_view,
    login_view, 
    dashboard_view,
    about_view, 
    contact_view, 
    special_view,
    whatsapp_greet,
    logout_view, 
    header_view, 
    footer_view, 
    profile_view,
    
)
# Import admin views
from .admin_views import (
    PartialsView, home_slider_view,home_banner_view
)