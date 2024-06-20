# URLs (urls.py)

from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views 
from .views import test_email
from .views import ForgotPasswordView, ResetPasswordView, VerifyOTPView

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('cookies/', views.cookies_view, name='cookies'),
    path('category/<int:category_id>/', views.category_items, name='category_items'),
    path('contact/', views.contact, name='contact'),
    path('student-portal/', views.student_portal, name='student_portal'),
    path('student-practical/', views.student_practical, name='student_practical'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('ready-to-wear/', views.ready_to_wear, name='ready_to_wear'),
    path('ebook/', views.ebook, name='ebook'),
    path('training/', views.training, name='training'),
    path('custom-made/', views.custom_made, name='custom_made'),
    path('courses/', views.courses, name='courses'),
    path('market-place/', views.market_place, name='market_place'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_user, name='update_user'),
    path('account/delete/', views.delete_account, name='delete_account'),
    path('terms_and_conditions/', views.terms_and_conditions_view, name='terms_and_conditions'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('verify_otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('admin/', admin.site.urls),  # Default Django admin
    
]
