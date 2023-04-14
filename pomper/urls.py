from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('register_customer/', views.customer_registration,
         name='customer_registration'),
    path('register_admin/', views.admin_registration, name='admin_registration'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="password_reset.html"), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="password_reset_done.html"), name='password_reset_complete'),
    path('road_trip/<id>', views.specific_trip, name='trip'),
    path('book_trip/<id>', views.bookings, name='bookings'),
    path('search_tours/', views.search_tours, name='search'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('trips/', views.trips, name='trips'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery_post/', views.gallery_post, name='gallery_post'),
    path('adventures_safaris/<id>', views.a_tour, name='a_tour'),
    path('elements/', views.elements, name='elements'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('group_tours/', views.group_tours, name='group_tours'),
    path('road_trips/', views.road_trips, name='road_trips'),
    path('adventures_safaris/', views.adventures_safaris,
         name='adventures_safaris'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
# urlpatterns += staticfiles_urlpatterns()
