from django.urls import path
from .views import login_view, logout_view, create_admin

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),  # ← logout URL
    path('create-admin/', create_admin, name='create_admin'),
]
