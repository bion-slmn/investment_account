from .views import AccountView, UserView, AdminView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    # account routes
    path('view-account/<str:account_id>/', AccountView.as_view(), name='view-account'),
    path('create-account/', AccountView.as_view(), name='create-account'),
    path('update-account/<str:account_id>/', AccountView.as_view(), name='update-account'),
    path('delete-account/<str:account_id>/', AccountView.as_view(), name='delete-account'),

    # Admin only view user_transaction
    path('view-user-accounts/<str:user_id>/', AdminView.as_view(), name='view-user-accounts'),

    # register a user
    path('register-user/', UserView.as_view(), name='register-user'),

    # token routes and login 
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
]